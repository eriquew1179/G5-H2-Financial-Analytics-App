import pandas as pd

def temporal_trend(df):
    """
    Returns a DataFrame showing the total monthly transaction amount.
    
    Parameters:
        df (pd.DataFrame): The financial transactions dataset.

    Returns:
        pd.DataFrame: DataFrame grouped by month-year with total summed amount.
    """

    # Ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Add month-year column
    df['month_year'] = df['date'].dt.to_period('M')

    # Group by month-year and sum amounts
    monthly = df.groupby('month_year')['amount'].sum().reset_index()

    # Convert month-year back to datetime for sorting
    monthly['month_year'] = monthly['month_year'].dt.to_timestamp()

    return monthly
