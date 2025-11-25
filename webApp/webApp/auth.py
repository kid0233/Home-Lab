from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .model import User
from .forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Login Successful", category="success")
                login_user(user, remember=True)
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
            login_user(new_user, remember=True)
            flash("Account Created!", category="success")
            return redirect(url_for("main.index"))
    return render_template("signup.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))