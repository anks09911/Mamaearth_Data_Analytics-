# ============================================================
# MAMAEARTH GROWTH ANALYTICS PROJECT
# Part 2: Python / Pandas Data Wrangling and EDA
#
# Input:
#   data/customers.csv
#   data/products.csv
#   data/orders.csv
#
# Output:
#   output/cleaned_orders.csv
#   output/merged_clean.csv
#   output/monthly_revenue_including_outliers.csv
#   output/monthly_revenue_corrected.csv
#   output/return_rate_by_payment.csv
#   output/return_rate_by_payment_and_tier.csv
#
# Original CSV files are never modified.
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(
    "/content/drive/MyDrive/mamaearth_analytics"
)

DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
