from flask import Response, request, render_template, redirect, url_for, flash, jsonify

from flaskProj import app, session, flaskBcrypt
from flaskProj.loginUtils import LoginForm, RegisterForm, isLogged
from flaskProj.dbUtils import DBCommands, DBErrors, ValidErrors

from itsdangerous import URLSafeTimedSerializer


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route('/<path:path>')
def index(path, title: str = "Joe's Web App") -> "html":
    response = Response("index_page")
    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    clientAddress = request.environ.get("REMOTE_ADDR")
    serverAddress = request.environ.get("SERVER_NAME")
    requestHost = request.environ.get("HTTP_HOST")
    
    if (path != ""):
        return redirect(url_for("index"))

    return render_template("index.html", the_title = title,
                                            the_client_address = clientAddress, 
                                            the_server_address = serverAddress, 
                                            the_host = requestHost, loginForm = LoginForm())

@app.route('/data')
def data():
    data = {"name": "Joe", "pronouns": str(flaskBcrypt.generate_password_hash("24"))}

    return jsonify(data)

# @app.route("/userpage", methods=["GET", "POST"])
# @isLogged
# def userPage() -> str:
#     return "This is a logged-in user page!"

# @app.route("/userPortal", methods=["GET", "POST"])
# def userPortal(title: str = "User Portal") -> "html":
#     if ("logged_in" not in session):
#         loginForm = LoginForm()
#         registerForm = RegisterForm()

#         return render_template("auth/user_portal.html", the_title = title, loginForm=loginForm, registerForm=registerForm)
    
#     else:
#         flash("Already logged in!", "fail")

#         return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login() -> "html":
    loginForm = LoginForm(formdata=request.form)

    if (loginForm.validate_on_submit()):
        # with DBCommands() as cursor:
        #     cursor.execute("""SELECT *
        #                         FROM userAccounts
        #                         WHERE email=%s""", (str(loginForm.userLoginEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
        #     result = cursor.fetchone()

        if (loginForm.userLoginEmail.data == "jamal@gmail.com"):
            session["logged_in"] = True

            flash("Welcome back, " + str(loginForm.userLoginEmail.data).split("@")[0], "success")
            print("Login Success!")
            return redirect(url_for("index"))
    
    flash("Login unsuccessful", "fail")
    print("Login Fail!")

    return redirect(url_for("index"))

# @app.route("/register", methods=["GET", "POST"])
# def register(title: str = "Registering...") -> "html":
#     registerForm = RegisterForm(formdata=request.form)
    
#     if (registerForm.validate_on_submit()):
#         with DBCommands() as cursor:
#             cursor.execute("""SELECT email
#                             FROM userAccounts
#                             WHERE email=%s""", (str(registerForm.userRegisterEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
#             result = cursor.fetchone()

#         if (result):
#             raise ValidErrors("Email is already registered.")

#         passwordHash = flaskBcrypt.generate_password_hash(str(registerForm.userRegisterPassword.data)).decode('utf-8')
#         userEmail = registerForm.userRegisterEmail.data

#         with DBCommands() as cursor:
#             cursor.execute("""INSERT INTO userAccounts
#                             VALUES (%s, %s, %s)""", (str(userEmail).lower(), passwordHash, False))
            
#         registerForm.sendConfirmation()
            
#         flash("Submitted successfully, " + str(userEmail).split("@")[0] + ". Please check your email!", "success")

#         return redirect(url_for("index"))
    
#     return redirect(url_for("userPortal"))
    
# @app.route("/logout", methods=["GET", "POST"])
# @isLogged
# def logout() -> str:
#     session.pop("logged_in")

#     return "You are now logged out."

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

    if (result and result[2]):
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

