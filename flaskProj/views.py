from flask import request, render_template, redirect, url_for, flash

from flaskProj import app, session, flaskBcrypt
from flaskProj.loginUtils import LoginForm, RegisterForm, isLogged
from flaskProj.dbUtils import DBCommands, DBErrors, ValidErrors

from itsdangerous import URLSafeTimedSerializer


@app.route("/", methods=["GET", "POST"])
def index(title: str = "Joe's Web App") -> "html":
    clientAddress = request.environ.get("REMOTE_ADDR")
    serverAddress = request.environ.get("SERVER_NAME")
    requestHost = request.environ.get("HTTP_HOST")
    
    return render_template("index.html", the_title = title,
                                            the_client_address = clientAddress, 
                                            the_server_address = serverAddress, 
                                            the_host = requestHost)

@app.route("/userpage", methods=["GET", "POST"])
@isLogged
def userPage() -> str:
    return "This is a logged-in user page!"

@app.route("/userPortal", methods=["GET", "POST"])
def userPortal(title: str = "User Portal") -> "html":
    if ("logged_in" not in session):
        loginForm = LoginForm()
        registerForm = RegisterForm()

        return render_template("auth/user_portal.html", the_title = title, loginForm=loginForm, registerForm=registerForm)
    
    else:
        flash("Already logged in!", "fail")

        return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login(title: str = "Logging in...") -> "html":
    loginForm = LoginForm(formdata=request.form)

    if (loginForm.validate_on_submit()):
        with DBCommands() as cursor:
            cursor.execute("""SELECT *
                                FROM userAccounts
                                WHERE email=%s""", (str(loginForm.userLoginEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            result = cursor.fetchone()

        if (result):
            print(loginForm.userLoginEmail.data, loginForm.userLoginPassword.data, result["password"])
            print(flaskBcrypt.check_password_hash(result["password"], str(loginForm.userLoginPassword.data)))

        if (result and flaskBcrypt.check_password_hash(result["password"], str(loginForm.userLoginPassword.data))):
            session["logged_in"] = True

            flash("Welcome back, " + str(loginForm.userLoginEmail.data).split("@")[0], "success")
            return redirect(url_for("index"))
    
    flash("Login unsuccessful", "fail")
    
    return redirect(url_for("userPortal"))

@app.route("/register", methods=["GET", "POST"])
def register(title: str = "Registering...") -> "html":
    registerForm = RegisterForm(formdata=request.form)
    
    if (registerForm.validate_on_submit()):
        with DBCommands() as cursor:
            cursor.execute("""SELECT email
                            FROM userAccounts
                            WHERE email=%s""", (str(registerForm.userRegisterEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            result = cursor.fetchone()

        if (result):
            raise ValidErrors("Email is already registered.")

        passwordHash = flaskBcrypt.generate_password_hash(str(registerForm.userRegisterPassword.data)).decode('utf-8')
        userEmail = registerForm.userRegisterEmail.data

        with DBCommands() as cursor:
            cursor.execute("""INSERT INTO userAccounts
                            VALUES (%s, %s, %s)""", (str(userEmail).lower(), passwordHash, False))
            
        registerForm.sendConfirmation()
            
        flash("Submitted successfully, " + str(userEmail).split("@")[0] + ". Please check your email!", "success")

        return redirect(url_for("index"))
    
    return redirect(url_for("userPortal"))
    
@app.route("/logout", methods=["GET", "POST"])
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

    if (result and result["verified"]):
        flash("Account is already confirmed. You may login.", "fail")

        return redirect(url_for("index"))
    
    else:
        with DBCommands() as cursor:
            cursor.execute("""UPDATE userAccounts
                                SET verified=True
                                WHERE email=%s""", (str(userEmail).lower(),)) #Extra ',' at end to tell python to unpack tuple.
        flash("Account verified!", "success")
            
    return redirect(url_for("index"))

@app.errorhandler(DBErrors)
def dbErrors():
    return redirect(url_for("index"))

@app.errorhandler(ValidErrors)
def validErrors(error):
    flash(str(error), "fail")

    return redirect(url_for("index"))

