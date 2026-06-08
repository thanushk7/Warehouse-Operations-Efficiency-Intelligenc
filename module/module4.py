import pandas as pd
import os
from datetime import datetime

current_path = os.getcwd()

data_path = os.path.join(current_path, "datas", "processed")
model_path = os.path.join(current_path, "error_alert")

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

tp["worker_id"] = tp["worker_id"].astype(str).str.strip()
sp["worker_id"] = sp["worker_id"].astype(str).str.strip()

tp["error_flag"] = tp["error_flag"].fillna(0)
tp["error_flag"] = tp["error_flag"].apply(lambda x: 1 if x >= 1 else 0)

sp["shift_hours"] = (
    sp["logout_time"] - sp["login_time"]
).dt.total_seconds() / 3600

sp = sp[sp["shift_hours"] > 0]

worker_hours = (
    sp.groupby(["worker_id", "date"])["shift_hours"]
    .sum()
    .reset_index()
)

daily_tp = (
    tp.groupby(["worker_id", "date"])
    .agg(
        total_pick=("pick_qty", "sum"),
        total_error=("error_flag", "sum"),
        operations=("operation_id", "count")
    )
    .reset_index()
)

kpi = daily_tp.merge(
    worker_hours,
    on=["worker_id", "date"],
    how="left"
)

kpi["pick_rate"] = kpi["total_pick"] / kpi["shift_hours"]
kpi["error_rate"] = kpi["total_error"] / kpi["operations"]

kpi = kpi.replace([float("inf"), -float("inf")], 0)
kpi = kpi.fillna(0)

error_rate_alert = kpi[kpi["error_rate"] > 0.05]

today = datetime.now().strftime("%Y%m%d")

error_rate_alert.to_csv(
    os.path.join(model_path, f"error_rate_alert_{today}.csv"),
    index=False
)