# Care Transition Efficiency & Placement Outcome Analytics
## HHS Unaccompanied Alien Children (UAC) Program

---

## 📁 Project Structure

```
UAC_Analytics_Project/
├── app.py                  ← Streamlit Dashboard (main file)
├── dataset.csv             ← HHS UAC Dataset
├── research_paper.md       ← Full Research Paper (EDA + Insights)
├── executive_summary.md    ← Executive Summary for Stakeholders
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## 🚀 How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the dashboard
```bash
streamlit run app.py
```

### Step 3 — Open in browser
The dashboard will open automatically at: http://localhost:8501

---

## 📊 Dashboard Features

| Tab | Contents |
|-----|----------|
| 📈 Care Pipeline Flow | Daily pipeline stages, funnel chart, monthly trends |
| ⚡ Transfer & Discharge Efficiency | KPI trend lines, weekday vs weekend, year comparison |
| 🔍 Bottleneck Detection | Backlog alerts, inflow vs outflow, stagnation periods |
| 📊 Outcome Trend Analysis | Placement trends, variability, correlation matrix, KPI table |
| 📋 Raw Data | Filtered data view + CSV download |

---

## 📝 Deliverables

- **research_paper.md** — Full EDA, KPI analysis, insights & policy recommendations
- **executive_summary.md** — Short summary for government stakeholders
- **app.py** — Interactive Streamlit dashboard

---

*Machine Learning Internship — Unified Mentor | Healthcare Analytics Domain*
