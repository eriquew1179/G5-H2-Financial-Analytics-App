# File: src/features/temporal_trend.py
# Implements US-5
# All comments are in English, as requested.
import pandas as pd
from pprint import pprint

def get_temporal_trend(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    """
    Returns a DataFrame showing the total monthly transaction amount
    for a specific date range.
    
    Parameters:
        df (pd.DataFrame): The financial transactions dataset.
        start_date (pd.Timestamp): The start of the date range (inclusive).
        end_date (pd.Timestamp): The end of the date range (inclusive).

    Returns:
        pd.DataFrame: DataFrame grouped by month-year with total summed amount.
    """
    
    # 1. Filter the DataFrame based on the user-selected date range
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask]

    # 2. Handle the case where the filter results in no data
    if filtered_df.empty:
        # Return an empty DataFrame with the correct columns
        return pd.DataFrame(columns=['month_year', 'amount'])

    # 3. Create month-year column ON THE FILTERED DATA
    # Use .copy() to avoid the SettingWithCopyWarning
    filtered_df = filtered_df.copy() 
    filtered_df['month_year'] = filtered_df['date'].dt.to_period('M')

    # 4. Group by month-year and sum amounts
    monthly = filtered_df.groupby('month_year')['amount'].sum().reset_index()

    # 5. Convert month-year back to datetime for sorting and charting
    monthly['month_year'] = monthly['month_year'].dt.to_timestamp()

    return monthly

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
        print("\n--- 🚀 Testing Specific Range (2021 only) 🚀 ---")
        start_test = pd.to_datetime("2021-01-01")
        end_test = pd.to_datetime("2021-12-31")
        
        trend_2021 = get_temporal_trend(df, start_test, end_test)
        
        print("--- Testing Temporal Trend Function (2021) ---")
        pprint(trend_2021.head()) # Print the first 5 rows
        print("------------------------------------------")
    else:
        print("Error: Could not load data for testing.")