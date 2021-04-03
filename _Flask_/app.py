import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'puppyadopt.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class User(db.Model):
    __tablename__ = 'usertable'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)

@app.route('/signup', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_password )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                session['logged_in'] = True
                session['email'] = user.email
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

class Data(db.Model):
    id2 = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

@app.route('/index')
def index():
    all_data = Data.query.all()

    return render_template("index.html", puppies=all_data)

@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        my_data = Data(name)
        db.session.add(my_data)
        db.session.commit()

        flash("Added Puppy!")

        return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id2'))

        my_data.name = request.form['name']
        db.session.commit()
        flash("Puppy Has Been Updated")

        return redirect(url_for('index'))

@app.route('/delete/<id2>/', methods = ['GET', 'POST'])
def delete(id2):
    my_data = Data.query.get(id2)
    db.session.delete(my_data)
    db.session.commit()
    flash("Puppy Has Been Deleted")

    return redirect(url_for('index'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run()
