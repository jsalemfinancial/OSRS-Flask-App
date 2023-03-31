from flask import request, render_template, redirect, url_for, flash

from flaskProj import app, session, flaskBcrypt
from flaskProj.loginUtils import isLogged

@app.route("/", methods=["GET", "POST"])
def landing(title: str = "Joe's Web App") -> "html":
    clientAddress = request.environ.get("REMOTE_ADDR")
    serverAddress = request.environ.get("SERVER_NAME")
    requestHost = request.environ.get("HTTP_HOST")
    
    return render_template("landing.html", the_title = title,
                                            the_client_address = clientAddress, 
                                            the_server_address = serverAddress, 
                                            the_host = requestHost)

@app.route("/userpage", methods=["GET", "POST"])
@isLogged
def userPage() -> str:
    return "This is a logged-in user page!"