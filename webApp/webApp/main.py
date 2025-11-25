from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    return render_template("main.html", username=current_user.username)