import pandas as pd
import os
import math

current_path = os.getcwd()
model = os.path.join(current_path, "kpi_results")
model_path = os.path.join(current_path, "Staffing Optimization Simulation")

kpi = pd.read_csv(os.path.join(model, "kpi_worker_level.csv"))

kpi["date"] = pd.to_datetime(kpi["date"], errors="coerce")

staffing_current = (
    kpi.groupby(["shift", "date"])
    .agg(
        workers_present=("worker_id", "nunique"),
        total_pick=("total_items_picked", "sum"),
        avg_pick_rate=("pick_rate", "mean")
    )
    .reset_index()
)

staffing_current["demand_20pct"] = staffing_current["total_pick"] * 1.20

staffing_current["workers_required_20pct"] = (
    staffing_current["demand_20pct"]
    / (staffing_current["avg_pick_rate"] * 8)
)
staffing_current["workers_required_20pct"] = (
    staffing_current["workers_required_20pct"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)
staffing_current["workers_required_20pct"] = staffing_current[
    "workers_required_20pct"
].apply(lambda x: math.ceil(x))
staffing_current["workers_if_absent"] = (
    staffing_current["workers_present"] - 1
)

staffing_current["throughput_if_absent"] = (
    staffing_current["workers_if_absent"]
    * staffing_current["avg_pick_rate"]
    * 8
)

staffing_current["staffing_gap"] = (
    staffing_current["workers_required_20pct"]
    - staffing_current["workers_present"]
)

staffing_current = staffing_current.fillna(0)

staffing_current.to_csv(
    os.path.join(model_path, "simulation_staffing_requirement.csv"),
    index=False
)