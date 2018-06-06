#python3 script to accompany: tutorial_python_sqlite #1

import sqlite3

conn = sqlite3.connect('racetimes_db')  # the connection
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM runners")
seq = cursor.fetchone()
print(seq)
conn.close()
