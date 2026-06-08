import pandas as pd
import os

current_path = os.getcwd()
model_path = os.path.join(current_path, "fact_and_dim_table")
kpi_path = os.path.join(current_path, "kpi_results")
sim_path = os.path.join(current_path, "Staffing Optimization Simulation")
savepath=os.path.join(current_path,"summary")

fact = pd.read_csv(os.path.join(model_path, "fact_operations.csv"))
kpi = pd.read_csv(os.path.join(kpi_path, "kpi_worker_level.csv"))
sim = pd.read_csv(os.path.join(sim_path, "simulation_staffing_requirement.csv"))

fact["date"] = pd.to_datetime(fact["date"], errors="coerce")

total_throughput = fact["items_picked"].sum()
total_errors = fact["error_count"].sum()
total_operations = fact["operation_id"].count()

total_hours = kpi["shift_hours"].sum()
overall_efficiency = total_throughput / total_hours if total_hours != 0 else 0

error_rate = total_errors / total_operations if total_operations != 0 else 0
avg_pick_rate = kpi["pick_rate"].mean()

cost_per_hour = 100
total_cost = total_hours * cost_per_hour
cost_per_item = total_cost / total_throughput if total_throughput != 0 else 0

active_workers = fact["worker_id"].nunique()

avg_staffing_gap = sim["staffing_gap"].mean()

staffing_status = (
    "Understaffed" if avg_staffing_gap > 0 else
    "Overstaffed" if avg_staffing_gap < 0 else
    "Optimal"
)

summary = pd.DataFrame({
    "Metric": [
        "Total Throughput",
        "Overall Efficiency",
        "Error Rate",
        "Average Pick Rate",
        "Cost per Item",
        "Active Workers",
        "Staffing Status"
    ],
    "Value": [
        total_throughput,
        overall_efficiency,
        error_rate,
        avg_pick_rate,
        cost_per_item,
        active_workers,
        staffing_status
    ]
})
summary.to_csv(
    os.path.join(savepath, "executive_summary.csv"),
    index=False
)