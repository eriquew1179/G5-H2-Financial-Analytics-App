# File: src/features/summary_kpis.py
import pandas as pd

def get_summary_kpis(df: pd.DataFrame) -> dict:
    """
    Calculates the main summary KPIs from the transaction data.
    
    Args:
        df: The cleaned financial transactions DataFrame.
        
    Returns:
        A dictionary containing the summary KPIs.
    """
    
    # 1. Calculate Total Amount
    total_amount = df['amount'].sum()
    
    # 2. Calculate Total Transactions
    total_transactions = len(df)
    
    # 3. Calculate Average Transaction
    avg_transaction = df['amount'].mean()
    
    # 4. Return as a dictionary (as per Acceptance Criteria)
    kpi_dict = {
        "total_amount": total_amount,
        "total_transactions": total_transactions,
        "avg_transaction": avg_transaction
    }
    
    return kpi_dict

# --- Bloque de prueba (Opcional pero recomendado) ---
# Esto te permite probar tu función antes de que el dashboard exista.
# Solo se ejecutará si corres este archivo directamente: python src/features/summary_kpis.py
if __name__ == "__main__":
    
    # Importar el data loader para probar
    # Nota: Estamos subiendo un nivel (..) para encontrar src/data_loader.py
    import sys
    import os
    
    # Esta magia nos permite importar desde la carpeta 'src'
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_loader import load_data
    
    # Carga los datos (asegúrate de que el CSV esté en tu carpeta 'data')
    df = load_data('data/financial_transactions.csv')
    
    if not df.empty:
        # Prueba tu función de KPI
        kpis = get_summary_kpis(df)
        print("--- Testing KPI Function ---")
        print(kpis)
        print("----------------------------")
    else:
        print("Could not load data for testing.")