import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

@anvil.server.callable
def Query_Get_Kursuebersicht():
    sql = """ SELECT Kurse.Kurs_id AS kurs_id, Kurse.Bezeichnung AS kurs, Kurse.Wochentag AS wochentag, Kurse.Uhrzeit AS uhrzeit, Trainer.Vorname || Trainer.Nachname AS trainer, count(Anmelden.Kurs_id) 
    || "/" || Kurse.Max_teilnehmer AS teilnehmer FROM Kurse
    JOIN Trainer 
    ON Trainer.Trainer_id = Kurse.Trainer_id
    JOIN Anmelden
    ON Anmelden.Kurs_id = Kurse.Kurs_id
    GROUP BY Kurse.Bezeichnung"""
    with sqlite3.connect(data_files["Nageler_Dominik_Fitnesstudio.db"]) as conn:
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      result = cur.execute(sql).fetchall()
    return [dict(row) for row in result]

@anvil.server.callable
def Query_Get_Mitglieder(kurs_id:str):
    sql = f"""SELECT Anmelden.Kurs_id AS kurs_id ,Mitglied.Mitglied_id AS mitglied_id,  Mitglied.Vorname || Mitglied.Nachname AS mitglied FROM Mitglied
    JOIN Anmelden 
    ON Mitglied.Mitglied_id = Anmelden.Mitglied_id
    WHERE Anmelden.Kurs_id != {kurs_id}"""
    with sqlite3.connect(data_files["Nageler_Dominik_Fitnesstudio.db"]) as conn:
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      result = cur.execute(sql).fetchall()
    return [dict(row) for row in result]



@anvil.server.callable
def Query_Insert_Mitglied(Mitglied_id:str, kurs_id: str):
  sql = f"INSERT INTO Anmelden (Kurs_id,Mitglied_id,Anmeldedatum) VALUES ({kurs_id},{Mitglied_id},2024-04-01)"
  with sqlite3.connect(data_files["Nageler_Dominik_Fitnesstudio.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(sql).fetchall()
  return [dict(row) for row in result]

  