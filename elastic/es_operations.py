from elasticsearch import Elasticsearch, helpers


def create_index(es, mapping, index=None):
    try:
        response = es.indices.create(index=index, body=mapping,
                                     ignore=400)  # ignore 400 to prevent error if the index already exists

        print("Mapping Created Successfully")
        print(response)
    except Exception as e:
        print(f"Mapping can't create due to this error - {str(e)}")


def add_bulk_data_into_es(data, es=None, index=None):
    try:
        helpers.bulk(es, data, index=index)
        print(f"{len(data)} Documents Insertion is Done into elastic search Database")
    except Exception as e:
        print(f"ES insert failed due to {str(e)}")


def delete_from_es(es, query, index):
    res = {"status": "True", "message": "Data Deleted Successfully from Elastic Search"}
    try:
        es.delete_by_query(index=index, body=query)
    except Exception as e:
        res["status"] = False
        res["message"] = f"Data deleted failed from Elastic Search due to - {str(e)}"

    return res


def get_all_data_from_es(es, index, query):
    query = {
        "query": {
            "match_all": {}
        },
        "size": 1000
    }
    data = es.search(index=index, body=query)
    return data