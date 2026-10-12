
# ============================================================
# MAMAEARTH GROWTH ANALYTICS PROJECT
# Part 2, Task 11: Visualizations
# ============================================================

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(
    "/content/drive/MyDrive/Mamaearth_Data_Analytics"
)

OUTPUT_DIR = PROJECT_DIR / "output"

VISUALIZATIONS_DIR = PROJECT_DIR / "05_Visualizations"

VISUALIZATIONS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD ANALYSIS RESULTS
# ============================================================

return_file = OUTPUT_DIR / "return_rate_by_payment.csv"
revenue_file = OUTPUT_DIR / "monthly_revenue_corrected.csv"

if not return_file.exists():
    raise FileNotFoundError(f"Missing file: {return_file}")

if not revenue_file.exists():
    raise FileNotFoundError(f"Missing file: {revenue_file}")

return_rates = pd.read_csv(return_file, index_col=0)

monthly_revenue = pd.read_csv(revenue_file, index_col=0)

# Check required columns.

if "return_rate_pct" not in return_rates.columns:
    raise ValueError(
        "Column 'return_rate_pct' not found in return-rate CSV."
    )

if "monthly_order_value" not in monthly_revenue.columns:
    raise ValueError(
        "Column 'monthly_order_value' not found in revenue CSV."
    )

# Convert values to numeric.

return_rates["return_rate_pct"] = pd.to_numeric(
    return_rates["return_rate_pct"],
    errors="raise"
)

monthly_revenue["monthly_order_value"] = pd.to_numeric(
    monthly_revenue["monthly_order_value"],
    errors="raise"
)

print("\nReturn rate results:")
print(return_rates)

print("\nMonthly revenue results:")
print(monthly_revenue)


# ============================================================
# CHART 1: RETURN RATE BY PAYMENT METHOD
# ============================================================

print("\nCreating return-rate chart...")

return_rates = return_rates.sort_values(
    "return_rate_pct",
    ascending=False
)

plt.figure(figsize=(8, 5))

bars = plt.bar(
    return_rates.index.astype(str),
    return_rates["return_rate_pct"]
)

for bar, value in zip(
    bars,
    return_rates["return_rate_pct"]
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.1f}%",
        ha="center",
        va="bottom"
    )

plt.title("Return Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")

plt.ylim(
    0,
    max(return_rates["return_rate_pct"].max() * 1.2, 1)
)

plt.tight_layout()

return_chart_path = (
    VISUALIZATIONS_DIR / "return_rate_by_payment.png"
)

plt.savefig(
    return_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("Saved:", return_chart_path)


# ============================================================
# CHART 2: OUTLIER-CORRECTED MONTHLY REVENUE
# ============================================================

print("\nCreating monthly revenue chart...")

monthly_revenue = monthly_revenue.sort_index()

peak_month = monthly_revenue[
    "monthly_order_value"
].idxmax()

peak_value = monthly_revenue[
    "monthly_order_value"
].max()

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_revenue.index.astype(str),
    monthly_revenue["monthly_order_value"],
    marker="o"
)

plt.scatter(
    [str(peak_month)],
    [peak_value],
    marker="o",
    label=f"Peak: ₹{peak_value:,.2f}"
)

plt.title("Outlier-Corrected Monthly Order Value Trend")
plt.xlabel("Month")
plt.ylabel("Order Value (INR)")

plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

monthly_chart_path = (
    VISUALIZATIONS_DIR / "monthly_revenue_trend.png"
)

plt.savefig(
    monthly_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("Saved:", monthly_chart_path)

print("\nPeak month:", peak_month)
print(f"Peak monthly order value: ₹{peak_value:,.2f}")


# ============================================================
# TASK COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("TASK 11: VISUALIZATIONS COMPLETED")
print("=" * 60)

print("\nGenerated files:")

print(return_chart_path)
print(monthly_chart_path)
