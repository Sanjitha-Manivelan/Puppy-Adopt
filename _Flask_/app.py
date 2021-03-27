import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'puppy adopt')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    store = db.Column(db.String(100))

    def __init__(self, name, store):

        self.name = name
        self.store = store

@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)

@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        store = request.form['store']


        my_data = Data(name, store)
        db.session.add(my_data)
        db.session.commit()

        flash("Added Puppy!")

        return redirect(url_for('Index'))

@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.store = request.form['store']
        db.session.commit()
        flash("Puppy Has Been Updated")

        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Puppy Has Been Deleted")

    return redirect(url_for('Index'))

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
