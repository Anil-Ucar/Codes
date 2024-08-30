import os
import pandas as pd
from pathlib import Path
from data_preparation import load_data, clean_data
from analysis import analyze_basic_statistics
from visualization import plot_most_common_queries

if __name__ == "__main__":
    try:
        # Dynamischer Pfad relativ zum aktuellen Skript
        base_path = Path(os.path.dirname(__file__)).parent
        
        # Liste der Textdateien, die geladen werden sollen
        file_names = [
            'user-ct-test-collection-01.txt',
            'user-ct-test-collection-02.txt',
            'user-ct-test-collection-03.txt',
            'user-ct-test-collection-04.txt',
            'user-ct-test-collection-05.txt',
            'user-ct-test-collection-06.txt',
            'user-ct-test-collection-07.txt',
            'user-ct-test-collection-08.txt',
            'user-ct-test-collection-09.txt',
            'user-ct-test-collection-10.txt'
        ]

        # Liste für die gesammelten Daten
        combined_data = pd.DataFrame()

        # Schleife über alle Dateien und Daten laden und bereinigen
        for file_name in file_names:
            file_path = base_path / file_name
            data = load_data(file_path)
            if data is not None and not data.empty:
                data = clean_data(data)
                combined_data = pd.concat([combined_data, data], ignore_index=True)
            else:
                print(f"Fehler: Die Datei {file_path} konnte nicht geladen werden oder enthält keine Daten.")

        # Überprüfen, ob Daten geladen wurden
        if combined_data.empty:
            raise ValueError("Es wurden keine gültigen Daten geladen.")

        # Datenanalyse
        total_queries, unique_users, most_common_queries = analyze_basic_statistics(combined_data)
        print(f'Total Queries: {total_queries}')
        print(f'Unique Users: {unique_users}')
        print('Most Common Queries:')
        print(most_common_queries)

        # Datenvisualisierung
        plot_most_common_queries(combined_data)

    except FileNotFoundError as e:
        print(f"Fehler: {e}")
    except ValueError as e:
        print(f"Fehler: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
