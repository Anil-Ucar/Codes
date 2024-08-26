import os
import pandas as pd
from pathlib import Path

def load_clean_data(file_path):
    file_path = Path(file_path)  # Pfad sicherstellen
    data = pd.read_csv(file_path)
    return data

def analyze_basic_statistics(data):
    total_queries = len(data)
    unique_users = data['AnonID'].nunique()
    most_common_queries = data['Query'].value_counts().head(10)
    return total_queries, unique_users, most_common_queries

if __name__ == "__main__":
    # Dynamischer Pfad relativ zum Skriptstandort
    base_path = Path(__file__).parent
    file_path = base_path / 'user-ct-test-collection-01.txt'
    
    # Daten laden und analysieren
    data = load_clean_data(file_path)
    total_queries, unique_users, most_common_queries = analyze_basic_statistics(data)
    
    # Ergebnisse anzeigen
    print(f'Total Queries: {total_queries}')
    print(f'Unique Users: {unique_users}')
    print('Most Common Queries:')
    print(most_common_queries)
najksdbakjsbdas