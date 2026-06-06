import pandas as pd
from pathlib import Path

base = Path(r"D:\FSF\FPL\Data\2025-2026\By Tournament\Premier League")

gw_data = []

for gw_folder in base.glob("GW*"):
    gw_file = gw_folder / "player_gameweek_stats.csv"

    if gw_file.exists():
        df = pd.read_csv(gw_file)
        gw_data.append(df)

all_data = pd.concat(gw_data, ignore_index=True)

all_data = all_data.sort_values(["id", "gw"])

last5 = all_data.groupby("id").tail(5)
last3 = all_data.groupby("id").tail(3)

summary_last5 = (
    last5.groupby(["id", "web_name"])
    .agg(
        goals_last5=("goals_scored", "sum"),
        assists_last5=("assists", "sum"),
        minutes_last5=("minutes", "sum"),
        bonus_last5=("bonus", "sum"),
        xg_last5=("expected_goals", "sum"),
        xa_last5=("expected_assists", "sum"),
        threat_last5=("threat", "sum"),
        creativity_last5=("creativity", "sum"),
        total_points_last5=("total_points", "sum")
    )
    .reset_index()
)

points_last3 = (
    last3.groupby("id")
    .agg(points_last3=("total_points", "sum"))
    .reset_index()
)

final = summary_last5.merge(points_last3, on="id", how="left")

final.to_excel(
    r"D:\FSF\FPL\fpl_player_summary.xlsx",
    index=False
)

print("Done. Excel file created.")