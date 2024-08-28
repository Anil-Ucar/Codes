import os
import pandas as pd
from pathlib import Path

def load_data(file_path):
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Die Datei {file_path} wurde nicht gefunden.")
        column_names = ['AnonID', 'Query', 'QueryTime', 'ItemRank', 'ClickURL']
        data = pd.read_csv(file_path, sep='\t', names=column_names, encoding='utf-8')
        return data
    except FileNotFoundError as e:
        print(f"Fehler: {e}")
        # Alternativ: raise e, um den Fehler weiterzugeben
    except pd.errors.ParserError as e:
        print(f"Fehler beim Parsen der Datei: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

def clean_data(data):
    try:
        data = data.dropna(subset=['Query'])
        return data
    except KeyError as e:
        print(f"Fehler: Die Spalte {e} wurde in den Daten nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist beim Bereinigen der Daten aufgetreten: {e}")
