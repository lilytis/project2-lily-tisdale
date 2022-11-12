import os
import flask
from flask_sqlalchemy import SQLAlchemy
# import models
# from models import Person
# from models import Review
from urllib import response
import requests
import json
from dotenv import load_dotenv, find_dotenv
from random import randrange

load_dotenv(find_dotenv())

app=flask.Flask(__name__)
app.debug=True
app.secret_key='abcdlmt103'
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Person with username: {self.username}"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieID = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(500))

    def __repr__(movie):
        return f"Movie info: {movie.movieID}, {movie.rating}, {movie.review}"
    
with app.app_context():
    db.create_all()

def get_movies():    
    MOVIE_IDS=[642885, 616820, 760161]
    MOVIE_PATH=f'/movie/{MOVIE_IDS[randrange(3)]}'
    MOVIE_API_BASE_URL=f'https://api.themoviedb.org/3{MOVIE_PATH}'
    IMAGE_URL='https://image.tmdb.org/t/p/w500'

    response=requests.get(
        MOVIE_API_BASE_URL,
        params={
            'api_key': os.getenv('TMDB_API_KEY')
        }
    )
    this_movie=response.json()
    image_path=IMAGE_URL + this_movie['poster_path']
    genres_of_movie=""
    for genre in this_movie['genres']:
        genres_of_movie += str(genre['name'])+", "
    wiki_url=get_wiki_url(title = this_movie['original_title'])
    movie_info=[this_movie['original_title'], this_movie['tagline'],
                    genres_of_movie, image_path, wiki_url]

    return movie_info

def get_wiki_url(title):
    request=requests.Session()
    WIKI_URL="https://en.wikipedia.org/w/api.php"
    params={
        "action":"opensearch",
        "namespace":"0",
        "search": str(title), #+ "movie"
        "limit":"1",
        "format":"json"
    }
    wiki_info=request.get(url=WIKI_URL, params=params)
    get_info=wiki_info.json()
    return get_info[3][0]

@app.route('/')
def index():
    return flask.render_template('home.html')
# def index():
#     return [str(person) for person in Person.query.all()]

@app.route('/register')
def register():
    return flask.render_template('register.html')

# def create(username):
#             person=Person(username=username)
#             db.session.add(person)
#             db.session.commit()
#             return f'Created person with username: {username}'

@app.route('/register', methods=['POST'])
def register_post():
    form_data=flask.request.form
    Person.username = form_data['username']
    if flask.request.method=='POST' and 'username' in flask.request.form:
        return flask.flash('User already exists. Please log in.')
    else:
        person=Person(username=Person.username)
        db.session.add(person)
        db.session.commit()
        return f'Created person with username: {Person.username}'

@app.route('/login')
def login():
    return flask.render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    form_data=flask.request.form
    print(f'FORM DATA: {form_data}')
    Person.username=form_data['username']
    if flask.request.method=='POST' and 'username' in flask.request.form:
        Person.username=flask.request.form['username']
        flask.flash('Logged in successfully!')
        return flask.redirect(flask.url_for('movies'))
    else:
        return flask.flash('Try again. Username invalid.')
        #return flask.redirect(flask.url_for('login'))

@app.route('/movies')
def movies():
    list_of_movie_info = get_movies()
    return flask.render_template('movies.html', title=list_of_movie_info[0], 
        tagline=list_of_movie_info[1], genres=list_of_movie_info[2], 
        image=list_of_movie_info[3], link=list_of_movie_info[4])

@app.route('/movies', methods=['POST'])
def movies_post():
    form_data=flask.request.form
    print(f'FORM DATA: {form_data}')
    Review.movieID=form_data['movieID']
    Review.rating=form_data['rating']
    Review.review=form_data['review']
    return flask.flash('Thank you for submitting your review!')
    
#app.run()