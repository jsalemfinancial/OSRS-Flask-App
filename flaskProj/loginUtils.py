from functools import wraps
from threading import Thread

from flask import redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, StopValidation

from flaskProj import app, session, flaskBcrypt
from flaskProj.dbUtils import DBCommands, DBErrors

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

        if (result):
            raise StopValidation("Email already registered.")
        
    def sendConfirmation(self):
        confirmSerial = URLSafeTimedSerializer(app.config["SECRET_KEY"])

        confirmURL = url_for("verify", token=confirmSerial.dumps(self.userRegisterEmail.data, salt="saltsaltsalt"), _external=True)

        html = render_template("email_verification.html", confirmationUrl=confirmURL)

        emailThread = Thread(target=sendEmail, args=["Confirm Your Email with Joe's OSRS App", [self.userRegisterEmail.data], html])
        emailThread.start()

# Verification Routes and Functions

def isLogged(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if ("logged_in") in session:
            return function(*args, **kwargs)
        
        return redirect(url_for("userPortal"))
    
    return wrapper

def sendEmail(title: str, recipientList: list, htmlTemplate: "html") -> None:
    with app.app_context():
        mail = Mail()
        mail.init_app(app)

        msg = Message(title, recipients=recipientList, html=htmlTemplate)
        mail.send(msg)

@app.route("/userPortal", methods=["GET", "POST"])
def userPortal(title: str = "User Portal") -> "html":
    if ("logged_in" not in session):
        loginForm = LoginForm()
        registerForm = RegisterForm()

        return render_template("user_portal.html", the_title = title, loginForm=loginForm, registerForm=registerForm)
    else:
        flash("Already logged in!", "fail")

        return redirect(url_for("landing"))

@app.route("/login", methods=["GET", "POST"])
def login(title: str = "Logging in. . .") -> "html":
    try:
        loginForm = LoginForm()
        registerForm = RegisterForm()

        if (loginForm.validate_on_submit()):
            # Do Stuff. . .
                        
            flash("Welcome back, " + str(loginForm.userLoginEmail.data).split("@")[0], "success")

            return redirect(url_for("landing"))
    except DBErrors as error:
        print("Caught Error!", error)

        return "Error-Page TBA"
    
    return render_template("user_portal.html", the_title = title, loginForm=loginForm, registerForm=registerForm)

@app.route("/register", methods=["GET", "POST"])
def register(title: str = "Registering. . .") -> "html":
    try:
        loginForm = LoginForm()
        registerForm = RegisterForm()
        
        if (registerForm.validate_on_submit()):
            with DBCommands() as cursor:
                cursor.execute("""SELECT email
                                FROM userAccounts
                                WHERE email=%s""", (str(registerForm.userRegisterEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
                result = cursor.fetchone()

            if (result):
                raise ValidationError("Email is already registered.")
            
            passwordHash = flaskBcrypt.generate_password_hash(registerForm.userRegisterPassword.data).decode("utf-8")
            userEmail = registerForm.userRegisterEmail.data

            with DBCommands() as cursor:
                cursor.execute("""INSERT INTO userAccounts
                                VALUES (%s, %s, %s)""", (str(userEmail).lower(), str(passwordHash), False))
                
            registerForm.sendConfirmation()
                
            flash("Submitted successfully, " + str(userEmail).split("@")[0] + ". Please check your email!", "success")

            return redirect(url_for("landing"))
        
        return render_template("user_portal.html", the_title = title, loginForm=loginForm, registerForm=registerForm)
    except DBErrors as error:
        flash("DB Error: " + error, "fail")

        return redirect(url_for("userPortal"))
    except ValidationError as error:
        flash(str(error), "fail")
        return redirect(url_for("userPortal"))
    
    

@app.route("/logout", methods=["POST"])
@isLogged
def logout() -> str:
    session.pop("logged_in")

    return "You are now logged out."

@app.route("/verify/<token>")
def verify(token):
    try:
        confirmSerial = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        userEmail = confirmSerial.loads(token, salt="saltsaltsalt", max_age=600)
    except:
        flash("Invalid Confirmation Link!", "fail")

        return redirect(url_for("userPortal"))

    with DBCommands() as cursor:
        cursor.execute("""SELECT verified
                            FROM userAccounts
                            WHERE email=%s""", (str(userEmail).lower(),)) #Extra ',' at end to tell python to unpack tuple.
        result = cursor.fetchone()

    if (result):
        flash("Account is already confirmed. You may login.", "fail")

        return redirect(url_for("landing"))
    else:
        with DBCommands() as cursor:
            cursor.execute("""UPDATE userAccounts
                                SET verified=True
                                WHERE email=%s""", (str(userEmail).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            
        flash("Account verified!", "success")
            
    return redirect(url_for("landing"))

