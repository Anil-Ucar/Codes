import os
import pandas as pd
from pathlib import Path

def load_clean_data(file_path):
    try:
        file_path = Path(file_path)  # Pfad sicherstellen
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Fehler: Die Datei {file_path} wurde nicht gefunden.")
    except pd.errors.EmptyDataError:
        print("Fehler: Die Datei ist leer.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist beim Laden der Daten aufgetreten: {e}")

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

if __name__ == "__main__":
    # Dynamischer Pfad relativ zum Skriptstandort
    base_path = Path(__file__).parent
    file_path = base_path / 'user-ct-test-collection-01.txt'
    
    # Daten laden und analysieren
    data = load_clean_data(file_path)
    if data is not None:  # Prüfen, ob Daten erfolgreich geladen wurden
        total_queries, unique_users, most_common_queries = analyze_basic_statistics(data)
        
        # Ergebnisse anzeigen
        print(f'Total Queries: {total_queries}')
        print(f'Unique Users: {unique_users}')
        print('Most Common Queries:')
        print(most_common_queries)
