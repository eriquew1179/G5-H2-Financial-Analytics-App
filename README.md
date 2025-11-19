
# Group 5 - Homework 2 - Financial Analytics App
# G5-H2 Financial Analytics App

This project is a strategic financial analysis dashboard built by our 4-person student team (Group 5, Homework 2). It ingests a CSV of financial transactions and presents a one-page, interactive web dashboard for business stakeholders.

The application is built with **Python**, **matplotlib**, **Streamlit**, and **Pandas**.

The project is managed using a 2-sprint Scrum methodology and a feature-branch Git workflow. All code, comments, and documentation are in English.


🚀 How to Run This Project

To run this dashboard locally, you only need to follow 3 steps.

1. Get the Code

Clone this repository to your local machine:

git clone [https://github.com/eriquew1179/G5-H2-Financial-Analytics-App.git](https://github.com/eriquew1179/G5-H2-Financial-Analytics-App.git)
cd G5-H2-Financial-Analytics-App

## Project Setup & Installation
2. Set Up Your Environment

This will create a virtual environment and install all the necessary packages from requirements.txt.
# Create the environment
python -m venv venv

# Activate on Windows (PowerShell/CMD)
.\venv\Scripts\activate

# Activate on macOS/Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

**Add the data:**
    This project uses `financial_transactions.csv`. Due to its size, it is *not* tracked by Git. You must **place your local copy** of `financial_transactions.csv` inside the `/data/` folder.

## Run the Dashboard
3. Run the Dashboard

Before running, place your financial_transactions.csv file inside the /data/ folder.

Once the file is in place, run the following command:

streamlit run app.py


Streamlit will open the application in your default web browser.

## Features

Based on our defined User Stories, the dashboard will deliver the following strategic insights:

* **US-1: Net Cash Flow:** An area chart visualizing total "Inflow" (credits) vs. "Outflow" (debits) over time to monitor liquidity.
* **US-2: Summary KPIs:** "At-a-glance" summary cards for Total Transaction Amount, Total Transaction Count, and Average Transaction Value.
* **US-3: Transaction Type Analysis:** A bar chart breaking down transaction volume and value by type (credit, debit, transfer).
* **US-4: Temporal Trend Analysis:** A line chart showing total transaction value by month to identify seasonal trends and growth.
* **US-5: Top Client Analysis:** A table identifying the Top 10 most valuable customers by total spending.

## dashboard Features

The final dashboard integrates all 6 of our project's User Stories:

- Interactive Date-Range Filter: All metrics and charts are fully interactive and update based on the date range selected in the sidebar.

- KPI Summary Cards (US-2): "At-a-glance" cards for overall performance, as well as a breakdown by Inflow (Credit), Outflow (Debit), and Transfers.

- Net Cash Flow Chart (US-1): A monthly area chart that visualizes the "Inflow vs. Outflow" battle, allowing managers to monitor liquidity.

- Temporal Trend Chart (US-5): A line chart showing the total transaction amount over time to identify growth and seasonality.

- Transaction Type Chart (US-3): A bar chart that shows the total value and volume for each transaction type.

- Top N Clients Table (US-4): An interactive table and chart showing the most valuable customers, with a slider to select the Top 'N' clients.



## Project Architecture

To prevent merge conflicts and ensure parallel development, we use the following file structure. **Students must only edit files in their assigned feature module.**

```
financial-analysis-app/
│
├── .gitignore
├── data/
│   └── financial_transactions.csv  (NOT in Git)
├── src/
│   ├── __init__.py
│   ├── data_loader.py       (Completed in Sprint 0)
│   └── features/            (Sprint 1 Logic)
│       ├── __init__.py
│       ├── net_cash_flow.py   
│       ├── summary_kpis.py    
│       ├── temporal_trend.py  
│       └── customer_analysis.py 
├── app.py                   (Sprint 2 - UI)
└── requirements.txt
```

## Sprint Goals

### Sprint 0: Setup (Scrum Master)
* **Goal:** Prepare the project for parallel development.
* **Tasks:** Initialize Git repo, create branches, implement `data_loader.py`, and create the full file skeleton.

### Sprint 1: Feature Logic Development
* **Goal:** Build all business logic in isolation.
* **Tasks:** All developers work in parallel on their assigned feature branches and `.py` files. The `app.py` file is **not** touched.

### Sprint 2: Integration & Dashboard
* **Goal:** Deliver a single, unified dashboard (US-6).
* **Tasks:** The UI Lead integrates all feature modules into `app.py`. All other developers are on support/bug-fix duty.