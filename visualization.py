import matplotlib.pyplot as plt
from pathlib import Path

def plot_most_common_queries(data, save_path=None):
    try:
        # Ungültige oder leere Werte in der 'Query'-Spalte entfernen
        data = data.dropna(subset=['Query'])
        
        # Entfernen von Einträgen, bei denen die 'Query'-Spalte ein "-" enthält
        data = data[data['Query'].str.strip() != "-"]
        
        # Die häufigsten Suchanfragen bestimmen
        most_common_queries = data['Query'].value_counts().head(10)

        # Überprüfen, ob es Daten zum Plotten gibt
        if most_common_queries.empty:
            print("Keine Daten zum Plotten vorhanden.")
            return
        
        # Diagramm erstellen
        plt.figure(figsize=(12, 6))
        most_common_queries.plot(kind='bar')
        plt.title('Top 10 Most Common Queries')
        plt.xlabel('Queries')
        plt.ylabel('Frequency')
        plt.tight_layout()

        # Diagramm speichern oder anzeigen
        if save_path:
            save_path = Path(save_path)
            plt.savefig(save_path)
        else:
            plt.show()  # Diagramm anzeigen
        
    except KeyError as e:
        print(f"Fehler: Die Spalte {e} wurde in den Daten nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist bei der Erstellung der Visualisierung aufgetreten: {e}")
