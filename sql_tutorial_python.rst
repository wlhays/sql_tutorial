**********************************************************************
A Minimalist Introduction to Relational Databases and SQL using SQLite
**********************************************************************

SQLite and Python (SQLite3 and Python3)
=======================================

Will Hays - May-June 2018

SQL statements are typically used in applications that provide efficiencies
not easily seen in the above tutorials which focus on the SQL syntax.  Such
applications will be typically designed for a particular database and
use an library or api in a specific language targetted to a specific
database platform.  This is easily seen with the big players like Oracle but
are also available for SQLite which is designed for a more localized use case.  
In the Python 3 Standard Library there is a module for SQLite 3
called, easily enough, "sqlite3".  The following brief guide will break down
the use cases and even if you intend to use a different language to access
SQLite, it will show the basic points that need to be covered.

The most fundamental aspect of such a library/api is to mediate between the
application's data that the programming code has access to and the storage
capabilities in the database.  For a relational database, this includes
passing SQL statements to the database and optionally retrieving the results.
No data results in the case of CREATE, INSERT and UPDATE statements, but
there is the potential for errors or other descriptive system responses.  
SELECT statements will often return result sets wrapped in ways compatible with
the language used and according to the design of the library/api.

Let's start with the most basic and minimal interaction using Python.
First, a connection to the database is established using our previous roadrace
example db.  This is commonly called "opening a connection"  and we will
"close it" when done.  Database connections can be an important commodity, 
so it's important to tidy up as soon as it is no longer needed.
Save the following as a file ("tut_1.py")in the project directory, or you
can enter these commands by hand in the Python interpreter.::

     import sqlite3

     conn = sqlite3.connect('racetimes_db')  # the connection
     cursor = conn.cursor()
     cursor.execute("SELECT COUNT(*) FROM runners")
     seq = cursor.fetchone()
     print(seq)
     conn.close()

Here there are layers of Python objects from the sqlite3 API
that wrap what should by now be familiar SQL.  Once the connection
object is created, then a "cursor" is created which is used
to pass SQL statements to the database opened in SQLite. 
The "fetchone()" method will only return each row once after the "execute()"
method is called.  Typically you would store retrieved data in Python
variables to be used as needed or passed on to another system.
'fetchone()' returns a sequence, which in Python is usually a list or tuple
that implements a set of common operations such as indexing, length, etc.
In practice, 'fetchone()' seems to return a tuple.  In this case, a tuple of
length 1, the value is the number of runners in that table.

To retrieve multiple rows, use cursor.fetchmany(size=n) or cursor.fetchall().
With fetchmany, the size parameter is the size of the resulting array that
receives the result. ::

     import sqlite3

     conn = sqlite3.connect('racetimes_db')  # the connection
     cursor = conn.cursor()
     cursor.execute("SELECT name, location FROM runners")
     seq = cursor.fetchall()
     print(f'result size = {}', len(seq))
     [print(runner) for runner in seq]
     conn.close()

To gain more advanced control of changes to the database, commands are
managed by "transactions" that allow  a series of commands to the database 
to be treated as a unit.  At the end of the series
another command is issued to either "commit" or "rollback" the changes 
as needed.  And indeed, there are many situations where changes need to
be made in tandem.  By default, transactions in the sqlite3 library are 
"autocommit", but to explicitly
start a transaction without autocommit use "BEGIN" ::

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

If "rollback()" in the above script is changed to "commit()", 
then the changes will be saved.

In the case of multiple and possibly simultaneous accesses to a database,
things start to get more complicated and each of these accesses need to be
managed even more closely with transactions.
Any other user with a simultaneous connection to the database will not
see the first user's changes until they are committed and vice versa.
The mechanisms for preventing mishaps are out of scope here.

The documentation for the sqlite3 Python3 library is
available online at https://docs.python.org/3/library/sqlite3.html
(This is not easy to understand in many places.)
It is compliant with the more general Python reldb api: DB-API 2.0.
