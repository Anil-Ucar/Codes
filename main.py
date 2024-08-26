# Hauptprogramm (main.py)
import os
from pathlib import Path
from data_preparation import load_data, clean_data
from analysis import analyze_basic_statistics
from visualization import plot_most_common_queries

if __name__ == "__main__":
    # Dynamische Pfade relativ zum aktuellen Skript
    base_path = Path(os.path.dirname(__file__)).parent # Der Ordner, in dem sich das Skript befindet
    raw_data_path = str(base_path) + '/user-ct-test-collection-01.txt'
    cleaned_data_path = str(base_path) + '/user-ct-test-collection-01.csv'
    
    # Datenvorbereitung
    data = load_data(raw_data_path)
    data = clean_data(data)
    data.to_csv(cleaned_data_path, index=False)
    
    # Datenanalyse
    total_queries, unique_users, most_common_queries = analyze_basic_statistics(data)
    print(f'Total Queries: {total_queries}')
    print(f'Unique Users: {unique_users}')
    print('Most Common Queries:')
    print(most_common_queries)
    
    # Datenvisualisierung
    plot_most_common_queries(data)