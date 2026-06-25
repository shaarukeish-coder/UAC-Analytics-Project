# Care Transition Efficiency & Placement Outcome Analytics
## Research Paper — EDA, Insights & Recommendations

**Program:** HHS Unaccompanied Alien Children (UAC) Program  
**Internship Domain:** Machine Learning / Healthcare Analytics  
**Organization:** Unified Mentor  
**Dataset:** HHS UAC Daily Program Data (Jan 2023 – Dec 2025)  
**Author:** Shaarukeish

---

## Abstract

This paper presents a comprehensive analytical study of the U.S. Department of Health and Human Services (HHS) Unaccompanied Alien Children (UAC) Program's care transition pipeline. Using 720 daily observations spanning January 2023 to December 2025, we evaluate process efficiency through derived Key Performance Indicators (KPIs), identify systemic bottlenecks, and propose data-driven recommendations for improving reunification timelines and placement outcomes. Our analysis reveals persistent backlogs, declining discharge rates in 2025, and significant weekday-weekend performance disparities.

---

## 1. Introduction

### 1.1 Background and Context

The UAC Program manages a multi-stage child welfare pipeline involving:
1. **Apprehension & CBP Custody** — Border apprehension and initial processing
2. **Transfer to HHS Care** — Handover from Customs and Border Protection to HHS
3. **Medical Screening, Sheltering & Case Management** — Active HHS custody
4. **Discharge & Reunification with a Vetted Sponsor** — Final placement outcome

From a humanitarian standpoint, the speed, continuity, and reliability of this pipeline are as critical as capacity. A child spending excessive time in institutional care faces elevated health, psychological, and developmental risks.

### 1.2 Problem Statement

While aggregate counts of children in custody are monitored by federal agencies, **process efficiency metrics are largely absent** from public reporting. Key unanswered questions include:

- How efficiently are children transferred from CBP to HHS?
- Are discharges keeping pace with inflows?
- When and where do care backlogs accumulate?
- Are placement outcomes improving or deteriorating over time?

Without structured transition analytics, system bottlenecks remain hidden within headline numbers.

### 1.3 Objectives

**Primary:**
- Measure efficiency of CBP → HHS transitions
- Evaluate discharge and sponsor placement outcomes
- Identify delays and process bottlenecks

**Secondary:**
- Support faster reunification through insight generation
- Improve case management workflows
- Inform policy-level process reforms

---

## 2. Dataset Description

| Column | Description |
|--------|-------------|
| Date | Reporting date (daily) |
| Children apprehended and placed in CBP custody | Daily intake volume |
| Children in CBP custody | Active CBP care load |
| Children transferred out of CBP custody | Flow into HHS system |
| Children in HHS Care | Active HHS care load |
| Children discharged from HHS Care | Successful sponsor placements |

**Dataset Summary:**
- **Total Records:** 720 daily observations
- **Date Range:** January 12, 2023 – December 21, 2025
- **Missing Values:** None (after date-based cleaning)
- **Data Quality:** One column ("Children in HHS Care") required comma removal for numeric parsing

---

## 3. Exploratory Data Analysis (EDA)

### 3.1 Descriptive Statistics

| Metric | Mean | Min | Max | Std Dev |
|--------|------|-----|-----|---------|
| CBP Apprehended (daily) | 93.5 | 0 | 333 | 72.6 |
| CBP Custody (daily) | ~45 | 0 | ~250 | — |
| CBP Transferred (daily) | 128.7 | 0 | ~300 | — |
| HHS Care (active load) | ~6,500 | 1,972 | 11,516 | — |
| HHS Discharged (daily) | 173.4 | 0 | 505 | 125.7 |

**Notable Observations:**
- Average daily **transfers (128.7) exceed apprehensions (93.5)**, indicating HHS is absorbing backlog from prior periods
- Average daily **discharges (173.4) exceed apprehensions**, yet the HHS active load remains very high — indicating structural multi-year backlogs
- HHS Care peaked at **11,516 children** and has since declined to near 2,000, suggesting capacity improvements or policy changes

### 3.2 Pipeline Flow Analysis

The care pipeline follows a flow model:

```
CBP Apprehension → CBP Custody → Transfer to HHS → HHS Care → Discharge/Sponsor
```

Monthly trend analysis reveals:
- **2023:** Highest inflow volumes, peaking mid-year, with strong discharge activity
- **2024:** Moderate inflow, moderate discharge, sustained backlog
- **2025:** Dramatically declining inflow AND discharge — HHS Care load drops sharply

