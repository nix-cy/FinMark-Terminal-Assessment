# MO-IT162 Terminal Assessment: FinMark ML Solution

**Section:** BSIT-H3101  
**Team:** Group 6

**Official team members:**
- Danica Mae Tugare
- Christian Cristobal
- Pg Amir Nur Mohammad Urbano

## Submission Contents

| Resource | Purpose |
|---|---|
| `terminal_ml_solution_project.ipynb` | Final preprocessing, conflict verification, cleaning, EDA, and validation notebook |
| `Final_ml_visualizations.ipynb` | Final numerical analysis, correlations, outlier screening, visualizations, and modeling recommendations |
| `finmark_analysis.py` | Standalone validator and evidence/figure generator |
| `data/raw/` | Three unchanged contaminated course-project CSVs |
| `data/cleaned/` | Three finalized cleaned CSVs |
| `figures/` | Seven exported PNG visualizations |
| `evidence/` | JSON/CSV numerical evidence used by the report and presentation |
| `presentation/` | Final team-authored Canva PowerPoint, corrected and validated against the project evidence |
| `VALIDATION_REPORT.md` | Criterion-by-criterion final quality review |

## Data Provenance

The three contaminated CSVs were supplied as the FinMark MFML course-project datasets and are preserved unchanged in `data/raw/`. The official project website is [FinMark Corporation](https://sites.google.com/mmdc.mcl.edu.ph/finmarkcorp/home). The repository files, raw dimensions, and quality audit provide the reproducible data record used by this submission.

## Reproduce the Results

From this folder:

```powershell
python -m pip install -r requirements.txt
python finmark_analysis.py
```

Then open and run the notebooks from top to bottom with Python 3.12 or another compatible Python 3 environment. Both notebooks resolve paths whether VS Code starts the kernel in the repository root or this folder.

## Verified Final State

- Raw datasets: 3,200 rows each.
- Cleaned datasets: 3,000 rows each with unique business IDs.
- Business-key conflicts: 23 demographic, 15 transaction, and 20 social IDs, all verified as original/appended contamination pairs.
- Transaction states: 29 unresolved `Free` labels, 34 preserved signed negatives, 282 source-missing median imputations, and 29 genuine numeric zeros.
- IQR screening: 0 age outliers and 0 transaction-amount outliers under the 1.5 x IQR rule.
- Key customer-level correlations: `TotalSpend`/`TransactionCount` = 0.863 and `TotalSpend`/`AverageAmount` = 0.606.

## Final Attribution Check

The technical package is complete and validated. The verified Group 6 roster and official FinMark project URL are included in the notebooks, documentation, and final Canva-authored presentation. The 15-slide PowerPoint was programmatically checked and rendered through Microsoft PowerPoint without errors.