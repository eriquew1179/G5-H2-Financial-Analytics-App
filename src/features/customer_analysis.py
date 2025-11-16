# File: src/features/customer_analysis.py
# Implements US-3 and US-4
# All comments are in English, as requested.
import pandas as pd
from pprint import pprint

# =========================
# US-3 — Distribution by transaction type
# =========================
def get_distribution_by_type(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    """
    Group totals and counts by transaction 'type' for a specific date range.
    Returns a sorted DataFrame by total amount (desc).
    """
    
    # 1. Filter the DataFrame based on the user-selected date range
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask]

    # 2. Handle the case where the filter results in no data
    if filtered_df.empty:
        return pd.DataFrame(columns=['type', 'amount_sum', 'transactions'])

    # 3. Run the groupby on the FILTERED data
    summary = (
        filtered_df.groupby("type")
          .agg(amount_sum=("amount", "sum"),
               transactions=("amount", "count"))
          .reset_index()
    )
    summary["amount_sum"] = summary["amount_sum"].astype(float).round(2)
    return summary.sort_values("amount_sum", ascending=False)


# =========================
# US-4 — Top clients by total amount
# =========================
def get_top_clients(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp, n: int = 10) -> pd.DataFrame:
    """
    Top-N clients by total transaction amount for a specific date range.
    Requires a 'customer_id' column.
    """
    if "customer_id" not in df.columns:
        return pd.DataFrame(columns=['customer_id', 'total_amount', 'transactions'])

    # 1. Filter the DataFrame based on the user-selected date range
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask]
    
    # 2. Handle the case where the filter results in no data
    if filtered_df.empty:
        return pd.DataFrame(columns=['customer_id', 'total_amount', 'transactions'])

    # 3. Run the groupby on the FILTERED data
    grouped = (
        filtered_df.groupby("customer_id")
          .agg(total_amount=("amount", "sum"),
               transactions=("amount", "count"))
          .reset_index()
    )
    
    # Continue with your excellent logic
    out = (
        grouped.sort_values("total_amount", ascending=False)
               .head(n)
               .copy()
    )
    out["total_amount"] = out["total_amount"].astype(float).round(2)
    return out


# =========================
# Updated Test Block
# =========================
if __name__ == "__main__":
    
    import sys
    import os
    
    # Find the project root to import other modules
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(project_root)
    
    from src.data_loader import load_data
    
    DATA_PATH = "data/financial_transactions.csv"
    df = load_data(DATA_PATH)
    
    if not df.empty:
        # --- Test 1: Specific Date Range (Testing new feature) ---
        print("\n--- 🚀 Testing Specific Range (2021 only) 🚀 ---")
        start_test = pd.to_datetime("2021-01-01")
        end_test = pd.to_datetime("2021-12-31")
        
        # --- Test US-3 ---
        print("\n--- Testing US-3 (Distribution by Type) ---")
        us3_table = get_distribution_by_type(df, start_test, end_test)
        pprint(us3_table)
        
        # --- Test US-4 ---
        print("\n--- Testing US-4 (Top Clients) ---")
        us4_table = get_top_clients(df, start_test, end_test, n=5)
        pprint(us4_table)
        
        print("------------------------------------------")
    else:
        print("Error: Could not load data for testing.")