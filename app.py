from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
import config

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.POSTGRES_URI

heroku = Heroku(app)
db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    genre = db.Column(db.String(25))

    def __init__(self, title, genre):
        self.title = title
        self.genre = genre

@app.route('/')
def home():
    return "<h1>hello from flask</h1>"

@app.route('/movie/input', methods=['POST'])
def movie_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        genre = post_data.get('genre')
        record = Movie(title, genre)
        db.session.add(record)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("Something went horribly wrong")

@app.route('/movies', methods=['GET'])
def return_movies():
    all_movies = db.session.query(Movie.id, Movie.title, Movie.genre).all()
    return jsonify(all_movies)

@app.route('/movie/update/<id>', methods=['PUT'])
def movie_update(id):
    if request.content_type == "application/json":
        put_data = request.get_json()
        title = put_data.get('title')
        genre = put_data.get('genre')
        record = db.session.query(Movie).get(id)
        record.title = title
        record.genre = genre
        db.session.commit()
        return jsonify("Completed Update")
    return jsonify("Update Failed")

@app.route('/movie/delete/<id>', methods=['DELETE'])
def movie_delete(id):
    if request.content_type == "application/json":
        record = db.session.query(Movie).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("Deleted Record")
    return jsonify("Delete Failed")


if __name__ == '__main__':
    app.debug = True
    app.run()