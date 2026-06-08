import pandas as pd
import os

current_path = os.getcwd()

data_path = os.path.join(current_path, "datas", "processed")
save_path = os.path.join(current_path, "fact_and_dim_table")

os.makedirs(save_path, exist_ok=True)

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

tp["worker_id"] = tp["worker_id"].astype(str).str.strip()
sp["worker_id"] = sp["worker_id"].astype(str).str.strip()

tp["shift"] = tp["shift"].astype(str).str.strip()
sp["shift"] = sp["shift"].astype(str).str.strip()

tp["error_flag"] = tp["error_flag"].fillna(0)
tp["error_flag"] = tp["error_flag"].apply(
    lambda x: 1 if x >= 1 else 0
)


dim_time = (
    tp[["date"]]
    .drop_duplicates()
    .sort_values("date")
    .reset_index(drop=True)
)

dim_time["month"] = dim_time["date"].dt.month
dim_time["year"] = dim_time["date"].dt.year


dim_worker = (
    sp[["worker_id"]]
    .drop_duplicates()
    .sort_values("worker_id")
    .reset_index(drop=True)
)


dim_shift = (
    tp[["shift"]]
    .drop_duplicates()
    .sort_values("shift")
    .reset_index(drop=True)
)

dim_shift["shift_id"] = [
    "S" + str(i + 1) for i in range(len(dim_shift))
]

dim_shift = dim_shift[["shift_id", "shift"]]

tp = tp.merge(dim_shift, on="shift", how="left")


fact_operations = tp[[
    "operation_id",
    "date",
    "worker_id",
    "shift_id",
    "zone",
    "pick_qty",
    "error_flag"
]].copy()

fact_operations = fact_operations.rename(
    columns={
        "pick_qty": "items_picked",
        "error_flag": "error_count"
    }
)

fact_operations = fact_operations.drop_duplicates()


dim_time.to_csv(os.path.join(save_path, "dim_time.csv"), index=False)
dim_worker.to_csv(os.path.join(save_path, "dim_worker.csv"), index=False)
dim_shift.to_csv(os.path.join(save_path, "dim_shift.csv"), index=False)
fact_operations.to_csv(
    os.path.join(save_path, "fact_operations.csv"),
    index=False
)

