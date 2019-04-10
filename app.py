from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route('/')
def home():
    return "<h1>hello from flask</h1>"

if __name__ == '__main__':
    app.debug = True
    app.run()