import os
import pandas as pd

def analyze_basic_statistics(data):
    try:
        # Entfernen von ungültigen oder leeren Werten in 'Query'
        data = data[data['Query'].str.strip() != "-"]
        data = data.dropna(subset=['Query'])
        
        # Berechnung der grundlegenden Statistiken
        total_queries = len(data)
        unique_users = data['AnonID'].nunique()
        most_common_queries = data['Query'].value_counts().head(10)
        
        return total_queries, unique_users, most_common_queries
    
    except KeyError as e:
        print(f"Fehler: Die erwartete Spalte {e} wurde in den Daten nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist bei der Datenanalyse aufgetreten: {e}")