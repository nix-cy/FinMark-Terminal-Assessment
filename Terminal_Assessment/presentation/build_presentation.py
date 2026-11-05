"""Build the final FinMark terminal-assessment PowerPoint deck."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


BASE_DIR = Path(__file__).resolve().parents[1]
FIGURE_DIR = BASE_DIR / "figures"
OUTPUT = Path(__file__).with_name(
    "MO-IT162 Terminal Assessment - ML Solution - BSIT- H3101 - Group 6.pptx"
)

INK = RGBColor(35, 38, 42)
TEAL = RGBColor(23, 107, 135)
RED = RGBColor(201, 72, 81)
ORANGE = RGBColor(230, 161, 92)
PAPER = RGBColor(247, 248, 246)
MUTED = RGBColor(102, 110, 117)


def add_background(slide, accent=TEAL):
    background = slide.background.fill
    background.solid()
    background.fore_color.rgb = PAPER
    line = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    line.fill.solid()
    line.fill.fore_color.rgb = accent
    line.line.fill.background()


def add_title(slide, title, number, accent=TEAL):
    add_background(slide, accent)
    box = slide.shapes.add_textbox(Inches(0.65), Inches(0.35), Inches(11.9), Inches(0.65))
    paragraph = box.text_frame.paragraphs[0]
    paragraph.text = title
    paragraph.font.name = "Aptos Display"
    paragraph.font.size = Pt(27)
    paragraph.font.bold = True
    paragraph.font.color.rgb = INK
    footer = slide.shapes.add_textbox(Inches(12.25), Inches(7.05), Inches(0.5), Inches(0.25))
    footer_paragraph = footer.text_frame.paragraphs[0]
    footer_paragraph.text = str(number)
    footer_paragraph.alignment = PP_ALIGN.RIGHT
    footer_paragraph.font.name = "Aptos"
    footer_paragraph.font.size = Pt(9)
    footer_paragraph.font.color.rgb = MUTED


def add_bullets(slide, bullets, left=0.8, top=1.35, width=5.8, height=5.3, size=20):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    frame.clear()
    for index, text in enumerate(bullets):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = text
        paragraph.level = 0
        paragraph.font.name = "Aptos"
        paragraph.font.size = Pt(size)
        paragraph.font.color.rgb = INK
        paragraph.space_after = Pt(12)


def add_image(slide, name, left, top, width):
    slide.shapes.add_picture(
        str(FIGURE_DIR / name), Inches(left), Inches(top), width=Inches(width)
    )


def add_metric(slide, value, label, left, top, color):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(2.7), Inches(1.3))
    frame = box.text_frame
    value_paragraph = frame.paragraphs[0]
    value_paragraph.text = value
    value_paragraph.font.name = "Aptos Display"
    value_paragraph.font.size = Pt(32)
    value_paragraph.font.bold = True
    value_paragraph.font.color.rgb = color
    label_paragraph = frame.add_paragraph()
    label_paragraph.text = label
    label_paragraph.font.name = "Aptos"
    label_paragraph.font.size = Pt(14)
    label_paragraph.font.color.rgb = MUTED


def build_deck():
    presentation = Presentation()
    presentation.slide_width = Inches(13.333)
    presentation.slide_height = Inches(7.5)
    blank = presentation.slide_layouts[6]

    slide = presentation.slides.add_slide(blank)
    add_background(slide, TEAL)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(2.5))
    frame = title_box.text_frame
    title = frame.paragraphs[0]
    title.text = "MO-IT162 Terminal Assessment"
    title.font.name = "Aptos Display"
    title.font.size = Pt(38)
    title.font.bold = True
    title.font.color.rgb = INK
    subtitle = frame.add_paragraph()
    subtitle.text = "ML Solution | BSIT-H3101 | Group 6"
    subtitle.font.name = "Aptos"
    subtitle.font.size = Pt(24)
    subtitle.font.color.rgb = TEAL
    detail = frame.add_paragraph()
    detail.text = "FinMark preprocessing, exploratory analysis, and model-readiness review"
    detail.font.name = "Aptos"
    detail.font.size = Pt(17)
    detail.font.color.rgb = MUTED
    members = frame.add_paragraph()
    members.text = "Danica Mae Tugare | Christian Cristobal | Pg Amir Nur Mohammad Urbano"
    members.font.name = "Aptos"
    members.font.size = Pt(15)
    members.font.color.rgb = INK

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Business Goal and Data Architecture", 2)
    add_bullets(slide, [
        "Prepare reliable customer, transaction, and social features for segmentation and future predictive modeling.",
        "CustomerID connects all three datasets; TransactionID and InteractionID identify business events.",
        "Identifiers support joins and validation, not direct prediction.",
        "Audience: analysts, data scientists, marketing teams, and decision-makers.",
    ], width=11.6, size=22)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Source, Method, and Reproducibility", 3, ORANGE)
    add_bullets(slide, [
        "Course-provided FinMark MFML CSVs are preserved unchanged under data/raw.",
        "Official project website: sites.google.com/mmdc.mcl.edu.ph/finmarkcorp/home.",
        "Two executed notebooks contain cleaning, numerical analysis, visualizations, and interpretations.",
        "A standalone Python program regenerates validation evidence and seven final figures.",
        "JSON and CSV evidence files keep every reported value traceable.",
    ], width=11.6, size=21)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Cleaning Verification", 4, RED)
    add_metric(slide, "3,200 -> 3,000", "rows per dataset", 0.8, 1.35, TEAL)
    add_metric(slide, "0", "duplicate IDs after cleaning", 3.85, 1.35, RED)
    add_metric(slide, "23 / 15 / 20", "conflicting IDs verified", 6.9, 1.35, ORANGE)
    add_bullets(slide, [
        "Exact duplicate rows: 177 demographics, 185 transactions, 180 social.",
        "Each non-identical conflict was an original row plus a modified appended contamination row.",
        "Original-source retention is based on verified lineage, not blind row order.",
    ], left=0.8, top=3.0, width=11.4, height=3.2, size=20)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Preserving Transaction Meaning", 5, ORANGE)
    add_image(slide, "07_transaction_quality_states.png", 6.35, 1.25, 6.25)
    add_bullets(slide, [
        "29 Free labels remain unresolved numerically.",
        "34 negatives remain signed for refund/reversal review.",
        "282 source-missing values are median-imputed and flagged.",
        "29 genuine zeros remain distinct from Free.",
    ], left=0.7, top=1.4, width=5.3, size=19)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Descriptive Evidence", 6)
    add_image(slide, "01_customer_age_distribution.png", 0.65, 1.25, 5.9)
    add_image(slide, "02_transaction_amount_distribution.png", 6.78, 1.25, 5.9)
    add_bullets(slide, [
        "Age: mean 44.680, median/mode 45, SD 14.437, range 18-70.",
        "Amount: n=2,971, mean 491.931, median/mode 497.49, SD 283.658, signed range -100.00 to 999.86.",
    ], left=0.8, top=5.65, width=11.7, height=1.2, size=15)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Category Evidence", 7, ORANGE)
    add_image(slide, "03_product_category_frequency.png", 6.25, 1.2, 6.35)
    add_bullets(slide, [
        "Income: High 935, Low 918, Medium 863, Unknown 284.",
        "Product categories are relatively balanced; Clothing is largest at 568.",
        "Sentiment: Positive 898, Neutral 870, Negative 861, Unknown 308.",
        "Unknown and rare extreme classes remain visible.",
    ], left=0.7, top=1.4, width=5.2, size=18)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Customer-Level Relationships", 8, RED)
    add_image(slide, "04_customer_feature_correlations.png", 6.25, 1.15, 6.1)
    add_bullets(slide, [
        "TotalSpend / TransactionCount: r = 0.863.",
        "TotalSpend / AverageAmount: r = 0.606.",
        "Age and social volume have near-zero linear relationships with spending.",
        "Correlation is descriptive; related spending features may be redundant.",
    ], left=0.7, top=1.45, width=5.25, size=18)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Outliers and Time Trends", 9)
    add_image(slide, "05_transaction_trends.png", 6.15, 1.15, 6.45)
    add_bullets(slide, [
        "1.5 x IQR screen: 0 age and 0 amount outliers.",
        "Negative values can still be business-significant.",
        "Peak volume: May 2024, 149 transactions.",
        "Peak average amount: August 2023, 548.843.",
        "Observed time span is too short to claim seasonality.",
    ], left=0.7, top=1.35, width=5.1, size=17)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Modeling Recommendations", 10, ORANGE)
    add_bullets(slide, [
        "Retain missingness and amount-review flags; preserve Unknown as its own category.",
        "Scale numeric features for distance-based models and screen correlated spending features.",
        "Split customer-level models by CustomerID; use chronological validation for forecasting.",
        "Evaluate nonlinear effects despite near-zero simple correlations.",
        "Confirm Free and negative transaction meanings before production modeling.",
    ], width=11.6, size=21)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Professor Feedback Resolved", 11, RED)
    add_bullets(slide, [
        "Added record counts, source status, and explicit before/after evidence.",
        "Added category frequencies, correlation coefficients, outlier counts, and temporal peak values.",
        "Replaced unsupported duplicate and transaction assumptions with auditable decisions.",
        "Aligned analytical definitions across notebooks, evidence files, figures, and slides.",
        "Organized one authoritative final package under Terminal_Assessment.",
    ], width=11.6, size=21)

    slide = presentation.slides.add_slide(blank)
    add_title(slide, "Conclusion", 12)
    add_metric(slide, "3", "validated cleaned datasets", 1.0, 1.5, TEAL)
    add_metric(slide, "7", "exported final figures", 5.25, 1.5, RED)
    add_metric(slide, "2", "executed final notebooks", 9.2, 1.5, ORANGE)
    add_bullets(slide, [
        "The package is traceable, reproducible, analytically consistent, and ready for final team review and repository submission."
    ], left=1.0, top=4.2, width=11.2, height=1.5, size=24)

    presentation.save(OUTPUT)
    print(f"Created {OUTPUT.name} with {len(presentation.slides)} slides.")


if __name__ == "__main__":
    build_deck()