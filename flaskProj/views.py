from itsdangerous import SignatureExpired, BadTimeSignature
from pathlib import Path;

from flask import Response, request, render_template, redirect, url_for, flash, jsonify

from flaskProj import app, session, serializer
from flaskProj.loginUtils import LoginForm, sendConfirmation, isLogged
from flaskProj.dbUtils import DBCommands, DBErrors, ValidErrors


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route('/<path:path>')
def index(path, title: str = "OSRS Charting App") -> "html":
    response = Response("index_page")
    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    print(session)
    
    if (path != ""):
        return redirect(url_for("index"))

    return render_template("main/index.html", the_title = title, loginForm = LoginForm())

@app.route('/data', methods=["GET", "POST"])
@isLogged
def data():
    data = {"name": "Joe", "pronouns": "He/Him"}

    return jsonify(data)

@app.route('/popular', methods=["GET", "POST"])
# @isLogged
def popular():
    cache = {"cachedFiles": []}

    for file in Path("./flaskProj/cache/").resolve().iterdir():
        cache["cachedFiles"].append(file.read_text())
    return jsonify(cache)

@app.route("/authentication", methods=["GET", "POST"])
def authentication() -> "html":
    loginForm = LoginForm(formdata=request.form)

    if (loginForm.validate_on_submit()):
        # with DBCommands() as cursor:
        #     cursor.execute("""SELECT *
        #                         FROM users
        #                         WHERE email=%s""", (str(loginForm.userLoginEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
        #     result = cursor.fetchone()

        result = True

        if (result):
            print("result passed")
            tokenHash = serializer.dumps(loginForm.userLoginEmail.data, salt="email-request")
            sendConfirmation(tokenHash, loginForm.userLoginEmail.data)

            flash("Check your Email " + str(loginForm.userLoginEmail.data).split("@")[0] + "!", "success")

            return redirect(url_for("index"))
        
    flash(loginForm.errors, "fail")

    return redirect(url_for("index"))

@app.route("/verify/<token>")
def verify(token):
    try:
        request = serializer.loads(token, salt="email-request", max_age=600)
        flash("Welcome!", "success")
    except SignatureExpired:
        flash("Link expired! Try again.", "fail")

        return redirect(url_for("index"))
    except BadTimeSignature:
        flash("Invalid link! Try again.", "fail")

        return redirect(url_for("index"))
    else:
        session.permanent = False
        session["logged_in"] = True

        return redirect(url_for("index"))

@app.route("/logout", methods=["GET", "POST"])
@isLogged
def logout():
    session.pop("logged_in")
    flash("You are now logged out", "success")
    
    return redirect(url_for("index"))

@app.errorhandler(DBErrors)
def dbErrors():
    return redirect(url_for("index"))

@app.errorhandler(ValidErrors)
def validErrors(error):
    flash(str(error), "fail")

    return redirect(url_for("index"))