### 3.3 Year-over-Year Comparison

| Year | Avg TER | Avg DEI | Avg PTR | Avg Daily Backlog | Avg Daily Discharge |
|------|---------|---------|---------|-------------------|---------------------|
| 2023 | 1.429 | 3.34% | 0.823 | 8,358 | 288.0 |
| 2024 | 1.484 | 2.90% | 0.780 | 6,837 | 206.0 |
| 2025 | 1.539 | 0.90% | 0.442 | 2,514 | 29.0 |

**Key finding:** While Transfer Efficiency improved year-over-year, Discharge Effectiveness fell dramatically in 2025, suggesting sponsor placement processes became severely constrained.

### 3.4 Correlation Analysis

| Variable Pair | Correlation |
|---------------|-------------|
| CBP Apprehended ↔ CBP Transferred | **0.888** (very strong) |
| HHS Care ↔ HHS Discharged | **0.921** (very strong) |
| CBP Apprehended ↔ HHS Care | 0.691 (strong) |
| CBP Transferred ↔ HHS Discharged | 0.657 (strong) |

**Interpretation:** Discharge activity is tightly coupled with the active HHS care load — a larger census drives more placements, suggesting a capacity-driven rather than demand-driven discharge model.

### 3.5 Weekday vs. Weekend Patterns

Transfer efficiency and discharge rates are measurably lower on **Saturdays and Sundays**, confirming that the pipeline is operationally constrained to business-day staffing patterns. This represents a structural inefficiency in child welfare operations.

---

## 4. Key Performance Indicators (KPIs)

### 4.1 Transfer Efficiency Ratio (TER)
**Formula:** `CBP_Transferred / CBP_Apprehended`  
**Overall Average:** 1.484  
**Interpretation:** On average, 1.48 children are transferred to HHS for every new apprehension. A ratio > 1.0 means HHS is absorbing accumulated backlog in addition to new cases. This is positive for clearance but indicates the system had a prior structural deficit.

### 4.2 Discharge Effectiveness Index (DEI)
**Formula:** `HHS_Discharged / HHS_Care`  
**Overall Average:** 2.37%  
**Interpretation:** On any given day, only ~2.37% of children in HHS care are discharged to sponsors. The **2025 collapse to 0.9%** is alarming — placement capacity essentially halved relative to the care population, despite the care load also declining.

### 4.3 Pipeline Throughput Rate (PTR)
**Formula:** `CBP_Transferred / (CBP_Custody + 1)`  
**Overall Average:** 0.681  
**Interpretation:** For every child in CBP custody, 0.68 are transferred out daily. A PTR close to or above 1.0 is optimal. The declining PTR from 0.82 in 2023 to 0.44 in 2025 suggests the CBP-to-HHS handoff is slowing, possibly due to reduced HHS capacity to accept transfers.

### 4.4 Backlog Accumulation Rate (BAR)
**Formula:** `HHS_Care - HHS_Discharged`  
**Overall Average:** 5,888 children/day in net backlog  
**Peak Backlog Day:** Net load > 11,000 children  
**Interpretation:** The system carries a persistent daily backlog of nearly 6,000 children on average. This represents children in institutional care beyond what is being resolved through sponsor placements — a direct humanitarian concern.

---

## 5. Bottleneck Analysis

### 5.1 Primary Bottleneck: HHS-to-Sponsor Discharge Stage

The most critical bottleneck in the pipeline is **Stage 4 (Discharge to Sponsor)**. Despite the system successfully moving children from CBP to HHS, the final reunification step demonstrates:
- Lowest throughput relative to population size
- Highest variability month-over-month
- Steepest decline in 2025

### 5.2 Secondary Bottleneck: Weekend Operational Gaps

Weekend data shows consistent drops in both transfer and discharge rates. For a child welfare system, a 2-day weekly operational reduction compounds to significant additional detention time.

### 5.3 Seasonal Stagnation Periods

Peak backlog accumulation periods were identified in:
- **Mid-2023:** Highest absolute HHS care load (>11,000 children)
- **Early 2024:** Sustained high backlog despite moderate inflows
- **Late 2025:** Low absolute numbers but worst-ever discharge efficiency

### 5.4 Funnel Drop-off Summary

| Pipeline Stage | Avg Daily Volume | Drop-off |
|----------------|-----------------|----------|
| Apprehended | 93.5 | — |
| In CBP Custody | ~45 | –52% |
| Transferred to HHS | 128.7 | +38% (clearance) |
| In HHS Care | ~6,500 | Cumulative load |
| Discharged to Sponsor | 173.4 | 2.37% daily clearance rate |

