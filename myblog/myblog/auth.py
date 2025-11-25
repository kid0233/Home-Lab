from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .model import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect!", category="error")
        else:
            flash("Email doesn't exist!", category="error")
    
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        if email_exist:
            flash("Email Already Exists!", category="error")
        elif username_exist:
            flash("Username Already Exists!", category="error")
        elif password1 != password2:
            flash("Passwords don't Match!", category="error")
        elif len(username) < 2:
            flash("Username is too short!", category="error")
        elif len(password1) < 5:
            flash("Password is too short!", category="error")
        elif '@' not in email and len(email) < 4:
            flash("Enter a valid email", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="scrypt"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("New User Added!")
            return redirect(url_for("views.home"))
    
    return render_template("signup.html", user=current_user)

    