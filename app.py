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


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

ES_INDEX = os.environ.get("ES_INDEX", "customer")
ES_HOST = os.environ.get("ES_HOST", "http://localhost:9200")
ES_API_KEY = os.environ.get("ES_KEY", "799C4RlvmdEHLKR55A820n2C")
# es = create_es_client()
# ES_CLIENT = es.get("es")

ES_CLIENT = Elasticsearch(ES_HOST, api_key=ES_API_KEY)


if ES_CLIENT.ping():
    print("Successfully connected to Elasticsearch!")
else:
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
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.find_one({"username": username})

        if user_data:
            flash('Username already exists')
            return redirect(url_for('register'))

        # Use a supported hashing method (fallback to pbkdf2:sha256)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        data = {"username": username, "password": hashed_password}
        users.insert_one(data)
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
    try:
        es_table.insert_many(data) # insert to mongodb
        data = modify_id_filed(data)
        add_bulk_data_into_es(data, es=ES_CLIENT, index=ES_INDEX) # insert to elastic search
    except Exception as e:
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
    flash("Data deleted successfully")
    return redirect(url_for("show_all_es_data"))


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