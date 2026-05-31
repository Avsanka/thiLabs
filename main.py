import http
import io
import json
from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, desc
import pymysql
import models as cm
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/thilabs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getFilms', methods=['GET'])
def getFilms():
    with app.app_context():
        result = db.session.query(
           cm.Film.film_id, cm.Film.title, cm.Film.year, cm.Film.rating, cm.Film.director
        ).order_by(cm.Film.rating.desc()).all()

        films = []
        for film in result:
            films.append({
                'id': film.film_id,
                'title': film.title,
                'year': film.year,
                'rating': float(film.rating),
                'director': film.director
            })
    return jsonify(films)

@app.route('/filmInfo')
def renderFilmInfo():
    return render_template("filmInfo.html")

@app.route('/filmInfoById', methods=['GET'])
def filmInfo():
    film_id = request.args.get('id', 0)
    with app.app_context():
        query = select(
            cm.Film.film_id,
            cm.Film.title,
            cm.Film.year,
            cm.Film.director,
            cm.Film.duration_mins,
            cm.Film.description,
            cm.Film.rating,
            cm.Film.img_url,
            func.group_concat(func.distinct(cm.Country.country_name).op('SEPARATOR')(', ')).label('countries'),
            func.group_concat(func.distinct(cm.Genre.genre_name).op('SEPARATOR')(', ')).label('genres')
        ).select_from(
            cm.Film
        ).outerjoin(
            cm.Film.country
        ).outerjoin(
            cm.Film.genre
        ).where(
            cm.Film.film_id == film_id
        ).group_by(
            cm.Film.film_id
        ).order_by(cm.Film.title)

        film = db.session.execute(query).first()
        result = [({
                'id': film.film_id,
                'title': film.title,
                'year': film.year,
                'rating': float(film.rating),
                'director': film.director,
                'duration': film.duration_mins,
                'description': film.description,
                'genre': film.genres,
                'country': film.countries,
                'img': film.img_url
            })]
    return jsonify(result)

@app.route('/sessions')
def renderSessions():
    return render_template('sessions.html')

@app.route('/getSessions', methods=['GET'])
def getSessions():
    now = datetime.now()
    allSessions = request.args.get('allSessions', 0)
    with app.app_context():
        now = datetime.now()
        today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)

        if int(allSessions) == 1:
            result = db.session.query(
                cm.Session.session_id, cm.Session.session_datetime, cm.Session.price,
                cm.Film.title, cm.Film.year, cm.Film.img_url, cm.Hall.hall_name
            ).join(
                cm.Film, cm.Session.ID_film == cm.Film.film_id
            ).join(
                cm.Hall, cm.Session.ID_hall == cm.Hall.hall_id
            ).filter(
                cm.Session.session_datetime >= today_start,
                cm.Session.session_datetime > now
            ).all()
        else:
            result = db.session.query(
                cm.Session.session_id, cm.Session.session_datetime, cm.Session.price,
                cm.Film.title, cm.Film.year, cm.Film.img_url, cm.Hall.hall_name
            ).join(
                cm.Film, cm.Session.ID_film == cm.Film.film_id
            ).join(
                cm.Hall, cm.Session.ID_hall == cm.Hall.hall_id
            ).filter(
                cm.Session.session_datetime >= today_start,
                cm.Session.session_datetime <= today_end,
                cm.Session.session_datetime > now
            ).all()

    sessions = []
    for item in result:
        sessions.append({
            'id': item.session_id,
            'datetime': item.session_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'price': float(item.price),
            'title': item.title,
            'year': item.year,
            'img': item.img_url,
            'hall': item.hall_name
        })
    return jsonify(sessions)


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





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
