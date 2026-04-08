import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (wird erstellt, falls nicht vorhanden)
conn = sqlite3.connect('Nageler_Dominik_Fitnesstudio.db')
cursor = conn.cursor()

# Fremdschlüssel-Unterstützung in SQLite aktivieren
cursor.execute("PRAGMA foreign_keys = ON;")

# ==========================================
# 1. TABELLEN ERSTELLEN
# ==========================================

cursor.executescript('''
   

    -- Trainer Tabelle (Kurs_id FK entfernt)
    CREATE TABLE IF NOT EXISTS Trainer (
        Trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Vorname VARCHAR(50),
        Nachname VARCHAR(50),
        Spezialgebiet VARCHAR(200)
    );

  
    CREATE TABLE IF NOT EXISTS Kurse (
        Kurs_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Bezeichnung VARCHAR(100),
        Uhrzeit DATETIME,
        Wochentag VARCHAR(50),
        Max_teilnehmer INTEGER,
        Trainer_id INTEGER,
        FOREIGN KEY (Trainer_id) REFERENCES Trainer(Trainer_id)
    );

    -- Mitglied Tabelle
    CREATE TABLE IF NOT EXISTS Mitglied (
        Mitglied_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Vorname VARCHAR(50),
        Nachname VARCHAR(50),
        Email VARCHAR(150),
        Beitrittsdatum DATE
    );

    -- Anmelden Tabelle (Junction Table)
    CREATE TABLE IF NOT EXISTS Anmelden (
        Anmelde_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Kurs_id INTEGER,
        Mitglied_id INTEGER,
        Anmeldedatum DATE,
        FOREIGN KEY (Kurs_id) REFERENCES Kurse(Kurs_id),
        FOREIGN KEY (Mitglied_id) REFERENCES Mitglied(Mitglied_id)
    );
''')

# ==========================================
# 2. BEISPIELDATEN EINFÜGEN
# ==========================================



# >= 3 Trainer
trainer_daten = [
    ('Max', 'Mustermann', 'Yoga & Pilates'),
    ('Anna', 'Schmidt', 'HIIT & Krafttraining'),
    ('Lukas', 'Müller', 'Ausdauer & Spinning'),
    ('Sarah', 'Weber', 'Reha & Rücken')
]
cursor.executemany("INSERT INTO Trainer (Vorname, Nachname, Spezialgebiet) VALUES (?, ?, ?);", trainer_daten)

# >= 5 Kurse (Verknüpft mit Fitnessstudio 1 und verschiedenen Trainern)
kurse_daten = [
    ('Morning Yoga', '08:00:00', 'Montag', 15,  1),      # Trainer 1
    ('Power HIIT', '18:30:00', 'Dienstag', 20,  2),      # Trainer 2
    ('Spinning Intense', '19:00:00', 'Mittwoch', 12, 3),# Trainer 3
    ('Rückenfit', '10:00:00', 'Donnerstag', 15,  4),     # Trainer 4
    ('Pilates Basic', '17:00:00', 'Freitag', 15,  1),    # Trainer 1
    ('Zirkeltraining', '18:00:00', 'Samstag', 25,  2)    # Trainer 2
]
cursor.executemany("INSERT INTO Kurse (Bezeichnung, Uhrzeit, Wochentag, Max_teilnehmer, Trainer_id) VALUES (?, ?, ?, ?, ?);", kurse_daten)

# >= 6 Mitglieder
mitglieder_daten = [
    ('Julia', 'Meier', 'julia.m@example.com', '2023-01-15'),
    ('Tom', 'Bauer', 'tom.b@example.com', '2023-03-20'),
    ('Lisa', 'Wagner', 'lisa.w@example.com', '2023-05-11'),
    ('Felix', 'Hoffmann', 'felix.h@example.com', '2023-08-01'),
    ('Laura', 'Becker', 'laura.b@example.com', '2023-10-12'),
    ('Kevin', 'Schulz', 'kevin.s@example.com', '2024-01-05'),
    ('Mia', 'Koch', 'mia.k@example.com', '2024-02-28')
]
cursor.executemany("INSERT INTO Mitglied (Vorname, Nachname, Email, Beitrittsdatum) VALUES (?, ?, ?, ?);", mitglieder_daten)

# >= 8 Anmeldungen (Welches Mitglied nimmt an welchem Kurs teil?)
anmeldungen_daten = [
    (1, 1, '2024-04-01'), # Julia bei Morning Yoga
    (2, 1, '2024-04-02'), # Tom bei Power HIIT
    (3, 2, '2024-04-02'), # Lisa bei Spinning Intense
    (4, 3, '2024-04-03'), # Felix bei Rückenfit
    (5, 4, '2024-04-04'), # Laura bei Pilates Basic
    (6, 5, '2024-04-05'), # Kevin bei Zirkeltraining
    (1, 6, '2024-04-05'), # Julia zusätzlich bei Zirkeltraining
    (3, 4, '2024-04-06'), # Lisa zusätzlich bei Pilates Basic
    (5, 1, '2024-04-06'), # Laura zusätzlich bei Morning Yoga
]
cursor.executemany("INSERT INTO Anmelden (Kurs_id, Mitglied_id, Anmeldedatum) VALUES (?, ?, ?);", anmeldungen_daten)

# Änderungen speichern und Verbindung schließen
conn.commit()
print("Datenbank 'fitnessstudio.db' wurde erfolgreich erstellt und mit Beispieldaten gefüllt!")

# Überprüfungsausgabe
cursor.execute("SELECT COUNT(*) FROM Trainer;")
print(f"Anzahl Trainer: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM Kurse;")
print(f"Anzahl Kurse: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM Mitglied;")
print(f"Anzahl Mitglieder: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM Anmelden;")
print(f"Anzahl Anmeldungen: {cursor.fetchone()[0]}")

conn.close()