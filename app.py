from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from mongo_client import users
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated user database
# users_db = {"username": "kumararun31380@gmail.com", "password": "Arun@123"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.find_one({"username": username})
        check_pass = check_password_hash(user_data["password"], password)

        if user_data and check_pass:
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
        data = {"username": username, "password": generate_password_hash(password)}
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


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

