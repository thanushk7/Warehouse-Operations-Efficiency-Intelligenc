import pandas as pd
import os

current_path = os.getcwd()
model = os.path.join(current_path, "fact_and_dim_table")
model_path = os.path.join(current_path, "Throughput Forecasting")


fact = pd.read_csv(os.path.join(model, "fact_operations.csv"))

fact["date"] = pd.to_datetime(fact["date"], errors="coerce")

daily_tp = (
    fact.groupby("date")
    .agg(total_items=("items_picked", "sum"))
    .reset_index()
    .sort_values("date")
)

daily_tp = daily_tp.set_index("date")


daily_tp["moving_avg"] = (
    daily_tp["total_items"]
    .rolling(window=7, min_periods=1)
    .mean()
)

daily_tp = daily_tp.reset_index()

daily_tp["t"] = range(len(daily_tp))

t_mean = daily_tp["t"].mean()
y_mean = daily_tp["total_items"].mean()

numerator = ((daily_tp["t"] - t_mean) * (daily_tp["total_items"] - y_mean)).sum()
denominator = ((daily_tp["t"] - t_mean) ** 2).sum()

slope = numerator / denominator if denominator != 0 else 0
intercept = y_mean - slope * t_mean

future_days = 7
future_t = range(len(daily_tp), len(daily_tp) + future_days)

forecast_values = [intercept + slope * i for i in future_t]

forecast_dates = pd.date_range(
    start=daily_tp["date"].max() + pd.Timedelta(days=1),
    periods=future_days
)

forecast_dataset = pd.DataFrame({
    "date": forecast_dates,
    "moving_avg_forecast": daily_tp["moving_avg"].tail(7).mean(),
    "trend_forecast": forecast_values
})

forecast_dataset.to_csv(
    os.path.join(model_path, "throughput_forecast_next_week.csv"),
    index=False
)