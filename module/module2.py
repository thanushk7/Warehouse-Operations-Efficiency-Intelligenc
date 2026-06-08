import pandas as pd
import os

current_path=os.getcwd()
savepath=os.path.join(current_path,"datas","processed")
datas_path=os.path.join(current_path,"datas","raw")
sl=pd.read_csv(os.path.join(datas_path,"shift_logs.csv"))
tp=pd.read_csv(os.path.join(datas_path,"throughput.csv"))

#-----------------------------------------------------------------------------------------------------#



sl["worker_id"] = sl["worker_id"].astype(str).str.strip()
sl["worker_id"] = sl["worker_id"].replace(["", "None", "nan"], pd.NA)

sl = sl[sl["worker_id"].str.match(r"^W\d{4}$", na=False)]
sl = sl.dropna(subset=["worker_id"])

sl["shift"]=sl["shift"].astype(str).str.strip()
sl["shift"]=sl["shift"].replace( ["None", "nan", ""],pd.NA)


sl["shift"] = sl["shift"].replace({
    "Mornng":"Morning",
    "Night ":"Night"
})
sl=sl.dropna(subset=["shift"])

sl["login_time"]=pd.to_datetime(sl["login_time"],format="%d-%m-%Y %H:%M",errors="coerce")
sl["logout_time"]=pd.to_datetime(sl["logout_time"],format="%d-%m-%Y %H:%M",errors="coerce")
sl = sl.dropna(subset=["login_time","logout_time"])


sl=sl[sl["login_time"]<sl["logout_time"]]
sl["shift_hours"]=(sl["logout_time"]-sl["login_time"]).dt.total_seconds()/3600

sl.to_csv((os.path.join(savepath,"shiftlogsp.csv")),index=False)
#-----------------------------------------------------------------------------------------------------#

tp["worker_id"] = tp["worker_id"].astype(str).str.strip()

tp["worker_id"] = tp["worker_id"].replace(["", "None", "nan", "W9999"],pd.NA)

tp = tp.dropna(subset=["worker_id"])

tp = tp[tp["worker_id"].str.match(r"^W\d{4}$", na=False)]

tp["shift"] = tp["shift"].astype(str).str.strip()

tp["shift"] = tp["shift"].replace({
    "Mornng": "Morning",
    "Night ": "Night"
})

tp["shift"] = tp["shift"].replace(["", "None", "nan"], pd.NA)

tp = tp.dropna(subset=["shift"])

valid_shift = ["Morning", "Evening", "Night"]

tp = tp[tp["shift"].isin(valid_shift)]

tp["zone"] = tp["zone"].astype(str).str.strip()

tp["zone"] = tp["zone"].replace(
    ["", "None", "nan", "Z"],
    pd.NA
)

tp = tp.dropna(subset=["zone"])

valid_zone = ["A","B","C","D","E"]

tp = tp[tp["zone"].isin(valid_zone)]
tp["pick_qty"] = pd.to_numeric(tp["pick_qty"], errors="coerce")

tp = tp[tp["pick_qty"] > 0]

tp["error_flag"] = tp["error_flag"].apply(
    lambda x: 1 if x == 1 else 0
)
tp["operation_time"] = pd.to_datetime(
    tp["operation_time"],
    errors="coerce"
)

tp = tp.dropna(subset=["operation_time"])
tp = tp.drop_duplicates(
    subset=["operation_id"]
)
tp.to_csv((os.path.join(savepath,"throughtputp.csv")),index=False)
