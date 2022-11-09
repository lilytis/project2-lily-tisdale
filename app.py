import flask

app = flask.Flask(__name__)
app.secret_key='abcdlmt103'

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/handle_form', methods=['POST'])
def handle_username_submission():
    form_data = flask.request.form
    print(f'FORM DATA: {form_data}')
    username = form_data['username']
    if username == 'lily':
        return flask.redirect(flask.url_for('welcome_to_the_matrix'))
    else:
        flask.flash('Try again. Username invalid.')
        return flask.redirect(flask.url_for('index'))

@app.route('/login')
def welcome_to_the_matrix():
    return flask.render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from model import Person

# app = Flask(__name__)

# db = SQLAlchemy(app)
# db.init_app(app)

# @app.route('/')
# def index():
#     return [str(person) for person in Person.query.all()]

# @app.route('/create/<username>/<email>')
# def create(username, email):
#     person = Person(username=username, email=email)
#     db.session.add(person)
#     db.session.commit()
#     return f"created person with username: {username} and email {email}"

# if __name__ == "__main__":
#     app.run(
#         host = os.getenv('IP', '0.0.0.0'),
#         port = int(os.getenv('PORT', 8080)),
#     )
