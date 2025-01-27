# CouchBeans
*Have you ever held up a broken couch with a tin of beans?* CouchBeans is a [CouchDB](https://couchdb.apache.org/) library for python, aiming to provide as much resilience as possible for dodgy network environments. It's designed to be quick and easy to use, with as much complexity hidden from the user as possible.

A quick example:
```
>>> from couchbeans import CouchClient
>>> db = CouchClient("http://root:couchbeans@localhost:5984/")
>>> db.create_db("main")
True
>>> db.put_document("main", "bean", {"type": "baked"})
{'ok': True, 'id': 'bean', 'rev': '1-975cf46dd62455d25b4743874062ebfe'}
>>> db.get_document("main", "bean")
{'_id': 'bean', '_rev': '1-975cf46dd62455d25b4743874062ebfe', 'type': 'baked'}
```

Have a look at the [test script](./test/example.py) for more examples of how to use CouchBeans.

## Installation
CouchBeans is installable via PIP:
```pip install couchbeans```

## Features
The main advantage of CouchBeans over other CouchDB libraries is its default handling of failed requests. CouchBeans will try a user-configurable number of times to execute a request to help with spotty network connections.

CouchBeans provides utility functions for modifying documents, including a patch operation. It also hides handling of the _rev parameter, making it easy to forget about the underlying network connections.

## Dependencies

- requests
