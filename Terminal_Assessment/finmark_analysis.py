"""Validate the FinMark terminal-assessment data and generate final evidence."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
FIGURE_DIR = BASE_DIR / "figures"
EVIDENCE_DIR = BASE_DIR / "evidence"

DATASETS = {
    "Demographics": {
        "raw": "customer_demographics_contaminated.csv",
        "clean": "Cleaned_Customer_Demographics.csv",
        "key": "CustomerID",
        "date": "SignupDate",
    },
    "Transactions": {
        "raw": "customer_transactions_contaminated.csv",
        "clean": "Cleaned_Customer_Transactions.csv",
        "key": "TransactionID",
        "date": "TransactionDate",
    },
    "Social Media": {
        "raw": "social_media_interactions_contaminated.csv",
        "clean": "Cleaned_Social_Media_Interactions.csv",
        "key": "InteractionID",
        "date": "InteractionDate",
    },
}


def load_data() -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    """Load packaged raw and cleaned datasets."""
    raw: dict[str, pd.DataFrame] = {}
    clean: dict[str, pd.DataFrame] = {}
    for name, metadata in DATASETS.items():
        raw[name] = pd.read_csv(RAW_DIR / metadata["raw"])
        clean[name] = pd.read_csv(
            CLEAN_DIR / metadata["clean"], parse_dates=[metadata["date"]]
        )
    return raw, clean


def validate_data(
    raw: dict[str, pd.DataFrame], clean: dict[str, pd.DataFrame]
) -> None:
    """Raise an error if a final dataset violates a required invariant."""
    for name, metadata in DATASETS.items():
        key = metadata["key"]
        date = metadata["date"]
        assert len(raw[name]) == 3200, f"Unexpected raw row count: {name}"
        assert len(clean[name]) == 3000, f"Unexpected cleaned row count: {name}"
        assert clean[name][key].notna().all(), f"Missing business key: {name}"
        assert clean[name][key].is_unique, f"Duplicate business key: {name}"
        assert clean[name][date].notna().all(), f"Unparsed date: {name}"

    demographics = clean["Demographics"]
    transactions = clean["Transactions"]
    social = clean["Social Media"]
    assert demographics["Age"].between(18, 70).all()
    assert demographics.isna().sum().sum() == 0
    assert social.isna().sum().sum() == 0
    assert transactions["Amount"].isna().sum() == transactions["IsFreeLabel"].sum()
    assert transactions.loc[transactions["IsFreeLabel"], "Amount"].isna().all()
    assert transactions.loc[transactions["IsNegativeAmount"], "Amount"].lt(0).all()
    assert transactions.loc[transactions["WasAmountImputed"], "Amount"].notna().all()


def extended_statistics(series: pd.Series) -> dict[str, float | int]:
    """Return the descriptive statistics required by the assessment."""
    values = series.dropna()
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    return {
        "Valid count": int(values.count()),
        "Mean": float(values.mean()),
        "Median": float(values.median()),
        "Mode": float(values.mode().iloc[0]),
        "Standard deviation": float(values.std()),
        "Variance": float(values.var()),
        "Minimum": float(values.min()),
        "Maximum": float(values.max()),
        "Range": float(values.max() - values.min()),
        "Q1": float(q1),
        "Q3": float(q3),
        "IQR": float(q3 - q1),
        "Coefficient of variation": float(values.std() / values.mean()),
    }


def outlier_summary(series: pd.Series) -> dict[str, float | int]:
    """Apply the 1.5 x IQR screening rule."""
    values = series.dropna()
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return {
        "Q1": float(q1),
        "Q3": float(q3),
        "Lower bound": float(lower),
        "Upper bound": float(upper),
        "Outlier count": int(((values < lower) | (values > upper)).sum()),
    }


def build_evidence(
    raw: dict[str, pd.DataFrame], clean: dict[str, pd.DataFrame]
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Calculate every quantitative claim used by the final report."""
    data_quality: dict[str, dict[str, int | list[int]]] = {}
    for name, metadata in DATASETS.items():
        raw_frame = raw[name]
        clean_frame = clean[name]
        key = metadata["key"]
        distinct_conflicts = (
            raw_frame.drop_duplicates()
            .loc[lambda frame: frame.duplicated(key, keep=False), key]
            .nunique()
        )
        data_quality[name] = {
            "Raw shape": list(raw_frame.shape),
            "Clean shape": list(clean_frame.shape),
            "Exact duplicate rows before": int(raw_frame.duplicated().sum()),
            "Duplicate business-key rows before": int(raw_frame[key].duplicated().sum()),
            "Distinct conflicting business keys": int(distinct_conflicts),
            "Duplicate business-key rows after": int(clean_frame[key].duplicated().sum()),
            "Missing cells before": int(raw_frame.isna().sum().sum()),
            "Missing cells after": int(clean_frame.isna().sum().sum()),
        }

    demographics = clean["Demographics"]
    transactions = clean["Transactions"]
    social = clean["Social Media"]
    statistics = pd.DataFrame(
        {
            "Age": extended_statistics(demographics["Age"]),
            "Transaction amount": extended_statistics(transactions["Amount"]),
        }
    )
    outliers = pd.DataFrame(
        {
            "Age": outlier_summary(demographics["Age"]),
            "Transaction amount": outlier_summary(transactions["Amount"]),
        }
    )

    transaction_features = transactions.groupby("CustomerID").agg(
        TotalSpend=("Amount", "sum"),
        AverageAmount=("Amount", "mean"),
        TransactionCount=("TransactionID", "count"),
    )
    social_features = social.groupby("CustomerID").agg(
        SocialInteractions=("InteractionID", "count")
    )
    customer_features = (
        demographics.set_index("CustomerID")[["Age"]]
        .join(transaction_features)
        .join(social_features)
    )
    customer_features[["TotalSpend", "TransactionCount", "SocialInteractions"]] = (
        customer_features[
            ["TotalSpend", "TransactionCount", "SocialInteractions"]
        ].fillna(0)
    )
    correlation = customer_features.corr()

    monthly_transactions = transactions.set_index("TransactionDate").resample("ME").agg(
        TransactionCount=("TransactionID", "count"),
        AverageAmount=("Amount", "mean"),
    )
    monthly_social = social.set_index("InteractionDate").resample("ME").agg(
        InteractionCount=("InteractionID", "count")
    )
    summary: dict[str, object] = {
        "data_quality": data_quality,
        "transaction_states": {
            "Valid numeric amounts": int(transactions["Amount"].notna().sum()),
            "Unresolved Free labels": int(transactions["IsFreeLabel"].sum()),
            "Preserved negative amounts": int(transactions["IsNegativeAmount"].sum()),
            "Source-missing amounts imputed": int(
                transactions["WasAmountImputed"].sum()
            ),
            "Genuine numeric zero amounts": int(transactions["Amount"].eq(0).sum()),
        },
        "category_frequencies": {
            "IncomeLevel": demographics["IncomeLevel"].value_counts().to_dict(),
            "ProductCategory": transactions["ProductCategory"].value_counts().to_dict(),
            "Sentiment": social["Sentiment"].value_counts().to_dict(),
        },
        "temporal_peaks": {
            "Transaction volume month": str(
                monthly_transactions["TransactionCount"].idxmax().date()
            ),
            "Transaction volume": int(monthly_transactions["TransactionCount"].max()),
            "Average amount month": str(
                monthly_transactions["AverageAmount"].idxmax().date()
            ),
            "Average amount": float(monthly_transactions["AverageAmount"].max()),
            "Social activity month": str(
                monthly_social["InteractionCount"].idxmax().date()
            ),
            "Social interaction count": int(monthly_social["InteractionCount"].max()),
        },
    }
    return summary, statistics, outliers, correlation


