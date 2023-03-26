from functools import wraps
from threading import Thread

from flask import redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from flaskProj import app, session
from flaskProj.dbUtils import DBCommands

#Login UI Class

class loginPortal(FlaskForm):
    userEmail = StringField("E-mail:", validators=[DataRequired(), Email(check_deliverability=True)])
    userPassword = PasswordField("Password:", validators=[DataRequired(), Length(min=8, max=32)])
    submitButton = SubmitField("Send Data")

    def sessionStatus(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if ("logged_in") in session:
                return function(*args, **kwargs)
            
            return redirect(url_for("login"))
        
        return wrapper
    
    def validate_userEmail(self, userEmail):
        with DBCommands(app.config["MYSQL_HOST"],app.config["MYSQL_USER"], app.config["MYSQL_PASSWORD"], app.config["MYSQL_DB"], app.config["MYSQL_PORT"]) as cursor:
            cursor.execute("""SELECT email
                                FROM userAccounts
                                WHERE email=%s""", (str(userEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            result = cursor.fetchone()

        if (result):
            raise ValidationError("Email already registered.")
        
    def sendConfirmation(self):
        confirmSerial = URLSafeTimedSerializer(app.config["SECRET_KEY"])

        confirmURL = url_for("verify", token=confirmSerial.dumps(self.userEmail.data, salt="saltsaltsalt"), _external=True)

        html = render_template("email_verification.html", confirmationUrl=confirmURL)

        # sendEmail("Confirm Your Email with Joe's OSRS App", [self.userEmail.data], html)
        emailThread = Thread(target=sendEmail, args=["Confirm Your Email with Joe's OSRS App", [self.userEmail.data], html])
        emailThread.start()

# Verification Routes and Functions

def sendEmail(title: str, recipientList: list, htmlTemplate: "html") -> None:
    with app.app_context():
        mail = Mail()
        mail.init_app(app)

        msg = Message(title, recipients=recipientList, html=htmlTemplate)
        mail.send(msg)

@app.route("/verify/<token>")
def verify(token):
    try:
        confirmSerial = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        userEmail = confirmSerial.loads(token, salt="saltsaltsalt", max_age=600)
    except:
        flash("Invalid Confirmation Link!", "fail")
        return redirect(url_for("login"))

    with DBCommands(app.config["MYSQL_HOST"],app.config["MYSQL_USER"], app.config["MYSQL_PASSWORD"], app.config["MYSQL_DB"], app.config["MYSQL_PORT"]) as cursor:
        cursor.execute("""SELECT verified
                            FROM userAccounts
                            WHERE email=%s""", (str(userEmail).lower(),)) #Extra ',' at end to tell python to unpack tuple.
        result = cursor.fetchone()

    if (result):
        flash("Account is already confirmed. You may login.", "fail")
        return redirect(url_for("landing"))
    else:
        with DBCommands(app.config["MYSQL_HOST"],app.config["MYSQL_USER"], app.config["MYSQL_PASSWORD"], app.config["MYSQL_DB"], app.config["MYSQL_PORT"]) as cursor:
            cursor.execute("""UPDATE userAccounts
                                SET verified=True
                                WHERE email=%s""", (str(userEmail).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            
        flash("Account verified!", "success")
            
    return redirect(url_for("landing"))

