from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from mongo_client import users, es_table
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()
import os
from utils.utilities import generate_random_data,  modify_id_filed
from elastic.es_operations import add_bulk_data_into_es, delete_from_es, get_all_data_from_es
from elastic.es_client import create_es_client
from utils.write_console import Logger



app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

ES_INDEX = os.environ.get("ES_INDEX", "customer")
ES_HOST = os.environ.get("ES_HOST", "http://localhost:9200")
ES_API_KEY = os.environ.get("ES_KEY", "799C4RlvmdEHLKR55A820n2C")
# es = create_es_client() # local purpose
# ES_CLIENT = es.get("es")

ES_CLIENT = Elasticsearch(ES_HOST, api_key=ES_API_KEY) # prod server

log_obj = Logger()
add_logs = log_obj.get_logger()

if ES_CLIENT.ping():
    add_logs.info("Successfully connected to Elasticsearch!")
    print("Successfully connected to Elasticsearch!")
else:
    add_logs.info("Could not connect to Elasticsearch.")
    print("Could not connect to Elasticsearch.")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.find_one({"username": username})

        if user_data and check_password_hash(user_data["password"], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            add_logs.info("Invalid username or password")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.find_one({"username": username})

        if user_data:
            add_logs.info('Username already exists')
            flash('Username already exists')
            return redirect(url_for('register'))

        # Use a supported hashing method (fallback to pbkdf2:sha256)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        data = {"username": username, "password": hashed_password}
        users.insert_one(data)
        add_logs.info('Registration successful! Please log in.')
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/generate_data/<count>')
def generate_data(count):
    data = generate_random_data(num_entries=int(count))
    add_logs.info(f"Total Records : {len(data)}")
    add_logs.info(f" Generated data : {data}")
    try:
        es_table.insert_many(data) # insert to mongodb
        add_logs.info("Data inserted to mongodb")
        data = modify_id_filed(data)
        add_bulk_data_into_es(data, es=ES_CLIENT, index=ES_INDEX) # insert to elastic search
        add_logs.info(f"{len(data)} records inserted to Elastic search")
    except Exception as e:
        add_logs.info(f"Insert failed due to : {e}")
        return jsonify({"Error": str(e)})
    return render_template("data_page.html", data=data)


@app.route('/data/<_id>/delete', methods=["POST", "GET"])
def delete_data_from_es_and_mongo_db(_id):
    from bson import ObjectId
    _query = {
        "query": {
            "match": {
                "_id": _id
            }
        }
    }
    delete_mongo_db = es_table.delete_one({"_id": ObjectId(_id)})
    es_delete = delete_from_es(es=ES_CLIENT, query=_query, index=ES_INDEX)
    add_logs.info("Data deleted successfully")
    flash("Data deleted successfully")
    return redirect(url_for("show_all_es_data"))


@app.route('/edit/<_id>', methods=["POST", "GET"])
def update_document(_id):
    """
    I am just updated the age field manually - need to implement dynamically
    :param _id:
    :return:
    """
    update_body = {"age": 22}
    try:
        response = ES_CLIENT.update(index=ES_INDEX, id=_id, body={"doc": update_body})
        add_logs.info(f"Document {_id} updated in '{ES_INDEX}'.")
        print(f"Document {_id} updated in '{ES_INDEX}'.")
        response_dict = response.raw
        return jsonify({"status": "success", "result": response_dict})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/show/all/es_data', methods=['GET'])
def show_all_es_data():
    filters = {}
    if 'id' in request.args and request.args.get("id") != "":
        filters['_id'] = request.args.get('id')
    if 'name' in request.args and request.args.get("name") != "":
        filters['name'] = request.args.get('name')
    if 'age' in request.args and request.args.get("age") != "":
        filters['age'] = request.args.get('age')
    if 'country' in request.args and request.args.get("country") != "":
        filters['country'] = request.args.get('country')

    # Add the logic to filter the data based on the provided filters
    records, total_records = filter_es_data(filters)

    # Assuming `page` is passed in the request for pagination
    page = int(request.args.get('page', 1))
    total_pages = (total_records // 50) + (1 if total_records % 50 else 0)

    return render_template('show_filter_data.html',
                           records=records,
                           total_records=total_records,
                           current_page=page,
                           total_pages=total_pages)


def filter_es_data(filters):
    query = {"query": {"bool": {"must": []}}, "size": 1000}
    for field, value in filters.items():
        query["query"]["bool"]["must"].append({"match": {field: value}})

    response = ES_CLIENT.search(index=ES_INDEX, body=query)
    total_records = response['hits']['total']['value']
    records = response['hits']['hits']

    return records, total_records


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)