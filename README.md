# 📊 Amazon Warehouse Project – Python & Data Analytics

## Overview
This project analyzes Amazon warehouse picking data to identify "collapse hours" (1-3 AM) and optimize picker allocation. It combines bar charts, line plots, heatmaps, and predictive analytics to uncover trends in warehouse efficiency, late-pick rates, and backlog. Designed as a portfolio project, it showcases actionable insights for operational optimization and highlights Python, data visualization, and analytics skills.

---

## Key Metrics
| Metric | Value |
|--------|-------|
| Peak W2S (Units per Picker) Hour | 13:00 – 349 units/picker |
| Peak Late-pick Hour | 04:00 – 100% of orders late |
| Peak Backlog Hour | 02:00 – 0.35 hours average backlog |
| Collapse Hours (1-3 AM) | Critical period requiring additional pickers |

---

## Visuals Included
- **Bar charts** for:
  - Average W2S per hour  
  - Late-pick rate by hour  
- **Line plot** for hourly backlog of orders  
- **Heatmap** visualizing daily W2S trends across hours  
- **Scenario analysis** with additional pickers to improve W2S during collapse hours  
- **Predictive recommendations** for optimal picker allocation during critical hours  

**Example Charts:**
- Average W2S per Hour: Highlights collapse hours (1-3 AM) with reduced units per picker.  
- Late-Pick Rate by Hour: Shows fraction of orders late, highlighting bottlenecks.  
- Hourly Backlog Plot: Displays backlog trends and peak hours.  
- W2S Heatmap: Visualizes daily efficiency patterns by hour.  

---

## Insights & Business Impact
- Collapse hours consistently show reduced picker efficiency, higher backlog, and elevated late-pick rates.  
- Adding 1-2 extra pickers during collapse hours significantly improves W2S and reduces backlog.  
- Peak efficiency and late-pick analysis allows for informed staffing decisions, reducing operational bottlenecks.  
- Heatmap visualization identifies recurring workload patterns, helping plan staffing and resource allocation.  
- Predictive recommendations provide actionable insights for warehouse managers, improving decision-making and operational efficiency.

**Sample Output Snapshot:**

**Collapse Hours W2S Snapshot**
| Timestamp           | Active Pickers | Units Picked | W2S |
|--------------------|----------------|-------------|-----|
| 2025-01-01 01:00:00 | 14            | 4508        | 322 |
| 2025-01-01 02:00:00 | 13            | 4771        | 367 |
| 2025-01-01 03:00:00 | 13            | 4316        | 332 |

**Collapse Hours - Optimal Picker Recommendations**
| Timestamp           | Active Pickers | Units Picked | W2S | Optimal Pickers | Extra Needed |
|--------------------|----------------|-------------|-----|----------------|-------------|
| 2025-01-01 01:00:00 | 14            | 4508        | 322 | 13             | 0           |
| 2025-01-01 02:00:00 | 13            | 4771        | 367 | 14             | 1           |
| 2025-01-01 03:00:00 | 13            | 4316        | 332 | 13             | 0           |

---

## Tools Used
- Python 3.x  
- Pandas & NumPy for data processing  
- Matplotlib & Seaborn for visualizations  
- CSV files for input/output data management  
- Scenario modeling for predictive staffing recommendations  

---

## Dataset Source
This project uses sample Amazon warehouse datasets, including:  
- `staffing_levels.csv` – Hourly picker staffing information  
- `picking_activity.csv` – Units picked and active pickers per hour  
- `order_flow.csv` – Orders with pick start/end times, SLA cutoff, and actual departure  

---

Project Structure
Amazon_Warehouse_Analysis/
│
├── outputs/                  # Created after running the script
│   ├── w2s_per_hour.png
│   ├── late_pick_rate.png
│   ├── backlog_plot.png
│   ├── heatmap_w2s.png
│   └── collapse_hours_optimal_pickers.csv
├── Amazon_warehouse.py
├── Amazon_warehouse_project/ # Optional folder if used
├── LICENSE
├── README.md
├── order_flow.csv.zip         # Unzip before running
├── picking_activity.csv
└── staffing_levels.csv
