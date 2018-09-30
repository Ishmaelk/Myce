from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/jon/Myce/test.db'

db = SQLAlchemy(app)

class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	use = db.Column(db.String(200))
	text = db.Column(db.String(200))
	complete = db.Column(db.String(200))

db.create_all()

@app.route("/")
def main():
	lines = db.session.query(Test).all()
	return render_template('index.html', row=lines)

if __name__ == '__main__':
    app.run(debug=True)
