*****************************************************
Introduction to Relational Databases and SQL - part 3
*****************************************************

Will Hays - May 2018

topics covered:

* loading cvs data
* running sql scripts
* aliases
* ordering
* counting
* group by

Setup
=====

As with parts 1 & 2, sqlite is used in this tutorial.
As mentioned in part 1, sqlite can usually be run from
the command line with either "sqlite" or "sqlite3".
To get started, create or find a directory appropriate
for this tutorial and download the accompanying files:

* races.csv
* runners.csv
* racetimes.csv
* reldb_tut_pt3_ddl.sql

Start sqlite and you will see the SQLite prompt.
Create a new database, load the data and save
under the name "racetime" as follows::

 sqlite>.open --new
  sqlite>.read sqlite_tut_pt3_ddl.sql
  sqlite>.mode csv  #this changes the csv separator to ','
  sqlite>.import races.csv races
  sqlite>.import runners.csv runners
  sqlite>.import times.csv times
  sqlite>.save racetime

Improved formatting for the command line output::

 sqlite>.headers on
  sqlite>.mode column

For future use, save these two lines in a file called **.sqliterc**
in your home directory.

Check each of the tables::

  sqlite>SELECT * FROM races;
   sqlite>SELECT * FROM runners;
   sqlite>SELECT * FROM times;

The **times** table contains each runner's racetimes for races they have run.
To correlate runners and races there are two FOREIGN KEY relationships that
use the runners.id and races.id fields.  To extract readable information in a
query, joins can be used, such as::

  sqlite>SELECT runners.name, races.name, races.distance_km, times.time
         FROM runners, races, times
         WHERE times.runner_id = runners.id AND times.race_id = races.id;

    name        name           distance_km  time
    ----------  -------------  -----------  ----------
    Alice       Escondido 10K  10           17.3
    Bob         Escondido 10K  10           16.8
    Dave        Escondido 10K  10           14.2
    Edgar       Escondido 10K  10           14.8
    Fran        Escondido 10K  10           20.1
    Alice       Chula Vista I  5            8.1
    Bob         Chula Vista I  5            7.7

Aliases
=======

In order to give better names to the result columns, use **aliases** in the
SELECT clause.  The "AS" is optional.  When there is no duplication of
column names, it is possible to just use the unqualified field name
even if there are several referenced tables.  However, it is often
helpful to qualify with the table name or alias even if not required::

    sqlite>SELECT runners.name AS runner, races.name AS race,
                  races.distance_km AS km, time
           FROM runners, races, times
           WHERE times.runner_id = runners.id AND times.race_id = races.id;

      runner      race           km          time
      ----------  -------------  ----------  ----------
      Alice       Escondido 10K  10          17.3
      [etc.]

To simplify and shorten the query statement, use aliases in the FROM clause.
All other references to the aliased tables must use the alias names::

    sqlite>SELECT rr.name runner, rc.name race, rc.distance_km  km, t.time
           FROM runners rr, races rc, times t
           WHERE t.runner_id = rr.id AND t.race_id = rc.id;

      runner      race           km          time
      ----------  -------------  ----------  ----------
      Alice       Escondido 10K  10          17.3
      [etc.]

Ordering Results
================

To order the results in a particular way, use the optional ORDER BY clause
to indicate one or more columns to order by, with the optional
qualifiers ASC or DESC for **ascending** (the default) or **descending**::

  sqlite>SELECT runners.name AS runner, races.name AS race,
              races.distance_km AS km, times.time
       FROM runners, races, times
       WHERE times.runner_id = runners.id AND times.race_id = races.id
       ORDER BY runner;

   runner      race           km          time
   ----------  -------------  ----------  ----------
   Alice       Escondido 10K  10          17.3
   Alice       Chula Vista I  5           8.1
   Bob         Escondido 10K  10          16.8
   Bob         Chula Vista I  5           7.7
   Dave        Escondido 10K  10          14.2
   Edgar       Escondido 10K  10          14.8
   Fran        Escondido 10K  10          20.1

