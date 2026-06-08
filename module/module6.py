import pandas as pd
import os

current_path = os.getcwd()
model = os.path.join(current_path, "kpi_results")
model_path = os.path.join(current_path, "Productivity Comparison Analysis")

kpi = pd.read_csv(os.path.join(model, "kpi_worker_level.csv"))
shift_tp = pd.read_csv(os.path.join(model, "kpi_shift_throughput.csv"))

kpi["date"] = pd.to_datetime(kpi["date"], errors="coerce")
shift_tp["date"] = pd.to_datetime(shift_tp["date"], errors="coerce")

worker_comp = (
    kpi.groupby("worker_id")
    .agg(
        total_pick=("total_items_picked", "sum"),
        avg_pick_rate=("pick_rate", "mean"),
        avg_error_rate=("error_rate", "mean")
    )
    .reset_index()
)

worker_ranking = worker_comp.sort_values(
    "avg_pick_rate",
    ascending=False
)

high_error_worker = worker_comp.sort_values(
    "avg_error_rate",
    ascending=False
)

shift_comp = (
    kpi.groupby("shift")
    .agg(
        total_pick=("total_items_picked", "sum"),
        avg_pick_rate=("pick_rate", "mean"),
        avg_error_rate=("error_rate", "mean")
    )
    .reset_index()
)

low_productivity_shift = shift_comp.sort_values(
    "avg_pick_rate"
)


day_comp = (
    kpi.groupby("date")
    .agg(
        total_pick=("total_items_picked", "sum"),
        avg_pick_rate=("pick_rate", "mean"),
        avg_error_rate=("error_rate", "mean")
    )
    .reset_index()
).sort_values("date")


worker_ranking.to_csv(
    os.path.join(model_path, "analysis_worker_ranking.csv"),
    index=False
)

high_error_worker.to_csv(
    os.path.join(model_path, "analysis_high_error_worker.csv"),
    index=False
)

shift_comp.to_csv(
    os.path.join(model_path, "analysis_shift_comparison.csv"),
    index=False
)

low_productivity_shift.to_csv(
    os.path.join(model_path, "analysis_low_productivity_shift.csv"),
    index=False
)

day_comp.to_csv(
    os.path.join(model_path, "analysis_day_trend.csv"),
    index=False
)