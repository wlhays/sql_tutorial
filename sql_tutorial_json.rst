*****************************************************
Introduction to Relational Databases and SQL
*****************************************************

SQLite with JSON data (SQLite3 and Python3)
===========================================

Will Hays - June 2018

JSON (originally: JavaScript Object Notation) is now widely used to structure data 
in a character-based format for many
use cases beyond its original purpose, often to avoid the complexities of XML.
Following the popularity of document databases such as MongoDB and CouchDB, 
some relational database systems (RDBMs) such as Postgres and MariaDB have 
introduced a new datatype for JSON documents as single data fields in a record.
This could already happen by using a text or clob (character large object) datatype,
but the new JSON datatype is in association with features that also for additional
syntax to query these fields in a structured way following the hierarchical
structure of JSON.  

And SQLite has also added on JSON capabilities as an optional extension.  
It may not be included in the particular SQLite installation on your system.  
In its early years required
a special compilation to be included.  Understandably, you may not want or be able
to recompile SQLite.  However, it is an exciting new feature.


The SQLite documentation for JSON (https://www.sqlite.org/json1.html) does not describe 
the JSON datatype, though uses it in an example. But the following seems to work::

    sqlite> CREATE TABLE user (id INTEGER, user_json JSON);
    sqlite> INSERT INTO user VALUES (1, '{"name": "John", "phone": "123-456-7777"}');
    
The JSON1 function "json()" will "minify", i.e. remove extraneous spaces::

    sqlite> INSERT INTO user VALUES (2, json('  {"name": "Mary", "phone": "123-456-8888"}'));
    
If the JSON string is malformed, such as missing a comma, an error will be generated::

    sqlite> INSERT INTO user VALUES (22, json('  {"name": "Mary2" "phone": "123-456-8888"}'));
    Error: malformed JSON
        
Further proof of JSON features lies in the special JSON1 functions for extracting and updating rows.
The json_extract selects the indicated parts from the JSON where the "$" character
represents the root of the document::

    sqlite> SELECT json_extract(user_json, '$.name') FROM user;
    John
    Mary
    
There is no requirement that each JSON field in our tables records need conform to any schema.
Of course this is the challenge working with document databases.  Here is a compatible row
but it has additional hierarchical elements::

    sqlite> INSERT INTO user VALUES (3, json('{"name": "Agnes", 
                                               "phone": "123-456-8888",
                                               "address": {"street": "23 Elm",
                                                           "city": "Ames",
                                                           "state": "Iowa"} }'));
                                                           
    sqlite> SELECT json_extract(user_json, '$.name', '$.address.city') FROM user;                                                       
    ["John",null]
    ["Mary",null]
    ["Agnes","Ames"]

    
So even though the first two records don't have the address element, "extracting" the
city returns NULL for them.    
Let's try a different ordering of elements::    
    
    sqlite> INSERT INTO user VALUES (3, json('{"name": "Dwayne", 
                                               "address": {"street": "44 Elm",
                                                           "city": "Ames",
                                                           "state": "Iowa"},
                                               "phone": "123-456-9999" }'));
                                                           
    sqlite> SELECT json_extract(user_json, '$.address.street') FROM user;                                                       
    NULL
    NULL
    23 Elm
    44 Elm
    
Okay.  That works, too. Record validation would be an issue, and the onus is on the
developer to provide the tools.

Functions for altering the JSON data: 
json.insert 
json.replace
json.set
json.remove

                                                          
