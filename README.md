# CouchBeans
CouchBeans is a CouchDB library for python, aiming to provide as much resilience as possible for dodgy network environments. It's designed to be quick and easy to use, with as much complexity hidden from the user as possible.

A quick example:
```
>>> from couchbeans import CouchClient
>>> db = CouchClient("http://root:couchbeans@localhost:6984/")
>>> db.get_document("main", "bb0065e5-d047-4bfc-b64a-855adeb89e35")
{"_id":"bb0065e5-d047-4bfc-b64a-855adeb89e35", "_rev": "1-90d3dbcd053542fda4bdd6754ecc917a", "msg": "hello world!"}
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
