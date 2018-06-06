#python3 script to accompany: tutorial_python_sqlite #3
 
import sqlite3

conn = sqlite3.connect('racetimes_db')  
cursor = conn.cursor()

cursor.execute("BEGIN")
cursor.execute("UPDATE runners SET name = 'Alma' WHERE id = 1")
cursor.execute("UPDATE runners SET name = 'Barnabas' WHERE id = 2")

cursor.execute("SELECT name, location FROM runners WHERE id in (1, 2)")
seq = cursor.fetchall()
[print(runner) for runner in seq]

conn.rollback();
cursor.execute("SELECT name, location FROM runners WHERE id in (1, 2)")
seq = cursor.fetchall()
[print(runner) for runner in seq]
  
conn.close()
