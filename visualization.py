import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

def plot_most_common_queries(data, save_path=None):
    try:
        # Ungültige oder leere Werte in der 'Query'-Spalte entfernen
        data = data.dropna(subset=['Query'])

        # Entferne alle Queries, die nur ein "-" enthalten
        data = data[data['Query'].str.strip() != "-"]

        most_common_queries = data['Query'].value_counts().head(10)

        # Überprüfen, ob es Daten zum Plotten gibt
        if most_common_queries.empty:
            print("Keine Daten zum Plotten vorhanden.")
            return
        
        # Farbenpalette von Seaborn verwenden
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 8))

        # Diagramm erstellen
        ax = sns.barplot(x=most_common_queries.index, y=most_common_queries.values, palette="muted")

        # Titel und Achsenbeschriftungen
        plt.title('Top 10 Most Common Queries', fontsize=16)
        plt.xlabel('Queries', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)  # X-Achsen-Beschriftung schräg stellen

        # Die Werte über den Balken anzeigen
        for index, value in enumerate(most_common_queries.values):
            ax.text(index, value, f'{value}', ha='center', va='bottom', fontsize=12)

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
