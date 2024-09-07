import sqlite3

#Dateiname anpassen für die AOL Request Daten
input_filenames = ['user-ct-test-collection-01.txt', 'user-ct-test-collection-02.txt', 'user-ct-test-collection-03.txt', 'user-ct-test-collection-04.txt', 'user-ct-test-collection-05.txt', 'user-ct-test-collection-06.txt', 'user-ct-test-collection-07.txt', 'user-ct-test-collection-08.txt', 'user-ct-test-collection-09.txt', 'user-ct-test-collection-10.txt']

#Verbindungsaufbau mit Datenbank
conn = sqlite3.connect('search_queries.db')
#Erstellt den Cursor für die Datenbankoperation
cursor = conn.cursor()
#Bereitet die Datenbank operation für die Erstellung der Tabelle vor
cursor.execute('''
CREATE TABLE IF NOT EXISTS search_queries (
    AnonID INTEGER,
    Query TEXT,
    QueryTime TEXT,
    ItemRank INTEGER,
    ClickURL TEXT
)
''')

#oeffnet die txt Datei
for file_name in input_filenames:
    file = open(file_name, 'r', encoding='utf-8')
    next(file)  # Überspringe die Headerzeile
    for line in file:
        #trennt die Zeile mit dem vorgegeben Zeichen auf
        data = line.split('\t')
        # Fehlende Werte mit leere String ersetzen
        data = [d if d != '\n' else '' for d in data]
        # String die \n beinhalten wird \n entfernt
        data = [d if not '\n' in d else d.replace("\n", "") for d in data]

        if len(data) == 5:
            #bereitet die Datenbank operation für die Erstellung von einem Datensatz in die Tabelle mit den Werten von der txt Datei
            cursor.execute('''
            INSERT INTO search_queries (AnonID, Query, QueryTime, ItemRank, ClickURL)
            VALUES (?, ?, ?, ?, ?)
            ''', data)
        else:
            print(f"Ungültige Datenzeile: {data}")

#sendet alle vorbereiteten Operationen an die Datenbank
conn.commit()
#schließt die Datenbank
conn.close()

print("Daten erfolgreich in die SQL-Datenbank importiert.")
