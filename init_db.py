import sqlite3

db = sqlite3.connect("database.db")

db.execute("""
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,

    m1 TEXT,
    m2 TEXT,
    m3 TEXT,
    m4 TEXT,
    m5 TEXT,
    m6 TEXT,
    m7 TEXT,

    status TEXT,
    last_stage TEXT
)
""")

db.commit()
db.close()
