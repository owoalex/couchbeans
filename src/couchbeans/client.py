import requests
from enum import Enum
from .exceptions import *

class HTTPMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

class CouchClient:
    __max_retries = 3
    __connection_timeout = 3000
    __verbose = False

    def __init__(self, couch_base_uri):
        if couch_base_uri.endswith("/"):
            couch_base_uri = couch_base_uri[:-1]
        self.__couch_base_uri = couch_base_uri
        self.__current_session = requests.Session()

    def get_server_version(self):
        response = self.__couch_query("/", HTTPMethod.GET)
        if "version" in response:
            return response["version"]
        return None

    def set_verbose(self, verbose=True):
        self.__verbose = verbose

    def set_timeout(self, timeout):
        self.__connection_timeout = timeout

    def set_max_retries(self, max_retries):
        self.__max_retries = max_retries

    def __couch_query(self, endpoint, method, args = None):
        try_n = 0
        while try_n < self.__max_retries:
            try:
                if method == HTTPMethod.POST:
                    response = self.__current_session.post(self.__couch_base_uri + endpoint, json=args, timeout=self.__connection_timeout)
                elif method == HTTPMethod.DELETE:
                    response = self.__current_session.delete(self.__couch_base_uri + endpoint, timeout=self.__connection_timeout)
                elif method == HTTPMethod.PUT:
                    response = self.__current_session.put(self.__couch_base_uri + endpoint, json=args, timeout=self.__connection_timeout)
                else:
                    response = self.__current_session.get(self.__couch_base_uri + endpoint, timeout=self.__connection_timeout)
                if response.status_code >= 200 and response.status_code < 300:
                    return response.json()
                else:
                    raise CouchHTTPError(response.json(), response.status_code)
            except requests.exceptions.ConnectionError:
                if self.__verbose:
                    print("Request (" + endpoint + ") was refused on try " + str(try_n))
                try_n += 1
            except requests.exceptions.Timeout:
                if self.__verbose:
                    print("Request (" + endpoint + ") timed out on try " + str(try_n))
                try_n += 1
        raise ConnectionError("Gave up connecting to CouchDB after " + str(try_n) + " tries")

    def find(self, database, selector = {}, fields = None, sort = None, page = 0, page_size = 20):
        if not sort is None:
            for sortby in sort:
                for key in sortby:
                    if not key in selector:
                        selector[key] = {"$exists": True}

        mango = {
                "selector": selector,
                "skip": page * page_size,
                "limit": page_size
            }

        if not sort is None:
            mango["sort"] = sort

        if not fields is None:
            mango["fields"] = fields

        return self.__couch_query("/" + database + "/_find", HTTPMethod.POST, mango)["docs"]

    def find_all(self, database, selector = {}, fields = None, sort = None):
        limit = self.__couch_query("/" + database + "/_all_docs", HTTPMethod.GET)["total_rows"]


        if not sort is None:
            for sortby in sort:
                for key in sortby:
                    if not key in selector:
                        selector[key] = {"$exists": True}

        mango = {
                "selector": selector,
                "limit": limit
            }

        if not sort is None:
            mango["sort"] = sort

        if not fields is None:
            mango["fields"] = fields

        return self.__couch_query("/" + database + "/_find", HTTPMethod.POST, mango)["docs"]

    def create_db(self, database, shards=None, replicas=None, partitioned=False):
        options = {
                "partitioned": bool(partitioned)
            }
        if not shards is None:
            options["q"] = int(shards)
        if not replicas is None:
            options["n"] = int(replicas)
        try:
            self.__couch_query("/" + database, HTTPMethod.PUT, options)
            return True
        except CouchHTTPError as e:
            if e.code == 412:
                raise ObjectAlreadyExistsException("Database already exists", database)
            raise e

    def delete_db(self, database):
        return self.__couch_query("/" + database, HTTPMethod.DELETE)

    def get_document(self, database, doc_id):
        return self.__couch_query("/" + database + "/" + str(doc_id), HTTPMethod.GET)

    # This is a utility function - it will just delete whatever is at the ID!
    def delete_document(self, database, doc_id, strict=False):
        rev_str = ""
        try:
            document = self.__couch_query("/" + database + "/" + str(doc_id), HTTPMethod.GET)
            rev_str = "?rev=" + document["_rev"]
            return self.__couch_query("/" + database + "/" + str(doc_id) + rev_str, HTTPMethod.DELETE)
        except CouchHTTPError as e:
            if strict or (not e.code == 404):
                raise e # Filter out 404, usually we don't care if the document doesn't exist
            else:
                return False # Indicate we didn't actually have to delete anything!

    def put_document(self, database, doc_id, document, overwrite=True, strict=False):
        if overwrite and not strict:
            try:
                in_document = self.__couch_query("/" + database + "/" + str(doc_id), HTTPMethod.GET)
                document["_rev"] = in_document["_rev"]
            except CouchHTTPError as e:
                if not e.code == 404:
                    raise e # Filter out 404, we don't want false alarms!
        return self.__couch_query("/" + database + "/" + str(doc_id), HTTPMethod.PUT, document)

    # Another utility function, will modify the document regardless of _rev
    def patch_document(self, database, doc_id, document_diff, strict=False):
        document = {}
        try:
            document = self.__couch_query("/" + database + "/" + str(doc_id), HTTPMethod.GET)
        except CouchHTTPError as e:
            if strict or (not e.code == 404):
                raise e # Filter out 404, we just default to merging with an empty document
        merged_document = {**document, **document_diff}
        return self.__couch_query("/" + database + "/" + str(doc_id), HTTPMethod.PUT, merged_document)
