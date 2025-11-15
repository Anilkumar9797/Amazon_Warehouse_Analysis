# -----------------------------
# 1️⃣ IMPORT LIBRARIES
# -----------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# 2️⃣ LOAD DATASETS
# -----------------------------
staff = pd.read_csv('staffing_levels.csv', parse_dates=['timestamp'])
pick = pd.read_csv('picking_activity.csv', parse_dates=['timestamp'])
orders = pd.read_csv('order_flow.csv', parse_dates=['pick_start','pick_end','sla_cutoff','actual_departure'])

# Ensure 'hour' column exists in pick dataset
if 'hour' not in pick.columns:
    pick['hour'] = pick['timestamp'].dt.hour

# -----------------------------
# 3️⃣ CALCULATE W2S (UNITS PER PICKER)
# -----------------------------
pick['w2s'] = pick['units_picked'] / pick['active_pickers']

# -----------------------------
# 4️⃣ CREATE OUTPUTS FOLDER
# -----------------------------
os.makedirs('outputs', exist_ok=True)

# -----------------------------
# 5️⃣ AVERAGE W2S PER HOUR
# -----------------------------
hourly_w2s = pick.groupby('hour')['w2s'].mean().reset_index()

plt.figure(figsize=(10,5))
plt.bar(hourly_w2s['hour'], hourly_w2s['w2s'], color='skyblue')
plt.axvspan(1,3, color='red', alpha=0.2, label='Collapse Hours (1-3 AM)')
plt.title('Average W2S per Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Units per Picker')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/w2s_per_hour.png')
plt.close()

# -----------------------------
# 6️⃣ LATE-PICK RATE PER HOUR
# -----------------------------
orders['late'] = orders['actual_departure'] > orders['sla_cutoff']
orders['pick_hour_only'] = orders['pick_start'].dt.hour

late_rate_hourly = orders.groupby('pick_hour_only')['late'].mean().reset_index()

plt.figure(figsize=(10,5))
plt.bar(late_rate_hourly['pick_hour_only'], late_rate_hourly['late'], color='orange')
plt.axvspan(1,3, color='red', alpha=0.2)
plt.title('Late-pick Rate by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Fraction of Orders Late')
plt.tight_layout()
plt.savefig('outputs/late_pick_rate.png')
plt.close()

# -----------------------------
# 7️⃣ BACKLOG PER HOUR
# -----------------------------
orders = orders.sort_values('pick_start')
orders['backlog_hours'] = (orders['actual_departure'] - orders['pick_start']).dt.total_seconds() / 3600
backlog_hourly = orders.groupby(orders['pick_start'].dt.floor('h'))['backlog_hours'].mean().reset_index()

plt.figure(figsize=(12,5))
plt.plot(backlog_hourly['pick_start'], backlog_hourly['backlog_hours'], color='purple', label='Avg backlog (hours)')
plt.axvspan(pd.Timestamp('2025-01-01 01:00:00'), pd.Timestamp('2025-01-01 03:00:00'), color='red', alpha=0.2)
plt.title('Hourly Backlog (Hours)')
plt.xlabel('Timestamp')
plt.ylabel('Avg Backlog (Hours)')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/backlog_per_hour.png')
plt.close()

# -----------------------------
# 8️⃣ FOCUS ON COLLAPSE HOURS (1-3 AM)
# -----------------------------
collapse = pick[(pick['hour'] >= 1) & (pick['hour'] <= 3)]
print("Collapse Hours W2S Snapshot:")
print(collapse[['timestamp','active_pickers','units_picked','w2s']].head(10))

# Scenario analysis — adding extra pickers
for extra in [1,2,3]:
    pick[f'w2s_plus_{extra}'] = pick['units_picked'] / (pick['active_pickers'] + extra)

collapse_extra = pick[(pick['hour'] >= 1) & (pick['hour'] <= 3)]
print("\nCollapse Hours W2S with extra pickers:")
print(collapse_extra[['timestamp','w2s','w2s_plus_1','w2s_plus_2','w2s_plus_3']].head(10))

# -----------------------------
# 9️⃣ HEATMAP (MONTHLY PATTERN)
# -----------------------------
pivot = pick.pivot_table(index=pick['timestamp'].dt.date, columns='hour', values='w2s')
plt.figure(figsize=(15,6))
sns.heatmap(pivot, cmap='Reds')
plt.title('W2S Heatmap by Day and Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Date')
plt.tight_layout()
plt.savefig('outputs/w2s_heatmap.png')
plt.close()

# -----------------------------
# 🔟 PREDICT OPTIMAL PICKERS PER HOUR
# -----------------------------
def predict_optimal_pickers(df, target_w2s=350):
    df['optimal_pickers'] = np.ceil(df['units_picked'] / target_w2s)
    df['extra_needed'] = df['optimal_pickers'] - df['active_pickers']
    df['extra_needed'] = df['extra_needed'].apply(lambda x: max(0, x))
    return df

pick = predict_optimal_pickers(pick)

collapse_optimal = pick[(pick['hour'] >= 1) & (pick['hour'] <= 3)]
print("\nCollapse Hours - Optimal Picker Recommendations:")
print(collapse_optimal[['timestamp','active_pickers','units_picked','w2s','optimal_pickers','extra_needed']].head(10))

collapse_optimal.to_csv('outputs/collapse_hours_optimal_pickers.csv', index=False)
print("✅ CSV with optimal picker recommendations saved in outputs folder.")

# -----------------------------
# 1️⃣1️⃣ SUMMARY
# -----------------------------
print("\n📊 Summary Statistics:")
print(f"Peak W2S Hour: {hourly_w2s.loc[hourly_w2s['w2s'].idxmax()].to_dict()}")
print(f"Peak Late-pick Hour: {late_rate_hourly.loc[late_rate_hourly['late'].idxmax()].to_dict()}")
print(f"Peak Backlog Hour: {backlog_hourly.loc[backlog_hourly['backlog_hours'].idxmax()].to_dict()}")

print("\n✅ End-to-end analysis complete. All charts, heatmap, and recommendations saved in 'outputs' folder. Ready for presentation or resume portfolio.")
