#python3 script to accompany: tutorial_python_sqlite #2

import sqlite3

conn = sqlite3.connect('racetimes_db')  # the connection
cursor = conn.cursor()
cursor.execute("SELECT name, location FROM runners")
seq = cursor.fetchall()
print(f'result size = {}', len(seq))
[print(runner) for runner in seq]
conn.close()
