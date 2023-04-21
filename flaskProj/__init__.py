from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager

app = Flask(__name__.split(".")[0])
app.config.from_object("config.Config")

mysql = MySQL(app)
flaskBcrypt = Bcrypt(app)
jwt = JWTManager(app)

from flaskProj import views