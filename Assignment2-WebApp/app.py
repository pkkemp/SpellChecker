from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_wtf.csrf import CSRFProtect

import unittest, os

app = Flask(__name__)
csrf = CSRFProtect(app)
userList = []
session = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# class UnitTests(unittest.TestCase):
#     def test_findUser(self):



class user:
  def __init__(self, username, password, twofactor):
    self.username = username
    self.password = password
    self.twofactor = twofactor

    # getter method
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

class response:
    def __init__(self, input, response):
        self.input = input
        self.response = response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spell_check", methods=["GET", "POST"])
def spell_check():
    if session == False:
        return redirect(url_for("login"))
    else:
        data = response
        if request.method == "POST":
            inputtext = request.form["inputtext"]
            data.input = inputtext
            from subprocess import call
            #call(["./a.out"])
            if inputtext is not None and inputtext is not "" :
                return render_template("spell_check.html", data = data)
        return render_template("spell_check.html", data=data)


def findUser(username, userList):
    for x in userList:
        if x.username == username:
            return x
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    data = ""
    if request.method == "POST":
        uname = request.form["uname"]
        pword = request.form["pword"]
        twofact = request.form["2fa"]
        theUser = findUser(uname, userList)
        if theUser is not None:
            if theUser.password == pword and theUser.twofactor == twofact:
                global session
                session = True
                data = "success"
                #return redirect(url_for("spell_check"))



    return render_template("login.html", data = data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        pword = request.form['pword']
        twofact = request.form['2fa']

        register = user(username=uname, password=pword, twofactor=twofact)
        # need to check here to see if the user already exists, if they do we don't need to recreate their account.
        global userList
        theUser = findUser(uname, userList)
        success = "Account creation failure"
        if theUser is None:
            userList.append(register)
            success = "Account creation success"
        return render_template("register.html", data=success)

        return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
