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
but the new JSON datatype is in association with features that also provide for additional
syntax to query these fields in a structured way following the hierarchical
structure of JSON.  

And SQLite has also added on JSON capabilities as an optional extension.  
It may not be included in the particular SQLite installation on your system.  
In its early years it required a special compilation to be included and/or
the extension to be specified.  Understandably, you may not want or be able
to recompile SQLite.  However, it is an exciting new feature and the following
examples show the range of capabilities.

Warning: the following assumes familiarity with JSON syntax, though it should be
mostly intuitive.  For a quick description, see the 
`Wikipedia article <https://en.wikipedia.org/wiki/JSON>`_ .

The `SQLite documentation for their JSON1 extension <https://www.sqlite.org/json1.html>`_ 
does not describe the JSON datatype, though uses it in an example. 
In general, that documentation focuses
on the JSON1 features but does not show how they might be integrated into SQL statements.
The following examples strive to demonstrate how it comes together.::

    sqlite> CREATE TABLE user (id INTEGER NOT NULL, user_json JSON);
    sqlite> INSERT INTO user VALUES (1, '{"name": "John", "phone": ["123-456-7777"]}');
    
The JSON1 function "json()" will "minify", i.e. remove extraneous spaces from the JSON
string which will optimize storage::

    sqlite> INSERT INTO user VALUES (2, json('  {"name": "Mary", "phone": ["123-456-8888"]}'));
    
If the JSON string is malformed, such as missing a comma, an error will be generated::

    sqlite> INSERT INTO user VALUES (22, json('  {"name": "Mattie" "phone": ["123-726-8888"]}'));
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
                                               "phone": ["123-456-8888"],
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
    
    sqlite> INSERT INTO user VALUES (4, json('{"name": "Dwayne", 
                                               "address": {"street": "44 Elm",
                                                           "city": "Ames",
                                                           "state": "Iowa"},
                                               "phone": ["123-456-9999", "888-456-1111"] }'));
                                                           
    sqlite> SELECT DISTINCT json_extract(user_json, '$.address.street') FROM user;
    NULL
    23 Elm
    44 Elm
    
Okay.  That works, too. Data validation would likely be an issue for any application
using such a database with a loose structure; the onus is on the developer to provide the tools.

To qualify a SELECT query with a WHERE clause based on values in the JSON needs
another call to json_extract::

    sqlite> SELECT json_extract(user_json, '$.address.street') FROM user
            WHERE json_extract(user_json, '$.address') IS NOT NULL;
    23 Elm
    44 Elm
    
To qualify a SELECT query where there are multiple entries in a JSON element,
the json_each function is used to iterate through, in this case the 
phone number array for each user.  The json_each function call
is placed in the FROM clause as if it were a table and the json_each object
is used to pull values in the SELECT clause.  This query only works if
all of the users phone number JSON elements are iterable.::  
    
    sqlite> SELECT json_extract(user_json, '$.name'), json_each.value 
        FROM user, json_each(json_extract(user_json, '$.phone'))
        WHERE json_each.value LIKE '123%';
    John|123-456-7777
    Mary|123-456-8888
    Agnes|123-456-8888
    Dwayne|123-456-9999

To modify JSON on a per-element basis, the following functions are used:

* json_insert 
* json_replace
* json_set
* json_remove
* json_patch

Each of these takes a JSON object as the first parameter and returns another JSON object.
The consequence is that to make such a change means replacing the entire JSON object in
the database. json_insert and json_replace will not make a change unless the element is
new or exists, respectively.  json_set makes the change without regard to state of the data.
In the case of an incomplete JSON hierarchy as in the first update, SQLite creates it as needed.
::

    sqlite>UPDATE user SET user_json = json_insert(user_json, '$.address.zipcode', '12345') WHERE id = 2; 

    sqlite>UPDATE user SET user_json = json_replace(user_json, '$.address.zipcode', '12347') WHERE id = 2;
    
    sqlite>UPDATE user SET user_json = json_set(user_json, '$.address.zipcode', '12349') WHERE id = 2;
    
    sqlite>UPDATE user SET user_json = json_remove(user_json, '$.address.zipcode') WHERE id = 2;
     
Even arrays can be modified without json_extract.  The following uses json_insert for the second array
element since it does not yet exist::

    sqlite>UPDATE user SET user_json = json_insert(user_json, '$.phone[1]', '123-444-5588') WHERE id = 2; 

To append to the end of an array, the json_array_length function can be used to calculate that position
but there doesn't seem to be a way to interpolate that function call into the UPDATE statement.  Calling
json_set() on the array itself will remove the array -- not the hoped for result.  So it looks like two
separate SQL statements are required to append at an arbitrary index position.








                                                         









