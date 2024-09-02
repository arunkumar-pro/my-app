from elasticsearch import Elasticsearch, ConnectionError, AuthenticationException
import os
from base64 import b64encode
from elastic.es_operations import create_index


def basic_auth(username, password):
    if username and password:
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'{token}'


ELASTIC_HOST = os.environ.get("ELASTIC_HOST", "http://localhost:9200/")
ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", "alpha-logs")
ES_TIMEOUT = int(os.environ.get("ES_TIMEOUT", "10"))
ES_USERNAME = os.environ.get("ES_USERNAME", "elastic")
ES_PASSWORD = os.environ.get("ES_PASSWORD", "799C4RlvmdEHLKR55A820n2C")
ES_INDEX = os.environ.get("ES_INDEX", "customer")


mapping = {
    "mappings": {
        "properties": {
            "_id": {"type": "keyword"},
            "name": {"type": "text"},
            "age": {"type": "integer"},
            "phone": {"type": "keyword"},  # Phone numbers are better as keyword since they won't be analyzed
            "country": {"type": "text"}
        }
    }
}


def create_es_client():
    res = {"status": 200, "message": "", "error": None, 'es': None}
    try:
        # Connect to Elasticsearch with basic auth
        es = Elasticsearch(
            hosts=["http://localhost:9200"],
            basic_auth=(ES_USERNAME, ES_PASSWORD)
        )

        # Ping to check if the connection is successful
        if es.ping():
            # create_index(es, mapping, index=ES_INDEX)
            print("Connected successfully")
            print("Connected to Elasticsearch with Basic Authentication")
            res["message"] = "Connected to Elasticsearch and Mapping  with Basic Authentication"
            res["es"] = es
        else:
            print("Could not connect to Elasticsearch")

    except AuthenticationException as auth_error:
        res["error"] = str(auth_error)
        print(f"Authentication failed: {auth_error}")

    except ConnectionError as conn_error:
        res["error"] = str(conn_error)
        print(f"Connection error: {conn_error}")

    except Exception as ex:
        res["error"] = str(ex)
        print(f"An error occurred: {ex}")

    return res

