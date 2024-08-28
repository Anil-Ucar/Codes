import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
def connect_db():
    return sqlite3.connect('search_queries.db')

# Funktion zum Anzeigen der letzten 10 Suchabfragen
def show_last_queries():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT AnonID, Query, QueryTime FROM search_queries ORDER BY QueryTime DESC LIMIT 10")
        queries = cursor.fetchall()

        treeview.delete(*treeview.get_children())

        if queries:
            for query in queries:
                treeview.insert('', 'end', values=(query[0], query[1], query[2]))
        else:
            messagebox.showinfo("Info", "Keine Suchanfragen gefunden.")

    except sqlite3.DatabaseError as e:
        messagebox.showerror("Fehler", f"Ein Datenbankfehler ist aufgetreten: {e}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        conn.close()


# Funktion zum Analysieren der grundlegenden Statistiken
def analyze_statistics():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Gesamtanzahl der Suchanfragen
        cursor.execute("SELECT COUNT(*) FROM search_queries")
        total_queries = cursor.fetchone()[0]

        # Anzahl der eindeutigen Nutzer
        cursor.execute("SELECT COUNT(DISTINCT AnonID) FROM search_queries")
        unique_users = cursor.fetchone()[0]

        # Die häufigsten Suchabfragen
        cursor.execute("SELECT Query, COUNT(*) as count FROM search_queries GROUP BY Query ORDER BY count DESC LIMIT 10")
        common_queries = cursor.fetchall()

        # Statistiken anzeigen
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Gesamtzahl der Suchanfragen: {total_queries}\n")
        result_text.insert(tk.END, f"Einzigartige Nutzer: {unique_users}\n\n")
        result_text.insert(tk.END, "Häufigste Suchanfragen:\n")
        for query in common_queries:
            result_text.insert(tk.END, f"{query[0]} (Anzahl: {query[1]})\n")

    except Exception as e:
        messagebox.showerror("Fehler", str(e))

    finally:
        conn.close()

# Funktion zum Anzeigen aller Daten der Datenbank (Vorsicht bei großen Datensätzen!)
def show_all_data():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM search_queries LIMIT 100")  # Begrenze die Ausgabe auf 100 Datensätze
        queries = cursor.fetchall()

        # Treeview leeren
        treeview.delete(*treeview.get_children())

        if queries:
            for query in queries:
                treeview.insert('', 'end', values=query[1:])  # Werte korrekt einfügen, beginnend ab der zweiten Spalte
        else:
            messagebox.showinfo("Info", "Keine Daten gefunden.")

    except Exception as e:
        messagebox.showerror("Fehler", str(e))

    finally:
        conn.close()

# Tkinter-Setup
root = tk.Tk()
root.title("Suchabfrage-Analyse mit SQLite")
root.geometry("800x600")

# Buttons
btn_last_queries = tk.Button(root, text="Letzte 10 Suchanfragen anzeigen", command=show_last_queries)
btn_last_queries.pack(pady=10)

btn_analyze_stats = tk.Button(root, text="Statistiken analysieren", command=analyze_statistics)
btn_analyze_stats.pack(pady=10)

btn_show_all = tk.Button(root, text="Alle Daten anzeigen (limitiert)", command=show_all_data)
btn_show_all.pack(pady=10)

# Treeview für strukturierte Datenanzeige
columns = ('AnonID', 'Query', 'QueryTime')  # Definiere die Spalten
treeview = ttk.Treeview(root, columns=columns, show='headings')
treeview.heading('AnonID', text='AnonID')
treeview.heading('Query', text='Query')
treeview.heading('QueryTime', text='Time')
treeview.pack(pady=10, fill=tk.BOTH, expand=True)

# Textfeld für die Statistikausgabe
result_text = tk.Text(root, height=10, width=100)
result_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Hauptschleife der GUI
root.mainloop()
