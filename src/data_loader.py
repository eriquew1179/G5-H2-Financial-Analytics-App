# File: src/data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data  # ¡Importante! Cachea los datos para que no se carguen cada vez
def load_data(csv_path: str) -> pd.DataFrame:
    """
    Loads and cleans the financial transaction data from a CSV file.
    """
    try:
        df = pd.read_csv(csv_path)
        
        # --- Data Cleaning (Sprint 0) ---
        
        # Convert date column to datetime objects
        df['date'] = pd.to_datetime(df['date'])
        
        # Ensure 'amount' is a numeric type
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Drop rows with any missing values to ensure clean analysis
        df.dropna(inplace=True) 
        
        return df
        
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {csv_path}")
        return pd.DataFrame() # Return an empty DataFrame on error
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()