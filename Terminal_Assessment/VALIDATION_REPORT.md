# Terminal Assessment Validation Report

## Milestone 3 Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Incorporate professor feedback and team refinements | Pass | Notebooks now show record counts, source status, before/after cleaning evidence, category frequencies, correlation coefficients, outlier counts, and quantitative interpretations. |
| Resolve cleaning inconsistencies | Pass | Conflict retention is evidence-based; negative, `Free`, imputed, and zero transaction states remain distinct. |
| Finalize team-approved files with clear names | Pass | Required notebook names and the required presentation title are used. |
| Create `Terminal_Assessment` repository folder | Pass | All final resources are organized under this folder. |
| Include notebooks and source code | Pass | Two final notebooks plus the standalone `finmark_analysis.py` validator are included. |
| Include datasets | Pass | Three raw and three cleaned CSVs are organized under `data/`. |
| Include visualizations | Pass | Seven standalone PNGs plus executed notebook figures are included. |
| Include presentation materials | Pass | The team-authored Canva PowerPoint is included as the single authoritative presentation. |
| Include supporting resources | Pass | README, requirements, evidence JSON/CSVs, and this validation report are included. |
| Remove duplicates/outdated files from final folder | Pass | The folder contains one authoritative copy of each required dataset and final notebook. |
| Ensure files open and contents are accessible | Pass | Python source has no diagnostics; both notebooks execute successfully; CSVs and images were programmatically validated; all 15 PowerPoint slides rendered without errors. |
| Use meaningful commit message | Pass | Committed as `Finalize Milestone 3 terminal assessment package` and pushed to `origin/main`. |

## Quantitative Validation

| Dataset | Raw rows | Clean rows | Exact duplicates before | Duplicate IDs before | Conflicting IDs | Duplicate IDs after |
|---|---:|---:|---:|---:|---:|---:|
| Customer demographics | 3,200 | 3,000 | 177 | 200 | 23 | 0 |
| Customer transactions | 3,200 | 3,000 | 185 | 200 | 15 | 0 |
| Social interactions | 3,200 | 3,000 | 180 | 200 | 20 | 0 |

Every non-identical business-key conflict has one row in the original 3,000-record region and one modified row in the appended 200-record contamination region. No other conflict pattern was found. Original records are retained on that dataset-specific evidence, not through an unexplained `keep='first'` assumption.

## Analytical Consistency

- Average amount stays undefined for customers without transactions; it is not zero-filled.
- Total spend, transaction count, and social-interaction count are zero-filled when absent because they represent event totals.
- `Free` is not converted to numeric zero.
- Signed negative amounts are not discarded or imputed.
- Correlations use customer-level aggregates joined by `CustomerID`, not row positions.
- Temporal variation is reported without claiming seasonality.
- IQR results are treated as screening evidence, not automatic deletion rules.

## Confirmed Attribution and Source

The verified Group 6 members are Danica Mae Tugare, Christian Cristobal, and Pg Amir Nur Mohammad Urbano. The official project website supplied by the team is [FinMark Corporation](https://sites.google.com/mmdc.mcl.edu.ph/finmarkcorp/home). The raw CSVs used in the analysis remain preserved unchanged under `data/raw/`.

## Presentation Validation

The team-authored Canva presentation was reconciled with the final evidence before inclusion. Unsupported negative-amount handling was corrected, the customer-level correlations were updated to 0.863 and 0.606, exact IQR outlier counts were added, the official roster and source were included, and a professor-feedback resolution slide was added. The final 15-slide deck opens and renders successfully in Microsoft PowerPoint with no clipping or overlap.