import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Care Transition Efficiency & Placement Outcome Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    .kpi-title { font-size: 0.85rem; opacity: 0.85; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; }
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        border-left: 4px solid #667eea;
        padding-left: 0.6rem;
        margin: 1.2rem 0 0.8rem;
    }
    .insight-box {
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #2c5282;
        font-size: 0.92rem;
    }
    .alert-box {
        background: #fff5f5;
        border-left: 4px solid #e53e3e;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #742a2a;
        font-size: 0.92rem;
    }
    .stMetric > div { background: #f7fafc; border-radius: 8px; padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading & Cleaning ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df = df.dropna(subset=["Date"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Children in HHS Care"] = (
        df["Children in HHS Care"].astype(str)
        .str.replace(",", "").str.strip()
    )
    df["Children in HHS Care"] = pd.to_numeric(df["Children in HHS Care"], errors="coerce")
    df.columns = ["Date", "CBP_Apprehended", "CBP_Custody", "CBP_Transferred", "HHS_Care", "HHS_Discharged"]
    df = df.sort_values("Date").reset_index(drop=True)
    df = df.dropna()

    # Derived KPI metrics
    df["Transfer_Efficiency_Ratio"] = (df["CBP_Transferred"] / df["CBP_Apprehended"].replace(0, np.nan)).round(3)
    df["Discharge_Effectiveness_Index"] = (df["HHS_Discharged"] / df["HHS_Care"].replace(0, np.nan)).round(4)
    df["Pipeline_Throughput_Rate"] = (df["CBP_Transferred"] / (df["CBP_Custody"] + 1)).round(3)
    df["Backlog_Accumulation_Rate"] = (df["HHS_Care"] - df["HHS_Discharged"]).round(0)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Date"].dt.year
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["IsWeekend"] = df["Date"].dt.dayofweek >= 5
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Flag_of_the_United_States_%28DoS_ECA_Color_Standard%29.svg/320px-Flag_of_the_United_States_%28DoS_ECA_Color_Standard%29.svg.png", width=60)
    st.markdown("###  UAC Analytics Dashboard")
    st.caption("HHS Unaccompanied Alien Children Program")
    st.divider()

    st.markdown("** Date Range Filter**")
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input("Select Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    st.markdown("** Metric Toggles**")
    show_transfer = st.toggle("Transfer Efficiency Ratio", value=True)
    show_discharge = st.toggle("Discharge Effectiveness Index", value=True)
    show_throughput = st.toggle("Pipeline Throughput Rate", value=True)
    show_backlog = st.toggle("Backlog Accumulation Rate", value=True)

    st.divider()
    st.markdown("**⚠️ Alert Threshold**")
    backlog_threshold = st.slider("Backlog Alert Level", 0, 5000, 2000, 100)

    st.divider()
    st.caption("Data: HHS UAC Program | Jan 2023 – Dec 2025")

# ── Filter data ───────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = df["Date"].min(), df["Date"].max()

fdf = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header"> Care Transition Efficiency & Placement Outcome Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">HHS Unaccompanied Alien Children (UAC) Program — Process Efficiency & Outcome Dashboard</div>', unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric(" Records", f"{len(fdf):,}", help="Total daily records in selected range")
with k2:
    ter = fdf["Transfer_Efficiency_Ratio"].mean()
    st.metric(" Transfer Efficiency", f"{ter:.1%}", help="CBP→HHS transfers / apprehensions")
with k3:
    dei = fdf["Discharge_Effectiveness_Index"].mean()
    st.metric(" Discharge Effectiveness", f"{dei:.2%}", help="Discharges / HHS Care load")
with k4:
    ptr = fdf["Pipeline_Throughput_Rate"].mean()
    st.metric(" Pipeline Throughput", f"{ptr:.2f}", help="Transfers per CBP custody slot")
with k5:
    avg_backlog = fdf["Backlog_Accumulation_Rate"].mean()
    st.metric(" Avg Net Backlog/Day", f"{avg_backlog:,.0f}", help="HHS Care - Discharges")

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([" Care Pipeline Flow", " Transfer & Discharge Efficiency", " Bottleneck Detection", " Outcome Trend Analysis", " Raw Data"])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — Care Pipeline Flow
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Daily Care Pipeline — CBP → HHS → Sponsor Placement</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["CBP_Apprehended"], name="CBP Apprehended", line=dict(color="#e53e3e", width=1.5), fill="tozeroy", fillcolor="rgba(229,62,62,0.08)"))
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["CBP_Custody"], name="In CBP Custody", line=dict(color="#dd6b20", width=1.5)))
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["CBP_Transferred"], name="Transferred to HHS", line=dict(color="#3182ce", width=1.5)))
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["HHS_Care"], name="In HHS Care", line=dict(color="#38a169", width=2), fill="tozeroy", fillcolor="rgba(56,161,105,0.06)"))
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["HHS_Discharged"], name="Discharged (Sponsor)", line=dict(color="#805ad5", width=1.5, dash="dot")))
    fig.update_layout(height=400, hovermode="x unified", legend=dict(orientation="h", y=-0.2), xaxis_title="Date", yaxis_title="Children Count", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Monthly Average — Pipeline Stages</div>', unsafe_allow_html=True)
        monthly = fdf.groupby("Month")[["CBP_Apprehended", "CBP_Transferred", "HHS_Care", "HHS_Discharged"]].mean().reset_index()
        fig2 = px.bar(monthly.tail(18), x="Month", y=["CBP_Apprehended", "CBP_Transferred", "HHS_Care", "HHS_Discharged"],
                      barmode="group", color_discrete_sequence=["#e53e3e", "#3182ce", "#38a169", "#805ad5"],
                      labels={"value": "Avg Children", "variable": "Stage"})
        fig2.update_layout(height=320, xaxis_tickangle=-45, template="plotly_white", legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Pipeline Flow Funnel (Avg Daily)</div>', unsafe_allow_html=True)
        funnel_vals = [fdf["CBP_Apprehended"].mean(), fdf["CBP_Custody"].mean(),
                       fdf["CBP_Transferred"].mean(), fdf["HHS_Care"].mean(), fdf["HHS_Discharged"].mean()]
        funnel_labels = ["Apprehended", "CBP Custody", "Transferred to HHS", "In HHS Care", "Discharged to Sponsor"]
        fig3 = go.Figure(go.Funnel(y=funnel_labels, x=funnel_vals,
                                    marker=dict(color=["#e53e3e", "#dd6b20", "#3182ce", "#38a169", "#805ad5"])))
        fig3.update_layout(height=320, template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="insight-box"> <b>Insight:</b> The HHS Care load is significantly larger than daily discharges, indicating a sustained backlog. The pipeline funnel shows a large drop-off between "In HHS Care" and "Discharged to Sponsor" — the most critical bottleneck stage.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2 — Transfer & Discharge Efficiency
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">KPI Trend Lines — Efficiency Metrics Over Time</div>', unsafe_allow_html=True)

    active_metrics = []
    if show_transfer: active_metrics.append(("Transfer_Efficiency_Ratio", "Transfer Efficiency Ratio", "#3182ce"))
    if show_discharge: active_metrics.append(("Discharge_Effectiveness_Index", "Discharge Effectiveness Index", "#38a169"))
    if show_throughput: active_metrics.append(("Pipeline_Throughput_Rate", "Pipeline Throughput Rate", "#dd6b20"))

    if active_metrics:
        fig4 = go.Figure()
        for col, label, color in active_metrics:
            rolling = fdf[col].rolling(7, min_periods=1).mean()
            fig4.add_trace(go.Scatter(x=fdf["Date"], y=rolling, name=f"{label} (7-day avg)", line=dict(color=color, width=2)))
        fig4.update_layout(height=350, hovermode="x unified", template="plotly_white",
                           xaxis_title="Date", yaxis_title="Ratio / Index",
                           legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Enable at least one metric toggle in the sidebar.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Weekday vs Weekend Transfer Efficiency</div>', unsafe_allow_html=True)
        day_grp = fdf.groupby("DayOfWeek")["Transfer_Efficiency_Ratio"].mean().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).reset_index()
        fig5 = px.bar(day_grp, x="DayOfWeek", y="Transfer_Efficiency_Ratio",
                      color="Transfer_Efficiency_Ratio", color_continuous_scale="Blues",
                      labels={"Transfer_Efficiency_Ratio": "Avg Transfer Efficiency"})
        fig5.update_layout(height=300, template="plotly_white", showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Yearly Discharge Effectiveness Comparison</div>', unsafe_allow_html=True)
        year_grp = fdf.groupby("Year")[["Transfer_Efficiency_Ratio", "Discharge_Effectiveness_Index"]].mean().reset_index()
        fig6 = px.bar(year_grp, x="Year", y=["Transfer_Efficiency_Ratio", "Discharge_Effectiveness_Index"],
                      barmode="group", color_discrete_sequence=["#3182ce", "#38a169"],
                      labels={"value": "Ratio", "variable": "Metric"})
        fig6.update_layout(height=300, template="plotly_white", legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown('<div class="insight-box"> <b>Insight:</b> Transfer efficiency tends to dip on weekends, confirming that operational capacity is lower outside working days. Discharge effectiveness shows year-on-year improvement, suggesting better sponsor placement workflows over time.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3 — Bottleneck Detection
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Backlog Accumulation Rate Over Time</div>', unsafe_allow_html=True)

    if show_backlog:
        fdf["Backlog_7day"] = fdf["Backlog_Accumulation_Rate"].rolling(7, min_periods=1).mean()
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Backlog_7day"], name="Net Backlog (7-day avg)",
                                   line=dict(color="#e53e3e", width=2), fill="tozeroy", fillcolor="rgba(229,62,62,0.1)"))
        fig7.add_hline(y=backlog_threshold, line_dash="dash", line_color="orange",
                       annotation_text=f"Alert Threshold: {backlog_threshold:,}", annotation_position="top left")
        fig7.update_layout(height=350, template="plotly_white", xaxis_title="Date",
                           yaxis_title="Net Backlog (HHS Care - Discharged)", hovermode="x unified")
        st.plotly_chart(fig7, use_container_width=True)

        alert_days = fdf[fdf["Backlog_Accumulation_Rate"] > backlog_threshold]
        if len(alert_days) > 0:
            st.markdown(f'<div class="alert-box">⚠️ <b>Alert:</b> Backlog exceeded threshold ({backlog_threshold:,}) on <b>{len(alert_days)} days</b> in the selected period. Peak backlog: <b>{fdf["Backlog_Accumulation_Rate"].max():,.0f}</b></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Monthly Inflow vs Outflow</div>', unsafe_allow_html=True)
        monthly_flow = fdf.groupby("Month")[["CBP_Apprehended", "HHS_Discharged"]].sum().reset_index().tail(18)
        fig8 = go.Figure()
        fig8.add_trace(go.Bar(x=monthly_flow["Month"], y=monthly_flow["CBP_Apprehended"], name="Inflow (Apprehended)", marker_color="#e53e3e"))
        fig8.add_trace(go.Bar(x=monthly_flow["Month"], y=monthly_flow["HHS_Discharged"], name="Outflow (Discharged)", marker_color="#38a169"))
        fig8.update_layout(height=320, barmode="group", template="plotly_white",
                           xaxis_tickangle=-45, legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">HHS Care Load — Distribution</div>', unsafe_allow_html=True)
        fig9 = px.histogram(fdf, x="HHS_Care", nbins=40, color_discrete_sequence=["#667eea"],
                            labels={"HHS_Care": "Children in HHS Care"})
        fig9.update_layout(height=320, template="plotly_white")
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown('<div class="section-title">Stagnation Periods — Prolonged High Backlog Detection</div>', unsafe_allow_html=True)
    fdf["High_Backlog"] = fdf["Backlog_Accumulation_Rate"] > backlog_threshold
    stagnation = fdf[fdf["High_Backlog"]][["Date", "HHS_Care", "HHS_Discharged", "Backlog_Accumulation_Rate"]].head(10)
    if len(stagnation) > 0:
        st.dataframe(stagnation.rename(columns={
            "Backlog_Accumulation_Rate": "Net Backlog",
            "HHS_Care": "In HHS Care",
            "HHS_Discharged": "Discharged"
        }).style.background_gradient(subset=["Net Backlog"], cmap="Reds"), use_container_width=True)
    else:
        st.success("No stagnation periods detected above the current threshold.")

    st.markdown('<div class="insight-box"> <b>Insight:</b> Inflow consistently outpaces outflow in peak months. The backlog analysis identifies specific periods where the system was under maximum stress — critical information for resource allocation planning.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4 — Outcome Trend Analysis
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Month-over-Month Placement (Discharge) Trends</div>', unsafe_allow_html=True)

    monthly_out = fdf.groupby("Month")["HHS_Discharged"].agg(["sum", "mean", "std"]).reset_index().tail(24)
    fig10 = go.Figure()
    fig10.add_trace(go.Scatter(x=monthly_out["Month"], y=monthly_out["sum"], name="Total Discharges",
                                line=dict(color="#38a169", width=2), mode="lines+markers"))
    fig10.add_trace(go.Scatter(x=monthly_out["Month"], y=monthly_out["mean"], name="Daily Avg",
                                line=dict(color="#3182ce", width=1.5, dash="dot")))
    fig10.update_layout(height=320, template="plotly_white", xaxis_tickangle=-45,
                        xaxis_title="Month", yaxis_title="Children Discharged",
                        legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig10, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Outcome Stability Score — Variability in Discharges</div>', unsafe_allow_html=True)
        monthly_std = fdf.groupby("Month")["HHS_Discharged"].std().reset_index().tail(18)
        monthly_std.columns = ["Month", "Discharge_Variability"]
        fig11 = px.area(monthly_std, x="Month", y="Discharge_Variability",
                        color_discrete_sequence=["#805ad5"],
                        labels={"Discharge_Variability": "Std Dev of Daily Discharges"})
        fig11.update_layout(height=300, template="plotly_white", xaxis_tickangle=-45)
        st.plotly_chart(fig11, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Correlation Matrix — Pipeline Variables</div>', unsafe_allow_html=True)
        corr_cols = ["CBP_Apprehended", "CBP_Custody", "CBP_Transferred", "HHS_Care", "HHS_Discharged"]
        corr = fdf[corr_cols].corr()
        fig12 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                          zmin=-1, zmax=1, aspect="auto")
        fig12.update_layout(height=300, template="plotly_white")
        st.plotly_chart(fig12, use_container_width=True)

    st.markdown('<div class="section-title">All KPI Summary Table (Monthly)</div>', unsafe_allow_html=True)
    kpi_monthly = fdf.groupby("Month").agg(
        Avg_Transfer_Efficiency=("Transfer_Efficiency_Ratio", "mean"),
        Avg_Discharge_Effectiveness=("Discharge_Effectiveness_Index", "mean"),
        Avg_Pipeline_Throughput=("Pipeline_Throughput_Rate", "mean"),
        Total_Discharged=("HHS_Discharged", "sum"),
        Avg_HHS_Care=("HHS_Care", "mean"),
        Avg_Backlog=("Backlog_Accumulation_Rate", "mean")
    ).reset_index().tail(12)

    st.dataframe(
        kpi_monthly.style.format({
            "Avg_Transfer_Efficiency": "{:.1%}",
            "Avg_Discharge_Effectiveness": "{:.2%}",
            "Avg_Pipeline_Throughput": "{:.3f}",
            "Total_Discharged": "{:,.0f}",
            "Avg_HHS_Care": "{:,.0f}",
            "Avg_Backlog": "{:,.0f}"
        }).background_gradient(subset=["Avg_Discharge_Effectiveness"], cmap="Greens"),
        use_container_width=True
    )

    st.markdown('<div class="insight-box"> <b>Insight:</b> High discharge variability in certain months points to inconsistent reunification workflows. Periods of low variability with high volume represent best-practice windows that should be studied and replicated.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 5 — Raw Data
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Filtered Dataset</div>', unsafe_allow_html=True)
    st.dataframe(fdf[["Date", "CBP_Apprehended", "CBP_Custody", "CBP_Transferred",
                        "HHS_Care", "HHS_Discharged", "Transfer_Efficiency_Ratio",
                        "Discharge_Effectiveness_Index", "Pipeline_Throughput_Rate",
                        "Backlog_Accumulation_Rate"]].style.format({
        "Transfer_Efficiency_Ratio": "{:.3f}",
        "Discharge_Effectiveness_Index": "{:.4f}",
        "Pipeline_Throughput_Rate": "{:.3f}",
        "Backlog_Accumulation_Rate": "{:,.0f}"
    }), use_container_width=True, height=400)

    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Processed Data as CSV", data=csv, file_name="uac_processed_data.csv", mime="text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(" UAC Care Transition Efficiency Dashboard | Data: HHS Unaccompanied Alien Children Program | Built with Streamlit & Plotly")
