# Quick API Reference

In each function definition, the type of each argument is given. Optional arguments have their type prefixed with "?". Default values are shown after the "=" if notable.

`CouchClient.find(database:string, selector:?dict, fields:?dict, sort:?dict, page:?int=0, page_size:?int=20)`
Executes a mango query against the database.

`CouchClient.find_all(database:string, selector:?dict, fields:?dict, sort:?dict)`
Similar to `CouchClient.find` but will query the db for the max number of entries possible.

`CouchClient.create_db(database:string, shards:?int, replicas:?int, partitioned:?bool=False)`
Creates a new logical database on the remote server.

`CouchClient.delete_db(database:string)`
Deletes a database, including all child documents.

`CouchClient.get_document(database:string, doc_id:string)`
Gets a named document from the database.

`CouchClient.delete_document(database:string, doc_id:string)`
Deletes a document from the database.

`CouchClient.put_document(database:string, doc_id:string, document:dict)`
Adds or replaces a document in the database.

`CouchClient.patch_document(database:string, doc_id:string, document_diff:dict)`
Will add to the existing document. Anything specified in document_diff will override the existing value in the document.

`CouchClient.set_verbose(verbose:?bool=True)`
Default value on client creation is False. Verbose will print to console when connection errors occur.

`CouchClient.set_timeout(timeout:int)`
Connection timeout in milliseconds. Default value on client creation is 3000msec.

`CouchClient.set_max_retries(max_retries:int)`
Default value on client creation is 3 tries.
