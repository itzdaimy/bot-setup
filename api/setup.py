#this is an example api u can use the functions in other scripts by using this line below.
# from api.setup import setupdatabase

import os
import sqlite3

def setup_database(self):
    conn = sqlite3.connect(self.moderation_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            moderator_id TEXT,
            reason TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
