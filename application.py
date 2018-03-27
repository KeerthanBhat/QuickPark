import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
import datetime
from helpers import *

now = datetime.datetime.now()

#configure application
app = Flask(__name__)

#ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
        
#configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///park.db")

#home route
@app.route("/")
def home():
    return render_template("home.html")
    
#login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    #forget any user_id
    session.clear()

    #if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        #ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        #query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        #ensure username exists and password is correct
        if len(rows) != 1 or str(rows[0]["hash"]) != str(request.form.get("password")):
            return apology("invalid username and/or password")

        #remember which user has logged in
        session["user_id"] = rows[0]["id"]

        #redirect user to home page
        return redirect(url_for("myhome"))

    #else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user."""
    
    #forget any user_id
    session.clear()

    #if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        #ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        #ensure password was entered again
        elif not request.form.get("password1"):
            return apology("must re-enter password")
            
        #ensure that the passwords match
        if request.form.get("password") != request.form.get("password1"):
            return apology("Passwords doesn't match!")

        #query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        #ensure username is available
        if len(rows) == 1: 
            return apology("Sorry, username already taken.")

        
        #insert data into the database
        user = db.execute("INSERT INTO users ( username, hash ) VALUES( :username, :pwhash )", username = request.form.get("username"), pwhash = (request.form.get("password")))
        
        #remember which user has logged in
        session["user_id"] = user
        
        #redirect user to home page
        return redirect(url_for("myhome"))

    #else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")
    
@app.route("/logout")
def logout():
    """Log user out."""

    #forget any user_id
    session.clear()

    #redirect user to login form
    return redirect(url_for("login"))
    
#myhome route
@app.route("/myhome")
def myhome():
    return render_template("myhome.html")

#find route
@app.route("/find", methods=["GET", "POST"])
def find():
    
    spots = db.execute( "SELECT * FROM spot WHERE avail > '0'")
    return render_template("find.html")
    
#rent route
@app.route("/rent", methods=["GET", "POST"])
def rent():
    return render_template("rent.html")