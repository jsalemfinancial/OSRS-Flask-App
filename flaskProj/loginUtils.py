from functools import wraps
from threading import Thread

from flask import redirect, url_for, render_template, flash, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, StopValidation

from flaskProj import app, session
from flaskProj.dbUtils import DBCommands

#Login/Register UI Class

class LoginForm(FlaskForm):
    userLoginEmail = StringField("E-mail:", validators=[DataRequired("Please fill email."), Email(message="Invalid email.", check_deliverability=True)])
    userLoginPassword = PasswordField("Password:", validators=[DataRequired("Please fill password."), Length(min=8, max=32)])
    login = SubmitField("Login")

class RegisterForm(FlaskForm):
    userRegisterEmail = StringField("E-mail:", validators=[DataRequired("Please fill email."), Email(message="Invalid email.", check_deliverability=True)])
    userRegisterPassword = PasswordField("Password:", validators=[DataRequired("Please fill password."), Length(min=8, max=32)])
    userPasswordVerify = PasswordField("Verify Password:", validators=[DataRequired(), EqualTo("userRegisterPassword", message="Password does not match.")])
    register = SubmitField("Register Account")
    
    def validate_userRegistered(self, userEmail):
        with DBCommands() as cursor:
            cursor.execute("""SELECT email
                                FROM userAccounts
                                WHERE email=%s""", (str(userEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            result = cursor.fetchone()

        if (result[0]):
            raise StopValidation("Email already registered.")
        
    def sendConfirmation(self):
        confirmSerial = URLSafeTimedSerializer(app.config["SECRET_KEY"])

        confirmURL = url_for("verify", token=confirmSerial.dumps(self.userRegisterEmail.data, salt="saltsaltsalt"), _external=True)

        html = render_template("auth/email_verification.html", confirmationUrl=confirmURL)

        emailThread = Thread(target=sendEmail, args=["Confirm Your Email with Joe's OSRS App", [self.userRegisterEmail.data], html])
        emailThread.start()

# Verification Functions

def isLogged(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if ("logged_in") in session:
            return function(*args, **kwargs)
        
        flash("Please Login", "fail")
        return redirect(url_for("userPortal"))
    
    return wrapper

def sendEmail(title: str, recipientList: list, htmlTemplate: "html") -> None:
    with app.app_context():
        mail = Mail()
        mail.init_app(app)

        msg = Message(title, recipients=recipientList, html=htmlTemplate)
        mail.send(msg)