from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "visitors.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    ip = request.remote_addr  # get visitor IP
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (ip) VALUES (?)", (ip,))
    conn.commit()
    
    # count total visitors
    cur.execute("SELECT COUNT(*) FROM visits")
    total_visitors = cur.fetchone()[0]
    conn.close()

    return render_template("index.html", visitors=total_visitors)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
