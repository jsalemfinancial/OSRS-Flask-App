from flask import Response, request, render_template, redirect, url_for, flash, jsonify

from flaskProj import app, session, flaskBcrypt
from flaskProj.loginUtils import LoginForm, RegisterForm, isLogged
from flaskProj.dbUtils import DBCommands, DBErrors, ValidErrors

from itsdangerous import URLSafeTimedSerializer


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route('/<path:path>')
def index(path, title: str = "OSRS Charting App") -> "html":
    response = Response("index_page")
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    
    if (path != ""):
        return redirect(url_for("index"))

    return render_template("index.html", the_title = title, loginForm = LoginForm())

@app.route('/data')
def data():
    data = {"name": "Joe", "pronouns": str(flaskBcrypt.generate_password_hash("24"))}

    return jsonify(data)

@app.route("/authentication", methods=["GET", "POST"])
def authentication() -> "html":
    loginForm = LoginForm(formdata=request.form)

    if (loginForm.validate_on_submit()):
        with DBCommands() as cursor:
            cursor.execute("""SELECT *
                                FROM users
                                WHERE email=%s""", (str(loginForm.userLoginEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            result = cursor.fetchone()

        if (result):
            session["logged_in"] = True

            flash("Welcome back, " + str(loginForm.userLoginEmail.data).split("@")[0], "success")
            print("Login Success!")
            return redirect(url_for("index"))
    
    flash("Login unsuccessful", "fail")
    print("Login Fail!")

    return redirect(url_for("index"))

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

