import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "sessions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  target TEXT,
                  created_at TEXT,
                  updated_at TEXT,
                  notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS findings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id INTEGER,
                  tool TEXT,
                  data TEXT,
                  timestamp TEXT,
                  FOREIGN KEY(session_id) REFERENCES sessions(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id INTEGER,
                  role TEXT,
                  content TEXT,
                  timestamp TEXT,
                  FOREIGN KEY(session_id) REFERENCES sessions(id))''')
    conn.commit()
    conn.close()

def create_session(name, target=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT INTO sessions (name, target, created_at, updated_at, notes) VALUES (?, ?, ?, ?, ?)",
              (name, target, now, now, ""))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, target, created_at, updated_at FROM sessions ORDER BY updated_at DESC")
    sessions = c.fetchall()
    conn.close()
    return sessions

def get_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sessions WHERE id=?", (session_id,))
    session = c.fetchone()
    conn.close()
    return session

def delete_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM findings WHERE session_id=?", (session_id,))
    c.execute("DELETE FROM chat_history WHERE session_id=?", (session_id,))
    c.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    conn.commit()
    conn.close()

def add_finding(session_id, tool, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT INTO findings (session_id, tool, data, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, tool, json.dumps(data), now))
    c.execute("UPDATE sessions SET updated_at=? WHERE id=?", (now, session_id))
    conn.commit()
    conn.close()

def get_findings(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT tool, data, timestamp FROM findings WHERE session_id=? ORDER BY timestamp", (session_id,))
    findings = c.fetchall()
    conn.close()
    return findings

def add_chat_message(session_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT INTO chat_history (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, role, content, now))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history WHERE session_id=? ORDER BY timestamp", (session_id,))
    history = c.fetchall()
    conn.close()
    return history

def update_session_notes(session_id, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("UPDATE sessions SET notes=?, updated_at=? WHERE id=?", (notes, now, session_id))
    conn.commit()
    conn.close()
