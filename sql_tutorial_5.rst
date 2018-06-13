**********************************************************************
A Minimalist Introduction to Relational Databases and SQL using SQLite
**********************************************************************

Part 5
======

Will Hays - May 2018

topics covered:

* datatypes, storage classes and affinities
* loading cvs data using implicit autocommit
* dates using ISO8601
* temporary tables
* CREATE TABLE AS
* CREATE INDEX

Datatypes in SQLite
===================

SQLite appears to support traditional datatypes for databases and will
accept CREATE TABLE statements that use them.  But in reality it uses
dynamic "Storage Classes" using "Type Affinities" to handle traditional
datatype functionality.  According to the SQLite 
`documentation <https://www.sqlite.org/datatype3.html>`_ , 

"Except for INTEGER PRIMARY KEY, any value can be put in any column
and it will be dynamically accomodated."

So for an existing traditional CREATE TABLE statement such as::

CREATE TABLE person (
    id        INTEGER PRIMARY KEY,
    name      VARCHAR(16) NOT NULL,
    birthdate CHAR(10),
    category  INTEGER,
    score     DOUBLE
);

SQLite will accept the given datatypes using Type Affinities as if
the following were given, which it will also accept as valid::

CREATE TABLE person (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    birthdate TEXT,
    category  NUMBER,
    score     REAL
);

But except for the 'id' field, you can even do the following::

CREATE TABLE person (
    id        INTEGER PRIMARY KEY,
    name NOT NULL, birthdate, category,score
);

Unless transferring exiting DDL from a different database system,
it seems useful to use the Type Affinities as a guide to the
developer to indicate how columns intend to be used.

CSV import with AUTOCOMMIT
==========================

To support the following discussion, create a new SQLite database
'contact_db_' and create the above table.  There are many situations
where having the database assign the PRIMARY KEY id value is very
convenient.  This feature is called AUTOCOMMIT.  Unfortunately, 
it doesn't now work with CSV import but there is a workaround 
using a temporary table for the import.  Temporary tables are created as regular
tables with the additional word TEMP or TEMPORARY.  ::

    sqlite>CREATE TABLE temp_person (
            name      TEXT NOT NULL,
            birthdate TEXT,
            category  INTEGER,
            score     REAL
           );
          
    sqlite>.mode csv
    sqlite>.import persons.csv temp_person

Now fill the person table with data from the temp table. 
The SQLite documentation recommends not using the AUTOCOMMIT term
in the query.  Just adding the data without referencing the
PRIMARY KEY id field will trigger the proper autocommit to happen:

    sqlite>INSERT INTO person (name, birthday, category, score) 
           SELECT name, birthdate, category, score FROM temp_person;

Dropping the temporary table is unnecessary as it is
automatically dropped when the current session is ended.

Test for a successful import.  The table should have 2000 rows,
so for a quick test you will want to see just a few rows which
can be achieved with 'LIMIT n' added to the end of a select query,
where n is a positive integer::

    sqlite>SELECT COUNT(*) from person; 
    sqlite>SELECT * FROM person LIMIT 10;


Dates in SQLite
===============

SQLite does not have an 'Affinity' for date and date/time types but it does include
some functions to support a number of ways dates and times can be expressed as
strings or numbers:  ISO8061 strings, UNIX time and JulianDay.  
In the person table, the birthdate is formatted in ISO8061: YYYY-MM-DD.
The strftime function can extract or calculate aspects of a given date, such as
the year, the month, the day of year (1-366), etc.  
See the `documentation <https://www.sqlite.org/datatype3.html>`_ for a
comprehensive listing.  

Most of these functions might be used to display dates in particular formats
but other things are possible.
As an example, to calculate age based on birthdates in the person table::

    sqlite>SELECT strftime('%Y', 'now') - strftime('%Y', birthdate) + 
           ((strftime('%j', birthdate) < strftime('%j', date('now')))) AS age  
           FROM person LIMIT 5;

Subtracting the year of birth from the current year is the basis.
Then determine whether the number of days in the current year
is less than the number of days up to the birthday gives a boolean
value, which in SQLite is evaluated as 1 or 0, so it can be added
to get the correct age to the day. 

More complex calculations probably require things beyond what is possible
in a single line in SQL. One such path would be to create a temporary table 
from query results.   Here is a reworking of the above query with
a temporary table where the table structure and data is the result of a query::

    sqlite>CREATE TEMP TABLE temp_age_calc AS 
           SELECT id, name,
                  strftime('%Y', date('now')) cur_year,
                  strftime('%j', date('now')) now_day_of_year,  
                  strftime('%Y', birthdate) birth_year,
                  strftime('%j', birthdate) birth_day_of_year
                  from person;

    sqlite>SELECT name, cur_year - birth_year + 
           (birth_day_of_year < now_day_of_year) AS age
           FROM temp_age_calc LIMIT 5;

Indexes
=======

Up to now we have used tables with very few rows, so there have not
been performance considerations.  But the purpose of most databases
revolves around have a lot of data that cannot be easily managed
in other ways, which in turn means that tables with many rows need
to perform efficiently. 

A primary mechanism for SELECT statments to run quickly is the use
of indexes which avoids having the database check every row to find
matches.  In SQL, indexes are created as in::

    sqlite>CREATE INDEX person_pk_idx ON person(id);

where 'person_pk_idx' is the name of the index using a common shorthand
to indicate the specifics, in this case on the primary key 'id' field
in the 'person' table.  This index automatically updates when changes
are made to the referenced table.  However, it is possible that an
index can be corrupted and will need to be recreated.  To delete the
above index, it is simply:

    sqlite>DROP INDEX person_pk_idx;

Usually, primary key fields will need indexes.  In particular, any
foreign keys in other tables that reference the primary key depend
heavily on the index to be efficient.  The foreign key fields do not
need indexes since they are not being references.  Other fields that
are commonly searched on should have indexes as well.  For instance,
if the category field the person table is used in searches, then the
following will them speed up::

    sqlite>CREATE INDEX person_pk_idx ON person(category);
 
