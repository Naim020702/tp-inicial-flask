from flask import Blueprint, render_template, flash

predResView = Blueprint("predResView", __name__)

@predResView.route("/pred-res")
def 