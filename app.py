# File: app.py
# This is the main file for US-6 (The Dashboard)
# All comments are in English, as requested.

import streamlit as st
import pandas as pd
from datetime import datetime

# --- Import all our feature functions from the 'src' directory ---
# 1. The data loader
from src.data_loader import load_data

# 2. Our 5 feature functions
from src.features.net_cash_flow import get_net_cash_flow           # US-1
from src.features.summary_kpis import get_summary_kpis            # US-2
from src.features.customer_analysis import get_distribution_by_type, get_top_clients # US-3 & US-4
from src.features.temporal_trend import get_temporal_trend      # US-5

# --- Page Configuration ---
# Set the layout to wide mode for a modern dashboard feel
st.set_page_config(layout="wide")

# --- Main Title ---
st.title("G5-H2 Financial Analysis Dashboard")
st.caption(f"Scrum Master: Wilson | Team: Diego, Avinash, Joshua, Wilson | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- 1. Load Data (The Foundation) ---
# This is the single source of truth for our data
DATA_PATH = "data/financial_transactions.csv"
df = load_data(DATA_PATH)

# If the data loading fails, stop the app.
if df.empty:
    st.error("CRITICAL ERROR: Failed to load data. Please ensure 'data/financial_transactions.csv' exists.")
    st.stop()

# --- 2. Sidebar Filters (The Interactivity) ---
st.sidebar.header("Dashboard Filters")

# Get the min and max dates from the dataset for the filter's default range
min_date = df['date'].min().date()
max_date = df['date'].max().date()

# Create the date input widgets
start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Create a slider for the Top N Clients (US-4)
top_n = st.sidebar.slider("Select Top 'N' Clients (US-4)", min_value=5, max_value=20, value=10, step=1)

# --- 3. Run All Feature Functions (The "Engine") ---
# We must convert the dates from the widgets back to timestamps for Pandas
start_date_ts = pd.to_datetime(start_date)
end_date_ts = pd.to_datetime(end_date)

# Call all 5 feature functions one time with the filtered dates
# This is efficient and provides all the data we need to display
kpi_data = get_summary_kpis(df, start_date_ts, end_date_ts)              # US-2
cash_flow_data = get_net_cash_flow(df, start_date_ts, end_date_ts)       # US-1
type_dist_data = get_distribution_by_type(df, start_date_ts, end_date_ts) # US-3
top_clients_data = get_top_clients(df, start_date_ts, end_date_ts, n=top_n) # US-4
temporal_trend_data = get_temporal_trend(df, start_date_ts, end_date_ts) # US-5

# --- 4. Display Dashboard (The "UI") ---

# Section 1: KPI Summary Cards (US-2)
st.header(f"Key Metrics ({start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')})")

# Get the data from the nested dictionary
k_overall = kpi_data['overall']
k_credit = kpi_data['credit']
k_debit = kpi_data['debit']
k_transfer = kpi_data['transfer']

# Display the "Overall" KPIs in columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Transaction Amount", f"${k_overall['total_amount']:,.2f}")
col2.metric("Total Transactions", f"{k_overall['total_transactions']:,}")
col3.metric("Avg. Transaction Amount", f"${k_overall['avg_transaction']:,.2f}")

st.divider()

# Display the "By Type" KPIs in columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Inflow (Credit)", f"${k_credit['total_amount']:,.2f}", f"{k_credit['total_transactions']:,} transactions")
col2.metric("Total Outflow (Debit)", f"${k_debit['total_amount']:,.2f}", f"{k_debit['total_transactions']:,} transactions")
col3.metric("Total Transferred", f"${k_transfer['total_amount']:,.2f}", f"{k_transfer['total_transactions']:,} transactions")


# Section 2: Charts and Data Tables (US-1, US-3, US-4, US-5)
st.header("Detailed Analysis")

# Use tabs to organize the charts cleanly
tab1, tab2, tab3 = st.tabs(["📈 Net Cash Flow (US-1)", "📊 Transaction Analysis (US-3 & US-5)", "👥 Customer Insights (US-4)"])

with tab1:
    st.subheader("Monthly Net Cash Flow (Inflow vs. Outflow)")
    
    # Check if the dataframe is empty
    if cash_flow_data.empty:
        st.warning("No credit or debit transactions found for this date range.")
    else:
        # Use st.area_chart to show Inflow (green) vs. Outflow (red)
        # We must set the index to the date column for Streamlit charts
        st.area_chart(
            cash_flow_data.set_index('month_year'),
            y=['inflow', 'outflow'],
            color=["#00FF00", "#FF0000"] # Custom colors
        )
        st.dataframe(cash_flow_data, use_container_width=True)

with tab2:
    st.subheader("Total Transaction Amount Over Time (US-5)")
    
    # Check if the dataframe is empty
    if temporal_trend_data.empty:
        st.warning("No transactions of any type found for this date range.")
    else:
        # Use st.line_chart to show the overall trend
        st.line_chart(temporal_trend_data.set_index('month_year'), y='amount')
    
    st.divider()
    
    st.subheader("Transaction Distribution by Type (US-3)")
    
    # Check if the dataframe is empty
    if type_dist_data.empty:
        st.warning("No transactions found for this date range.")
    else:
        # Use st.bar_chart for the distribution
        st.bar_chart(type_dist_data.set_index('type'), y='amount_sum')
        st.dataframe(type_dist_data, use_container_width=True)


with tab3:
    st.subheader(f"Top {top_n} Clients by Total Amount (US-4)")
    
    # Check if the dataframe is empty
    if top_clients_data.empty:
        st.warning("No client transactions found for this date range.")
    else:
        # Display the Top N clients as a table
        st.dataframe(top_clients_data, use_container_width=True)
        
        # Also display a bonus bar chart
        st.bar_chart(top_clients_data.set_index('customer_id'), y='total_amount')