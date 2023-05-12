from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__.split(".")[0])
app.config.from_object("config.Config")

mysql = MySQL(app)
flaskBcrypt = Bcrypt(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

from flaskProj import views