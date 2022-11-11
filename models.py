from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    # def __repr__(self):
    #     return f"Person with username: {self.username}"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating_score = db.Column(db.Integer)
    review = db.Column(db.String(500))
    
