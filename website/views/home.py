from flask import Blueprint, render_template

homeView = Blueprint("home", __name__)

@homeView.route("/")
def home():
    # return "<h1>Hello, World!</h1>"
    return render_template("home.html")