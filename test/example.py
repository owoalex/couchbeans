#!/bin/python3

from couchbeans import CouchClient
from couchbeans.exceptions import ObjectAlreadyExistsException
import argparse
import json

def get_doc_diff(doc1, doc2):
    if "_rev" in doc1: # These are very likely to be different, but not useful for most unit tests
        del doc1["_rev"]
    if "_rev" in doc2:
        del doc2["_rev"]
    if "_id" in doc1: # Also not that useful for testing
        del doc1["_id"]
    if "_id" in doc2:
        del doc2["_id"]
    set1 = set(doc1.items())
    set2 = set(doc2.items())
    diff = set2 ^ set1
    return diff

def test_base_connection(conn, verbose):
    if verbose:
        print("Testing base connection")
    if len(conn.get_server_version()) > 3:
        return True
    return False

def test_create_db(conn, verbose):
    if verbose:
        print("Testing db creation")
    if conn.create_db("beans_test_db"):
        return True
    return False

def test_delete_db(conn, verbose):
    if verbose:
        print("Testing db deletion")
    if conn.delete_db("beans_test_db"):
        return True
    return False

def test_put_document(conn, verbose):
    if verbose:
        print("Testing creating a document")
    desired_doc = {
            "edible": True,
            "price": 1.20,
            "weight": 500,
            "stock": 256
        }
    conn.put_document("beans_test_db", "baked", desired_doc)
    doc = conn.get_document("beans_test_db", "baked")
    #print(json.dumps(doc, indent=4))
    return len(get_doc_diff(doc, desired_doc)) == 0 # Check for an exact match

def test_patch_document(conn, verbose):
    if verbose:
        print("Testing patching the last document")
    desired_doc = {
            "edible": True,
            "price": 1.20,
            "weight": 500,
            "stock": 255
        } # This should be the state of the doc after the patch
    patch = {
            "stock": 255 # Someone's eaten some beans!
        }
    conn.patch_document("beans_test_db", "baked", patch)
    doc = conn.get_document("beans_test_db", "baked")
    #print(json.dumps(doc, indent=4))
    return len(get_doc_diff(doc, desired_doc)) == 0 # Check for an exact match

def test_delete_document(conn, verbose):
    if verbose:
        print("Testing deleting the last document")
    conn.delete_document("beans_test_db", "baked")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="CouchBeans tester",
                    description="Tests the CouchBeans library, and acts as an example program")

    parser.add_argument("connection_uri")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-j", "--json", action="store_true")

    args = parser.parse_args()


    as_json = args.json
    verbose = args.verbose
    if as_json:
        verbose = False
    couch_base_uri = args.connection_uri # e.g. http://root:couchbeans@localhost:5984/
    conn = CouchClient(couch_base_uri)
    conn.set_verbose(verbose)

    passed_tests = []
    failed_tests = []
    exceptions = []
    tests = [
            test_base_connection,
            test_create_db,
            test_put_document,
            test_patch_document,
            test_delete_document,
            test_delete_db,
        ]

    for test in tests:
        try:
            if test(conn, verbose):
                passed_tests.append(test.__name__)
            else:
                failed_tests.append(test.__name__)
        except Exception as e:
            exceptions.append({
                    "on": test.__name__,
                    "error": str(e)
                })

    if as_json:
        output = {
                "passed": passed_tests,
                "failed": failed_tests,
                "crashed": exceptions
            }
        print(json.dumps(output, indent=4))
    else:
        print(f"{len(passed_tests)} tests passed")
        for passt in passed_tests:
            print("    - " + passt)
        print(f"{len(failed_tests)} tests failed")
        for failt in failed_tests:
            print("    - " + failt)
        print(f"{len(exceptions)} exceptions:")
        for exception in exceptions:
            print("    - " + exception["test"])
            print("      " + exception["exception"])