---

## 6. Insights

1. **The pipeline has a structural clearance deficit.** Even with daily discharges exceeding daily apprehensions, the HHS care load remains orders of magnitude higher — a legacy of years of accumulated backlog.

2. **2025 signals a discharge crisis.** The Discharge Effectiveness Index dropped from 3.34% (2023) to 0.90% (2025), indicating sponsor placement capacity was severely constrained, creating disproportionate institutional detention despite lower inflows.

3. **Transfers are efficient; placements are not.** The CBP → HHS handoff (TER > 1.0) works well. The HHS → Sponsor stage (DEI < 3%) is the system's critical failure point.

4. **Weekend gaps are a policy-correctable inefficiency.** The data clearly shows lower performance on Saturdays and Sundays, which could be addressed through weekend case management staffing.

5. **HHS care load and discharge volume are tightly correlated (r = 0.921)**, suggesting the system is self-regulating to capacity — not demand. When care load drops, discharges drop proportionally rather than accelerating to clear the backlog.

6. **The 2023–2025 decline in the HHS census** (from ~11,500 to ~2,000) is a major positive trend, though whether this reflects improved placements, policy changes, or reduced inflow requires policy-level investigation.

---

## 7. Recommendations

### 7.1 Operational Recommendations

**R1: Implement Weekend Duty Rosters for Case Workers**  
The data shows measurable performance dips on weekends. Deploying a minimum viable weekend team for case management and sponsor vetting could reduce average length of stay.

**R2: Set DEI Alert Thresholds**  
A daily Discharge Effectiveness Index below 1.5% should trigger an operational review. The 2025 collapse to 0.9% likely went undetected until the cumulative impact was visible.

**R3: Create a Pipeline Throughput Dashboard**  
Real-time visibility into TER, DEI, PTR, and BAR enables proactive intervention. The Streamlit dashboard created in this project provides a prototype for this system.

### 7.2 Policy Recommendations

**R4: Sponsor Matching Capacity Must Scale Independently of Care Census**  
The high correlation between HHS care load and discharge volume suggests a passive, capacity-driven model. Active sponsor outreach and vetting pipelines should operate independently.

**R5: Investigate the 2025 Discharge Collapse**  
The 97% decline in average daily discharges (from 288 in 2023 to 29 in 2025) demands a root-cause investigation — whether policy, funding, staffing, or legal changes are responsible must be understood to prevent recurrence.

**R6: Publish Process Efficiency Metrics Alongside Capacity Metrics**  
Current public reporting focuses on census counts. Adding TER, DEI, and PTR to official HHS reporting would improve public accountability and enable early warning detection.

### 7.3 Data Recommendations

**R7: Add Case-Level Data for Longitudinal Analysis**  
Aggregate daily data limits root-cause analysis. Individual case tracking (anonymized) would enable Length-of-Stay modeling, outcome prediction, and cohort analysis.

**R8: Include Reason Codes for Non-Placement Days**  
Understanding why discharge rates drop on specific days (legal holds, sponsor rejections, capacity, etc.) would enable targeted interventions.

---

## 8. Conclusion

This analysis reframes the UAC dataset from a capacity monitoring lens to a **process efficiency and outcome evaluation lens**. By analyzing how effectively children move through the care pipeline, it provides actionable insights for improving reunification timelines, reducing delays, and strengthening child welfare outcomes.

The five KPIs developed — Transfer Efficiency Ratio, Discharge Effectiveness Index, Pipeline Throughput Rate, Backlog Accumulation Rate, and Outcome Stability Score — provide a comprehensive framework for ongoing process monitoring. The Streamlit dashboard built as part of this project enables real-time application of these metrics by program administrators.

Key findings confirm that while the intake-to-HHS transfer stage is functioning efficiently, the HHS-to-sponsor discharge stage represents the system's critical failure point — and the 2025 data shows this failure intensifying precisely when the care census was at its lowest, pointing to structural rather than capacity-driven causes.

---

## References

1. U.S. Department of Health and Human Services — Office of Refugee Resettlement (ORR), UAC Program Data
2. U.S. Customs and Border Protection (CBP) — Unaccompanied Children Statistics
3. Unified Mentor Technical Documentation — Care Transition Efficiency & Placement Outcome Analytics Project Brief

---

*Submitted as part of the Machine Learning Internship — Unified Mentor | Healthcare Analytics Domain*
