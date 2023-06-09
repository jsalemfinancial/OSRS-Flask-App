from functools import wraps
from threading import Thread

from flask import url_for, render_template, jsonify
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from flaskProj import app, session
from flaskProj.dbUtils import DBCommands

#Login/Register UI Class

class LoginForm(FlaskForm):
    userLoginEmail = StringField("E-mail:", validators=[Length(max=128, message="Email too long."), DataRequired(message="Field empty."), Email(message="Invalid email.", check_deliverability=True)])
    login = SubmitField("Login")

def isLogged(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "logged_in" not in session:
            return jsonify({"notLogged": "Please login!"})

        return function(*args, **kwargs)
    
    return wrapper

def sendEmail(title: str, recipientList: list, htmlTemplate: "html") -> None:
    with app.app_context():
        mail = Mail()
        mail.init_app(app)

        msg = Message(title, recipients=recipientList, html=htmlTemplate)
        mail.send(msg)

def sendConfirmation(tokenData, userEmail):
    confirmURL = url_for("verify", token=tokenData, _external=True)

    html = render_template("auth/email_verification.html", confirmationUrl=confirmURL)

    emailThread = Thread(target=sendEmail, args=[app.config["MAIL_CONFIRMATION_TITLE"], [userEmail], html])
    emailThread.start()