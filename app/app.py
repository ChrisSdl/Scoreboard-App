# app.py
from flask import Flask, render_template, jsonify
import sqlite3
import time
import os

app = Flask(__name__)

DB_FILE = "app/scoreboard.db"

# ==================== Datenbank initialisieren ====================
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE scoreboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Team TEXT NOT NULL,
                Punkte INTEGER NOT NULL,
                Bild TEXT
            )
        """)
        # Beispiel-Daten
        cursor.executemany("""
            INSERT INTO scoreboard (Team, Punkte, Bild) VALUES (?, ?, ?)
        """, [
            ("Team A", 120, "team_a.png"),
            ("Team B", 100, "team_b.png"),
            ("Team C", 80, "team_c.png"),
        ])
        conn.commit()
        conn.close()
        print("Datenbank erstellt und initialisiert.")

# ==================== Daten laden ====================
def load_data():
    time.sleep(0.05)  # kleine Pause
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT Team, Punkte, Bild FROM scoreboard")
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    # Punkte sicher numerisch
    for row in data:
        row["Punkte"] = int(row.get("Punkte", 0))

    # Sortieren & Rang berechnen
    data.sort(key=lambda x: x["Punkte"], reverse=True)
    for i, row in enumerate(data, start=1):
        row["Rank"] = i

    return data

# ==================== Flask Routen ====================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    data = load_data()
    return jsonify(data)

# ==================== Start ====================
if __name__ == "__main__":
    init_db()

    app.run(debug=True, host="0.0.0.0")
