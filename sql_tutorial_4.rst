*****************************************************
Introduction to Relational Databases and SQL - part 4
*****************************************************

Will Hays - May 2018

This lesson will go back to the data in the second lesson but approach it
with a different table structure.  Startup the saved 'geodb' database in
SQLite.  We will use the tables there as a source for the data in the new
tables defined below.::

    >sqlite3 geodb

Rather than each geographical level
having its own table, there will be a single table 'geo-entity' for all levels.
For that to work, one of the columns will indicate the level of the geographical
entity described by a row.  A separate table will hold the relatively
small number of geographical levels or 'geo_types'.  This type of table
is typically called a lookup table, though there is nothing otherwise
special about it.::

    sqlite>CREATE TABLE geo_type (
       id            integer  PRIMARY KEY,
       name          text     NOT NULL,
       note          text     NOT NULL DEFAULT  ''
    );

    sqlite>INSERT INTO geo_type VALUES (1, 'hemisphere', '');
    sqlite>INSERT INTO geo_type VALUES (2, 'continent', '');
    sqlite>INSERT INTO geo_type VALUES (3, 'country', '');
    sqlite>INSERT INTO geo_type VALUES (4, 'state', '');
    sqlite>INSERT INTO geo_type VALUES (5, 'province', '');
    sqlite>INSERT INTO geo_type VALUES (6, 'city', '');
    sqlite>INSERT INTO geo_type VALUES (7, 'prefecture', '');

(Note that in Sqlite, you need to supply the default value
in the insert statement.)

The geo_entity table has two joins.  The first is to the above geo_type
table.  The second is a 'self join' to the same table where the container_id
is a reference to another row in the same table.  This enables the
containment relationships in our geographic representation.::

    sqlite>CREATE TABLE geo_entity(
       id            integer  PRIMARY KEY,
       geo_type_id   integer  NOT NULL,
       container_id  integer,
       name          text     NOT NULL,
       note          text     NOT NULL DEFAULT  '',
       FOREIGN KEY(geo_type_id) REFERENCES geo_type(id),
       FOREIGN KEY(container_id) REFERENCES geo_entity(id)
    );

Note that the container_id must be NULL or else have a special value for the
highest level containers.

Insert the two hemispheres with NULL container_ids.
Entering two rows in one statement.::

    sqlite>INSERT INTO geo_entity VALUES (1, 1, NULL, 'Eastern', ''),
                                         (NULL, 1, NULL, 'Western', '');

To reuse the data from the earlier tables, we can use a 'subquery' to pull
the data as part of an INSERT statement instead of writing out the data.
The other common use of a subquery is in a FROM clause instead of a table
name.

It is unusual to do arithmetic with id values, but it is convenient here.
Each set of ids in the geo_entity table will be in a specific numeric range,
since we can't reuse the ids as is when they are all moved into the same
table.::

    sqlite>INSERT INTO geo_entity (id, geo_type_id, container_id, name)
           SELECT (1000 + id), 2, 1, name FROM continent;

    sqlite>INSERT INTO geo_entity (id, geo_type_id, container_id, name)
           SELECT (2000 + id), 3, (1000 + continent_id), name FROM country;

    sqlite>INSERT INTO geo_entity (id, geo_type_id, container_id, name)
           SELECT (3000 + id), 6, (2000 + country_id), name FROM city;

Replicate the join queries from the first version.
Using table name aliases is important when joining a table to itself.::

    sqlite>SELECT g1.name as 'country', g2.name as 'city'
           FROM geo_entity g1 JOIN geo_entity g2 ON (g2.container_id  = g1.id)
           WHERE g2.geo_type_id IN (6, 7);

The same query but adding a bit of formatting to the output.
The || is for concatenation.::

    sqlite>SELECT g2.name || ' (' || g1.name || ')' as 'city'
           FROM geo_entity g1 JOIN geo_entity g2 ON (g2.container_id  = g1.id)
           WHERE g2.geo_type_id IN (6, 7);

Exercise:
* Expand the last query with an additional join to include the continent
in the output.

Exercise:
* Redo the geo_entity table by adding columns for area and population.
  Then adjust the insert queries to pull that data from the original tables.

As a practical matter for relational databases, indexes need
to be created for the fields that are used as references, particularly
PRIMARY KEY ids::

    sqlite>CREATE INDEX idx_geo_type_pk ON geo_type(id);
    sqlite>CREATE INDEX idx_geo_entity_pk ON geo_entity(id);

In the event there is a need to remove a table, view or other elements
in the database, a DROP statement is used.
For the geodb, once the data has been migrated to the new
geo_entity table we can safely remove the earlier tables.  Do this in
a way that does not leave dangling references, i.e. in the reverse order
from that of creation::

    sqlite>DROP TABLE city;
    sqlite>DROP TABLE country;
    sqlite>DROP TABLE continent;
    
