from dotenv import load_dotenv
load_dotenv()
import os

from elastic.es_client import create_es_client

ES_INDEX = os.environ.get("ES_INDEX", "customer")
es = create_es_client()
ES_CLIENT = es.get("es")


def get_all_data():
    query = {
        "query": {
            "match_all": {}
        },
        "size": 1000
    }
    data = ES_CLIENT.search(index=ES_INDEX, body=query)
    es_data = data["hits"]["hits"]
    print(es_data)

get_all_data()