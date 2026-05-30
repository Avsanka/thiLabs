import http
import io
import json
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func
import pymysql
import models as cm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/thilabs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dbtest1')
def dbtest1():
    with app.app_context():
        result = db.session.query(
            cm.Session.session_datetime, cm.Session.price, cm.Film.title, cm.Hall.hall_name
        ).join(
            cm.Film, cm.Session.ID_film == cm.Film.film_id
        ).join(
            cm.Hall, cm.Session.ID_hall == cm.Hall.hall_id
        ).order_by(cm.Session.session_datetime).all()
    return render_template("dbtest.html", test1=result)

# @app.route('/dbtest2')
# def dbtest2():
#     with app.app_context():
#         result = db.session.query(
#             cm.Film.title, cm.Film.year, cm.Film.director, cm.Film.duration_mins, cm.Film.rating,
#             cm.Country.country_name, cm.Genre.genre_name
#         ).join(
#             cm.t_film_genre, cm.t_film_genre.ID_film == cm.Film.film_id
#         ).join(
#             cm.Genre, cm.t_film_genre.ID_genre == cm.Genre.genre_id
#         ).join(
#             cm.t_film_country, cm.t_film_country.ID_film == cm.Film.film_id
#         ).join(
#             cm.Country, cm.t_film_country.ID_Country == cm.Country.country_id
#         ).group_by( cm.t_film_country
#             cm.Film.film_id, cm.Film.title
#         ).order_by(cm.Film.year).all()
#         print(result)
#     return render_template("dbtest.html", test2=result)

@app.route('/dbtest2')
def dbtest2():
    with app.app_context():
        query = select(
            cm.Film.title,
            cm.Film.year,
            cm.Film.director,
            cm.Film.duration_mins,
            cm.Film.rating,
            func.group_concat(func.distinct(cm.Country.country_name).op('SEPARATOR')(', ')).label('countries'),
            func.group_concat(func.distinct(cm.Genre.genre_name).op('SEPARATOR')(', ')).label('genres')
        ).select_from(
            cm.Film
        ).outerjoin(
            cm.Film.country
        ).outerjoin(
            cm.Film.genre
        ).group_by(
            cm.Film.film_id
        ).order_by(cm.Film.title)

        result = db.session.execute(query).all()
    return render_template("dbtest.html", test2=result)


# @app.route('/dbtest')
# def dbtest():
#     with app.app_context():
#         result = db.session.query(
#             Users.name, Users.surname, Users.email, Reviews.content
#             ).join(
#             Reviews, Users.user_ID == Reviews.ID_User
#             ).all()
#     return render_template("dbtest.html", list = result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