def save_figure(filename: str) -> None:
    """Apply a consistent export policy to the current figure."""
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=180, bbox_inches="tight")
    plt.close()


def generate_figures(
    clean: dict[str, pd.DataFrame], correlation: pd.DataFrame
) -> None:
    """Export the final visual evidence used in the presentation."""
    FIGURE_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", context="notebook")
    demographics = clean["Demographics"]
    transactions = clean["Transactions"]
    social = clean["Social Media"]

    plt.figure(figsize=(8, 4.8))
    sns.histplot(demographics["Age"], bins=18, kde=True, color="#176B87")
    plt.title("Customer Age Distribution")
    plt.xlabel("Age")
    save_figure("01_customer_age_distribution.png")

    plt.figure(figsize=(8, 4.8))
    sns.histplot(transactions["Amount"].dropna(), bins=25, kde=True, color="#D95F59")
    plt.axvline(0, color="#202020", linewidth=1)
    plt.title("Transaction Amount Distribution")
    plt.xlabel("Signed transaction amount")
    save_figure("02_transaction_amount_distribution.png")

    plt.figure(figsize=(8, 4.8))
    order = transactions["ProductCategory"].value_counts().index
    sns.countplot(data=transactions, y="ProductCategory", order=order, color="#E6A15C")
    plt.title("Transactions by Product Category")
    plt.xlabel("Transactions")
    plt.ylabel("")
    save_figure("03_product_category_frequency.png")

    plt.figure(figsize=(7.4, 5.8))
    sns.heatmap(correlation, annot=True, fmt=".3f", cmap="vlag", center=0)
    plt.title("Customer-Level Feature Correlations")
    save_figure("04_customer_feature_correlations.png")

    monthly_transactions = transactions.set_index("TransactionDate").resample("ME").agg(
        TransactionCount=("TransactionID", "count"),
        AverageAmount=("Amount", "mean"),
    )
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    axes[0].plot(monthly_transactions.index, monthly_transactions["TransactionCount"], color="#176B87", marker="o")
    axes[0].set_title("Monthly Transaction Volume")
    axes[0].set_ylabel("Transactions")
    axes[1].plot(monthly_transactions.index, monthly_transactions["AverageAmount"], color="#D95F59", marker="o")
    axes[1].set_title("Monthly Average Signed Amount")
    axes[1].set_ylabel("Average amount")
    save_figure("05_transaction_trends.png")

    monthly_social = social.set_index("InteractionDate").resample("ME").size()
    plt.figure(figsize=(9, 4.8))
    plt.plot(monthly_social.index, monthly_social.values, color="#3B7A57", marker="o")
    plt.title("Monthly Social Media Activity")
    plt.ylabel("Interactions")
    plt.xlabel("")
    save_figure("06_social_activity_trend.png")

    states = pd.Series(
        {
            "Free unresolved": int(transactions["IsFreeLabel"].sum()),
            "Negative preserved": int(transactions["IsNegativeAmount"].sum()),
            "Missing imputed": int(transactions["WasAmountImputed"].sum()),
            "Numeric zero": int(transactions["Amount"].eq(0).sum()),
        }
    )
    plt.figure(figsize=(8, 4.8))
    ax = sns.barplot(x=states.values, y=states.index, hue=states.index, palette="Set2", legend=False)
    for container in ax.containers:
        ax.bar_label(container, padding=3)
    plt.title("Preserved Transaction Data-Quality States")
    plt.xlabel("Records")
    plt.ylabel("")
    save_figure("07_transaction_quality_states.png")


def write_evidence(
    summary: dict[str, object],
    statistics: pd.DataFrame,
    outliers: pd.DataFrame,
    correlation: pd.DataFrame,
) -> None:
    """Write human-readable and machine-readable supporting evidence."""
    EVIDENCE_DIR.mkdir(exist_ok=True)
    with (EVIDENCE_DIR / "analysis_summary.json").open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
    statistics.to_csv(EVIDENCE_DIR / "descriptive_statistics.csv")
    outliers.to_csv(EVIDENCE_DIR / "outlier_summary.csv")
    correlation.to_csv(EVIDENCE_DIR / "correlation_matrix.csv")


def main() -> None:
    raw, clean = load_data()
    validate_data(raw, clean)
    summary, statistics, outliers, correlation = build_evidence(raw, clean)
    write_evidence(summary, statistics, outliers, correlation)
    generate_figures(clean, correlation)
    print("PASS: datasets validated; evidence and figures generated.")


if __name__ == "__main__":
    main()