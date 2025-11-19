# File: src/features/summary_kpis.py
import pandas as pd
from pprint import pprint # Used for pretty-printing in our test block

def get_summary_kpis(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> dict:
    """
    Calculates main summary KPIs, both overall and broken down
    by transaction type ('credit', 'debit', 'transfer') for a 
    specific date range.
    
    Args:
        df: The cleaned financial transactions DataFrame.
        start_date: The start of the date range (inclusive).
        end_date: The end of the date range (inclusive).
            
    Returns:
        A nested dictionary containing KPIs for 'overall' and each type.
    """
    
    # 1. Filter the DataFrame based on the user-selected date range
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask]
    
    # 2. Handle the case where the filter results in no data
    if filtered_df.empty:
        # Return a zero-filled structure
        empty_kpis = {"total_amount": 0, "total_transactions": 0, "avg_transaction": 0}
        return {
            "overall": empty_kpis,
            "credit": empty_kpis,
            "debit": empty_kpis,
            "transfer": empty_kpis
        }

    # 3. Calculate "Overall" KPIs (on the filtered data)
    overall_kpis = {
        "total_amount": filtered_df['amount'].sum(),
        "total_transactions": len(filtered_df),
        "avg_transaction": filtered_df['amount'].mean()
    }
    
    # 4. Calculate KPIs by Type
    grouped_by_type = filtered_df.groupby('type')['amount']
    type_sum = grouped_by_type.sum()
    type_count = grouped_by_type.count()
    type_mean = grouped_by_type.mean()

    # 5. Build the final nested dictionary result
    # We use .get(key, 0) to prevent errors if a type has 0 transactions
    results = {
        "overall": overall_kpis,
        "credit": {
            "total_amount": type_sum.get('credit', 0),
            "total_transactions": type_count.get('credit', 0),
            "avg_transaction": type_mean.get('credit', 0)
        },
        "debit": {
            "total_amount": type_sum.get('debit', 0),
            "total_transactions": type_count.get('debit', 0),
            "avg_transaction": type_mean.get('debit', 0)
        },
        "transfer": {
            "total_amount": type_sum.get('transfer', 0),
            "total_transactions": type_count.get('transfer', 0),
            "avg_transaction": type_mean.get('transfer', 0)
        }
    }
    
    return results

# --- Updated Test Block ---
# Now it's even more important, to test your new nested structure
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
        # --- Test 1: Full Date Range ---
        print("--- 🚀 Testing Full Range 🚀 ---")
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        kpis_full = get_summary_kpis(df, min_date, max_date)
        
        # Use Pretty Print to show the nested dictionary
        pprint(kpis_full)
        
        print("--------------------------------------")
    else:
        print("Error: Could not load data for testing.")