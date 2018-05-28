*****************************************************
Introduction to Relational Databases and SQL - part 1
*****************************************************

Will Hays - May 2018


Find the application SQLite on your machine or install it.

In a commandline window, create a new directory for this exercise
and change to it::

    >mkdir sql_tut
     >cd sql_tut

Any files you create in SQLite will now be saved to the current directory.

Typically the command to start SQLite is "sqlite3" which will give you the
SQLite prompt::

    sqlite>_

Here you can enter commands for the SQLite application, which usually start
with a dot to distinguish them from SQL commands.
Start off with the command ".help" which will give a list of commands.

In SQLite, groups of tabular data are organized into databases that usually
do not interrelate.
You will need to create a new database to do this exercise::

    sqlite>.open --new

Save this to a file, so you don't lose any work::

    sqlite>.save db_1

Just for practice, exit and open SQLite with the specified db::

    sqlite>.exit

Notice the new file "db_1" in the current directory::

    >ls -la

Now go back and open SQLite with the name of the db as the parameter::

    >sqlite3 db_1

The following two commands to SQLite will improve the output display::

    sqlite>.headers on
    sqlite>.mode column

Relational tables are two-dimensional grids of columns and rows.
Every item in a column must have the same datatype.
Every row will have elements or the empty element NULL for each of the columns.
This is structured data.

This new database doesn't have any tables, so let's create one with an
SQL statement::

    sqlite>CREATE TABLE toys (
       id         integer  PRIMARY KEY,
       name       text     NOT NULL,
       type       text     NOT NULL,
       brand      text,
       quantity   integer  NOT NULL,
       comments   text
    );

Note every SQL statement must end with a semicolon!!  SQLite will wait for
one if you forget.  The name of our new table is 'toys'.
The column names of the table are 'id', 'name', 'type', etc.
Each column has a specific datatype.  Not all databases use the same names
for datatypes.
SQLite uses fewer more generic datatypes for than most database programs.
A table may have a column designated as 'primary key', it is usually listed first.
'NOT NULL' indicates that the field is required for every row in the table.

Count the number of rows in the new table::

    sqlite>SELECT COUNT(*) FROM toys;

You get the expected answer, i.e. nothing. Now add some rows to the empty table::

    sqlite>INSERT INTO toys VALUES (1, 'Sheriff Woody', 'action figure', 'Disney', 1, '');
     sqlite>INSERT INTO toys VALUES (2, 'Buzz Lightyear', 'action figure', 'Disney', 1, 'missing hand');
     sqlite>INSERT INTO toys VALUES (3, 'Mr. Spell', 'device', 'Texas Instruments', 1, 'no longer works');

Now look at all the rows in the table::

    sqlite>SELECT * FROM toys;

Pull just the rows with type 'action figure'::

    sqlite>SELECT * FROM toys WHERE type = 'action figure';

Use 'IN' in the WHERE clause when values can match multiples::

    sqlite>SELECT * FROM toys WHERE type IN ('action figure', 'device');

Change the comment field for Buzz.  The *id* is usually the only unique
identifier for each row.::

    sqlite>UPDATE toys SET comments = 'broken nose' WHERE id = 1;

Remove the row for Buzz::

    sqlite>DELETE from toys WHERE id = 2;

Check results::

    sqlite>SELECT * FROM toys;

Remove the table from the database and exit SQLite::

    sqlite>DROP table toys;
     sqlite>.exit

The basics of a relational database have been covered with example statements:

1.  CREATE TABLE
2.  INSERT rows
3.  UPDATE rows
4.  DELETE rows
5.  Qualify affected rows with a WHERE clause
