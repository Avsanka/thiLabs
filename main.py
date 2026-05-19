import http
import io
import json
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
from models import Users, Reviews


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/thilabs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dbtest')
def dbtest():
    with app.app_context():
        result = db.session.query(
            Users.name, Users.surname, Users.email, Reviews.content
            ).join(
            Reviews, Users.user_ID == Reviews.ID_User
            ).all()
    return render_template("dbtest.html", list = result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
