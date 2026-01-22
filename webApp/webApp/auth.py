from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from . import db
from .model import User
from .forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Login Successful", category="success")
                login_user(user, remember=form.remember.data)
                current_app.logger.info(f"{user} has logged in")
                return redirect(url_for("main.index"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Username is incorrect!", category="error")
    
    return render_template("login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
            hash_password = generate_password_hash(form.password.data, method="scrypt")
            new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            current_app.logger.info(f"{new_user.username} account ctreated")
            flash("Account Created!", category="success")
            return redirect(url_for("main.index"))
    return render_template("signup.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    current_app.logger.info("User has logged out")
    flash("You are logged out!", category="warning")
    return redirect(url_for("auth.login"))