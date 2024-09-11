import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import sqlite3
import threading
import csv

# Verbindung zur SQLite-Datenbank herstellen
def connect_db():
    return sqlite3.connect('search_queries.db')

# Funktion zum Anzeigen der letzten 10 Suchabfragen
def show_last_queries():
    start_loading()  # Ladebalken starten
    threading.Thread(target=fetch_last_queries).start()  # Datenabfrage in einem separaten Thread

def fetch_last_queries():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Nur Suchanfragen abrufen, die kein "-" enthalten
        cursor.execute("SELECT AnonID, Query, QueryTime FROM search_queries WHERE Query != '-' ORDER BY QueryTime DESC LIMIT 10")
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
        stop_loading()  # Ladebalken stoppen

# Funktion zum Analysieren der grundlegenden Statistiken
def analyze_statistics():
    start_loading()  # Ladebalken starten
    threading.Thread(target=perform_analysis).start()  # Analyse in einem separaten Thread

def perform_analysis():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Gesamtanzahl der Suchanfragen ohne "-"
        cursor.execute("SELECT COUNT(*) FROM search_queries WHERE Query != '-'")
        total_queries = cursor.fetchone()[0]

        # Anzahl der eindeutigen Nutzer
        cursor.execute("SELECT COUNT(DISTINCT AnonID) FROM search_queries WHERE Query != '-'")
        unique_users = cursor.fetchone()[0]

        # Die häufigsten Suchanfragen ohne "-"
        cursor.execute("SELECT Query, COUNT(*) as count FROM search_queries WHERE Query != '-' GROUP BY Query ORDER BY count DESC LIMIT 10")
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
        stop_loading()  # Ladebalken stoppen

# Funktion zum gezielten Suchen nach AnonID, Query oder QueryTime
def search_data():
    start_loading()  # Ladebalken starten
    threading.Thread(target=perform_search).start()  # Suche in einem separaten Thread

def perform_search():
    search_term = search_entry.get()
    search_by = search_option.get()
    
    if not search_term:
        messagebox.showerror("Fehler", "Bitte einen Suchbegriff eingeben.")
        stop_loading()
        return
    
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = f"SELECT AnonID, Query, QueryTime FROM search_queries WHERE {search_by} LIKE ? AND Query != '-'"
        cursor.execute(query, ('%' + search_term + '%',))
        queries = cursor.fetchall()

        treeview.delete(*treeview.get_children())

        if queries:
            for query in queries:
                treeview.insert('', 'end', values=(query[0], query[1], query[2]))
        else:
            messagebox.showinfo("Info", "Keine Übereinstimmungen gefunden.")

    except Exception as e:
        messagebox.showerror("Fehler", str(e))
    finally:
        conn.close()
        stop_loading()  # Ladebalken stoppen

# Funktion zum Exportieren der Daten in eine CSV-Datei
def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    
    if not file_path:
        return  # Falls kein Pfad ausgewählt wird, abbrechen
    
    # Daten aus der Treeview abrufen
    data = []
    for row_id in treeview.get_children():
        row = treeview.item(row_id)['values']
        data.append(row)
    
    # Daten in die CSV-Datei schreiben
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['AnonID', 'Query', 'QueryTime'])  # Spaltennamen schreiben
        writer.writerows(data)  # Daten schreiben
    
    messagebox.showinfo("Erfolg", "Daten wurden erfolgreich exportiert.")

# Funktionen zum Starten und Stoppen des Ladebalkens
def start_loading():
    progress_bar.start()
    progress_bar.pack(pady=10)

def stop_loading():
    progress_bar.stop()
    progress_bar.pack_forget()

# Tkinter-Setup
root = tk.Tk()
root.title("Suchabfrage-Analyse mit SQLite")
root.geometry("800x600")

# Buttons
btn_last_queries = tk.Button(root, text="Letzte 10 Suchanfragen anzeigen", command=show_last_queries)
btn_last_queries.pack(pady=10)

btn_analyze_stats = tk.Button(root, text="Statistiken analysieren", command=analyze_statistics)
btn_analyze_stats.pack(pady=10)

btn_export_csv = tk.Button(root, text="Daten als CSV exportieren", command=export_to_csv)
btn_export_csv.pack(pady=10)

# Sucheingabe und Suchoptionen
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Suchen nach:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

search_option = tk.StringVar(value="Query")
search_option_menu = ttk.Combobox(search_frame, textvariable=search_option, values=["AnonID", "Query", "QueryTime"])
search_option_menu.pack(side=tk.LEFT, padx=5)

btn_search = tk.Button(search_frame, text="Suchen", command=search_data)
btn_search.pack(side=tk.LEFT, padx=5)

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

# Ladebalken (Progressbar)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")

# Hauptschleife der GUI
root.mainloop()