Excercise:  Try out different orderings, such as::

    ORDER BY race, time

Counting
========

To count the number of items in a query, use COUNT in the select clause::

  sqlite>SELECT COUNT(*) FROM races;

  3

The asterisk indicates that rows are being counted.  Alternatively,
a column can be specified.  In the case of a primary key, this will
give the same result as the asterisk::

  sqlite>SELECT COUNT(id) FROM races;

  3

In the case of counting values that repeat in a column, use
the DISTINCT qualifier::

  sqlite>SELECT COUNT(DISTINCT location) FROM runners;

To count the number of runners in each race::

  sqlite>SELECT races.name AS race, COUNT(runners.id) AS runners
     FROM runners, races, times
     WHERE times.runner_id = runners.id AND times.race_id = races.id
     GROUP BY race;

  race                      runners
  ------------------------  -----------------
  Chula Vista Invitational  2
  Escondido 10K             5

Note that even though there is no output from the **times** table,
the joins via that table are required to connect the races to the runners.
The GROUP BY clause is added here to indicate the breakdown column by
which to count.  If an alias is used in the SELECT statement, as
we did here with "race", then the GROUP BY clause will need to
use that alias.

To add up all the kilometers run by each runner over all the races::

  sqlite>SELECT runners.name AS runner, SUM(races.distance_km) AS 'total dist'
    FROM runners, races, times
    WHERE times.runner_id = runners.id AND times.race_id = races.id
    GROUP BY runner;

Similarly, averages can be computed with the AVG function.
The average race time for each runner doesn't work across races since
the races have different distances, but we can compute the average speed::

  sqlite>SELECT runners.name AS runner,
          AVG(races.distance_km / times.time) * 60 AS avg_km_per_hr
    FROM runners, races, times
    WHERE times.runner_id = runners.id AND times.race_id = races.id
    GROUP BY runner;

Exercise: Select the MIN and MAX speeds for each runner over all the races.

One use case that can come up frequently is to find duplicate entries.
In our design, it is possible that a runner may have more than one
time for the same race.  Let's introduce an inconsistency in the times table::

  sqlite>INSERT INTO times VALUES (10008, 1, 1, , 57.31,);

To find this error, we can query for duplicates::

  sqlite>SELECT times.id ti, runners.id ru, races.id ra, count(*)
    FROM times, runners, races
    WHERE times.runner_id = runners.id and times.race_id = races.id
    GROUP BY ru, ra HAVING COUNT(*) > 1;

This will identify one pair of duplicate rows in the **times** table.
The constraint to have the count be at least 2 rows with the same
runner id and race id is put in a **HAVING** clause, not in the WHERE clause.
For now, think of the count contraint as being subordinate to the GROUP BY
clause as the reason to place it in a HAVING clause.

As an additional level of complexity, we can count the number of duplicates.
Conceptually we want to treat the results of the above query as a table and
just count the number of rows.  We can do this quite literally and plug in
the query in place of a named table surrounded by parentheses::

  sqlite>SELECT count(*) AS duplicates FROM
    (SELECT times.id, runners.id rn, races.id rc, count(*)
    FROM times, runners, races
    WHERE times.runner_id = runners.id AND times.race_id = races.id
    GROUP BY rn, rc HAVING COUNT(*) > 1);

Views
=====

It was good practice to think in terms of the joined tables, but it
can get unnecessarily repetitious.  To solve this we can create a
**view** which will substitute a reusable single name reference
for the joined tables without copying data::

    sqlite>CREATE VIEW racetimes AS
      SELECT rc.name AS race, rc.distance_km, rn.id AS runner_id,
         rn.name AS runner, rn.gender, t.time, t.place
      FROM  races rc, runners rn, times t
      WHERE t.runner_id = rn.id AND t.race_id = rc.id;

Now most of the earlier queries can be restated more simply::

  sqlite>SELECT runner, SUM(distance_km) AS 'total dist'
    FROM racetimes
    GROUP BY runner;
