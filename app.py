from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import sys

app = Flask(__name__)

#engine = create_engine('mysql+pymysql://')



@app.route("/")
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
