from flask import request, render_template, redirect, url_for, flash
from flaskProj import app, session, flaskBcrypt
from flaskProj.loginUtils import loginPortal
from flaskProj.dbUtils import DBCommands, DBErrors

@app.route("/", methods=["GET", "POST"])
def landing(title: str = "Joe's Web App") -> "html":
    clientAddress = request.environ.get("REMOTE_ADDR")
    serverAddress = request.environ.get("SERVER_NAME")
    requestHost = request.environ.get("HTTP_HOST")
    
    return render_template("landing.html", the_title = title,
                                            the_client_address = clientAddress, 
                                            the_server_address = serverAddress, 
                                            the_host = requestHost)

@app.route("/login", methods=["GET", "POST"])
def login(title: str = "Login Portal") -> "html":
    try:
        LoginForm = loginPortal()

        if (LoginForm.validate_on_submit()):
            passwordHash = flaskBcrypt.generate_password_hash(LoginForm.userPassword.data).decode("utf-8")
            userEmail = LoginForm.userEmail.data

            with DBCommands(app.config["DB_CONFIG"]) as cursor:
                cursor.execute("""INSERT INTO userAccounts
                                VALUES (%s, %s, %s)""", (str(userEmail).lower(), str(passwordHash), False))
                
            LoginForm.sendConfirmation()
                
            flash("Submitted successfully, " + str(userEmail).split("@")[0] + ". Please check your email!", "success")

            return redirect(url_for("landing"))

        return render_template("login.html", the_title = title, form=LoginForm)
    except DBErrors as error:
        print("Caught Error!", error)
    return "Error-Page TBA"


@app.route("/logout", methods=["GET", "POST"])
@loginPortal.sessionStatus
def logout() -> str:
    session.pop("logged_in")

    return "You are now logged out."

@app.route("/userpage", methods=["GET", "POST"])
@loginPortal.sessionStatus
def userPage() -> str:
    return "This is a logged-in user page!"