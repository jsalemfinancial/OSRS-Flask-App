from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__.split(".")[0])
app.config.from_object("config.Config")

flaskBcrypt = Bcrypt(app)
mysql = MySQL(app)

from flaskProj import routes