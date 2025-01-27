import json

class CouchHTTPError(Exception):
    def __init__(self, body, code):
        self.body = body
        self.code = code

    def __str__(self):
        return "Error " + str(self.code) + " returned from CouchDB: " + json.dumps(self.body)

class ObjectAlreadyExistsException(Exception):
    def __init__(self, message, obj_id):
        self.message = message
        self.obj_id = obj_id

    def __str__(self):
        return self.message
