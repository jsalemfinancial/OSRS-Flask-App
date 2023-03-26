from flask import Flask, session
from flask_bcrypt import Bcrypt

app = Flask(__name__.split(".")[0])
app.config.from_object("config.Config")

flaskBcrypt = Bcrypt(app)

from flaskProj import routes