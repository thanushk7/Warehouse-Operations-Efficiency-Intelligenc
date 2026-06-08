import pandas as pd
import os

current_path = os.getcwd()

data_path = os.path.join(current_path, "datas", "processed")
model_path = os.path.join(current_path, "kpi_results")

tp = pd.read_csv(os.path.join(data_path, "throughtputp.csv"))
sp = pd.read_csv(os.path.join(data_path, "shiftlogsp.csv"))

tp.columns = tp.columns.str.strip().str.lower()
sp.columns = sp.columns.str.strip().str.lower()

tp["operation_time"] = pd.to_datetime(tp["operation_time"], errors="coerce")
sp["login_time"] = pd.to_datetime(sp["login_time"], errors="coerce")
sp["logout_time"] = pd.to_datetime(sp["logout_time"], errors="coerce")

tp = tp.dropna(subset=["operation_time"])
sp = sp.dropna(subset=["login_time", "logout_time"])

tp["date"] = tp["operation_time"].dt.normalize()
sp["date"] = sp["login_time"].dt.normalize()

tp["error_flag"] = tp["error_flag"].fillna(0)
tp["error_flag"] = tp["error_flag"].apply(lambda x: 1 if x >= 1 else 0)

sp["shift_hours"] = (
    sp["logout_time"] - sp["login_time"]
).dt.total_seconds() / 3600

sp = sp[sp["shift_hours"] > 0]

worker_hours = (
    sp.groupby(["worker_id", "shift", "date"])["shift_hours"]
    .sum()
    .reset_index()
)

daily_ops = (
    tp.groupby(["worker_id", "shift", "date"])
    .agg(
        total_items_picked=("pick_qty", "sum"),
        total_errors=("error_flag", "sum"),
        total_items_processed=("operation_id", "count")
    )
    .reset_index()
)

kpi = daily_ops.merge(
    worker_hours,
    on=["worker_id", "shift", "date"],
    how="left"
)

kpi["pick_rate"] = (
    kpi["total_items_picked"] / kpi["shift_hours"]
)

kpi["error_rate"] = (
    kpi["total_errors"] / kpi["total_items_processed"]
)

shift_throughput = (
    tp.groupby(["shift", "date"])
    .agg(
        items_shipped=("pick_qty", "sum")
    )
    .reset_index()
)

utilization = worker_hours.copy()
utilization["utilization"] = utilization["shift_hours"] / 8

kpi = kpi.replace([float("inf"), -float("inf")], 0)
kpi = kpi.fillna(0)

kpi.to_csv(os.path.join(model_path, "kpi_worker_level.csv"), index=False)
shift_throughput.to_csv(os.path.join(model_path, "kpi_shift_throughput.csv"), index=False)
utilization.to_csv(os.path.join(model_path, "kpi_utilization.csv"), index=False)