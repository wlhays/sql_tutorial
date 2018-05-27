*****************************************************
Introduction to Relational Databases and SQL - part 2
*****************************************************

Will Hays - May 2018

In each row in a table, each field will contain a single piece of data
corresponding to a supported data-type, not a composite of elements.
Some datatypes, e.g. dates, inherently represent a composite when they
are rendered (e.g. day + months + year) but internally are a single number
or string.

In designing a relational database, a data elements should not be redundant
across tables. They should be expressed once per row in one table.
The relational model
will provide the tools to access that data from any perspective required
if the table design is done well.  The means by which data is correlated
so that there is no redundancy is done through 'table joins', a syntax
which specifies how tables can be linked to each other and redundancy
eliminated.

Let's start with a geographical example.  As in the previous lesson,
start up the SQLite application from the command-line and save a new
database.::

  >sqlite3
    sqlite>.open --new
    sqlite>.save geodb
    sqlite>.headers on
    sqlite>.mode column

The data model begins with the topmost hierarchical level.::

    sqlite>CREATE TABLE continent (
       id            integer  PRIMARY KEY,
       name          text     NOT NULL,
       hemisphere    text     CHECK( hemisphere IN ('EAST', 'WEST') ) NOT NULL,
       area          integer  NOT NULL DEFAULT 0
    );

The qualifying "CHECK( ... )" is another way of expressing a constraint on
the data element and gets around
the lack of a way to specify an enumeration which is available in other
database applications. In this case, if an attempt is made to insert a row
where the 'hemisphere' field is not either 'EAST' or 'WEST' then it will
fail.::

    sqlite>INSERT INTO continent VALUES (1, 'Africa', 'EAST', 30300000);
    sqlite>INSERT INTO continent VALUES (2, 'Antarctica', 'EAST', 14000000);
    sqlite>INSERT INTO continent VALUES (3, 'Asia', 'EAST', 44579000);
    sqlite>INSERT INTO continent VALUES (4, 'Europe', 'EAST', 10180000);

    sqlite>CREATE TABLE country (
       id            integer  PRIMARY KEY,
       continent_id  integer,
       name          text     NOT NULL,
       area          integer  NOT NULL,
       FOREIGN KEY(continent_id) REFERENCES continent(id)
    );

The last line 'FOREIGN KEY ...' is the means to join tables by
referencing another table using its primary key column.::

    sqlite>INSERT INTO country VALUES (1, 4, 'France', 643801);
    sqlite>INSERT INTO country VALUES (2, 4, 'Italy',  301338);
    sqlite>INSERT INTO country VALUES (3, 4, 'Spain',  505990);
    sqlite>INSERT INTO country VALUES (4, 1, 'Kenya',  581309);
    sqlite>INSERT INTO country VALUES (5, 3, 'Japan',  377972);

Now we can query the related tables.
First, a shorthand version of a join query where the joined fields area
equated in the WHERE clause::

    sqlite>SELECT continent.name, country.name FROM continent, country
           WHERE country.continent_id = continent.id
           AND continent.hemisphere = 'EAST';

The longer, more formal join query has the join appear in the FROM clause.
The default join type is "INNER" so it is not required in queries.::

    sqlite>SELECT continent.name, country.name FROM country INNER JOIN continent
           ON (country.continent_id = continent.id)
           WHERE continent.hemisphere = 'EAST';

    sqlite>SELECT continent.name, country.name FROM country JOIN continent
           ON (country.continent_id = continent.id)
           WHERE continent.name LIKE 'A%' AND country.area > 400000;

Exercise:  Find the average area of all the countries listed for Europe.

Another hierarchical level in our geographical data model::

    sqlite>CREATE TABLE city (
       id            integer  PRIMARY KEY,
       country_id    integer,
       name          text     NOT NULL,
       population    integer  NOT NULL DEFAULT 0,
       FOREIGN KEY(country_id) REFERENCES country(id)
    );

    sqlite>INSERT INTO city VALUES (1, 1, 'Paris',   2206500);
    sqlite>INSERT INTO city VALUES (2, 2, 'Milan',   1363180);
    sqlite>INSERT INTO city VALUES (3, 2, 'Napoli',  3115320);
    sqlite>INSERT INTO city VALUES (4, 4, 'Nairobi', 6548000);
    sqlite>INSERT INTO city VALUES (5, 5, 'Tokyo',   9000000);
    sqlite>INSERT INTO city VALUES (6, 3, 'Madrid',  3166000);
    sqlite>INSERT INTO city VALUES (7, 3, 'Cádiz',    124000);

Retrieving data from the interrelated tables, this query uses two inner joins::

    sqlite>SELECT continent.name, country.name, city.name
           FROM continent, country, city
           WHERE country.continent_id = continent.id
           AND city.country_id = country.id
           AND city.population > 1000000;

The same query using the more formal syntax::

    sqlite>SELECT continent.name, country.name, city.name
           FROM city JOIN country ON (city.country_id = country.id)
           JOIN continent ON (country.continent_id = continent.id)
           WHERE city.population > 1000000;


This design is rigid and does not fit some modes of geographical organization.
It is also verbose.  In upcoming lessons, we'll explore some alternatives.

When you exit SQLite, it will have saved the current state of the data and
we will come back to it. ::

    sqlite>.exit