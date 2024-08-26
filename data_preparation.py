import os
import pandas as pd
from pathlib import Path

def load_data(file_path):
    # Sicherstellen, dass der Pfad ein Path-Objekt ist, falls es als String übergeben wurde
    file_path = Path(file_path)
    column_names = ['AnonID', 'Query', 'QueryTime', 'ItemRank', 'ClickURL']
    data = pd.read_csv(file_path, sep='\t', names=column_names, encoding='utf-8')
    return data

def clean_data(data):
    # Entfernen von NaN-Einträgen in der Spalte 'Query'
    data = data.dropna(subset=['Query'])
    return data
