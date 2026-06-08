import pandas as pd
import os

current_path=os.getcwd()
datas_path=os.path.join(current_path,"datas","raw")
shift_logs=pd.read_csv(os.path.join(datas_path,"shift_logs.csv"))
throughput=pd.read_csv(os.path.join(datas_path,"throughput.csv"))

