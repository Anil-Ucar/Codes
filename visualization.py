import matplotlib.pyplot as plt
from pathlib import Path

def plot_most_common_queries(data, save_path=None):
    # Leere Werte in 'Query' entfernen
    data = data.dropna(subset=['Query'])
    data = data[data['Query'].str.strip() != "-"]
    # Top 10 häufigste Suchanfragen ermitteln
    most_common_queries = data['Query'].value_counts().head(10)
    
    # Diagramm erstellen
    plt.figure(figsize=(12, 6))
    most_common_queries.plot(kind='bar')
    plt.title('Top 10 Most Common Queries')
    plt.xlabel('Queries')
    plt.ylabel('Frequency')
    
    # Layout anpassen, um abgeschnittene Beschriftungen zu vermeiden
    plt.tight_layout()

    # Diagramm anzeigen oder speichern
    if save_path:
        save_path = Path(save_path)
        plt.savefig(save_path)
    else:
        plt.show()
