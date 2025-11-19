# File: src/features/net_cash_flow.py
# Implements US-1
import pandas as pd
from pprint import pprint

def get_net_cash_flow(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    """
    Calculates the total Inflow (credit) vs. Outflow (debit)
    over time, grouped by month, for a specific date range.
    
    This function *intentionally ignores* 'transfer' types.
    
    Args:
        df: The cleaned financial transactions DataFrame.
        start_date: The start of the date range (inclusive).
        end_date: The end of the date range (inclusive).

    Returns:
        A DataFrame with columns [month_year, inflow, outflow].
    """
    
    # 1. Filter the DataFrame by the selected date range
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask]

    # 2. Filter *only* for Inflow/Outflow types.
    #    We MUST ignore 'transfer' for a Net Cash Flow analysis.
    cash_flow_df = filtered_df[filtered_df['type'].isin(['credit', 'debit'])]

    # 3. Handle the case where the filter results in no data
    if cash_flow_df.empty:
        return pd.DataFrame(columns=['month_year', 'inflow', 'outflow'])
        
    # 4. Create a month-year column for grouping
    cash_flow_df = cash_flow_df.copy() # Avoid SettingWithCopyWarning
    cash_flow_df['month_year'] = cash_flow_df['date'].dt.to_period('M')

    # 5. Group by month AND type, sum the amounts, and pivot the data
    #    This creates columns for 'credit' and 'debit'
    grouped = cash_flow_df.groupby(['month_year', 'type'])['amount'].sum().unstack(fill_value=0)

    # 6. Ensure both columns exist even if one has no data
    if 'credit' not in grouped.columns:
        grouped['credit'] = 0
    if 'debit' not in grouped.columns:
        grouped['debit'] = 0

    # 7. Rename columns to match our "Inflow/Outflow" contract
    final_df = grouped.reset_index().rename(
        columns={'credit': 'inflow', 'debit': 'outflow'}
    )
    
    # 8. Convert period back to timestamp for easy charting
    final_df['month_year'] = final_df['month_year'].dt.to_timestamp()
    
    return final_df

# --- Updated Test Block ---
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
        print("\n--- 🚀 Testing Net Cash Flow (2021 only) 🚀 ---")
        start_test = pd.to_datetime("2021-01-01")
        end_test = pd.to_datetime("2021-12-31")
        
        cash_flow_2021 = get_net_cash_flow(df, start_test, end_test)
        
        print("--- Testing Net Cash Flow Function (2021) ---")
        pprint(cash_flow_2021.head()) # Print the first 5 rows
        print("------------------------------------------")
    else:
        print("Error: Could not load data for testing.")