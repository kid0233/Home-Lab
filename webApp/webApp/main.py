from flask import Blueprint, render_template, abort, url_for, redirect, flash, current_app
from jinja2 import TemplateNotFound
from flask_login import login_required, current_user
from .forms import PostForm
from .model import Post
from . import db

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    try:
        posts = Post.query.order_by(Post.date_posted)
        return render_template("main.html", posts=posts)
    except TemplateNotFound as e:
        current_app.logger.info("Error finding post", exc_info=e)
        abort(404)

@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    id = current_user.id
    post = Post.query.get_or_404(id)
    return render_template("dashboard.html", post=post)

@main.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # Clear form data
        form.title.data = ""
        form.content.data = ""
        form.author.data = ""
        form.slug.data = ""

        #Add Post Data to Database
        db.session.add(post)
        db.session.commit()
        current_app.logger.info(f"Author: {post.author} Post Added!")
        flash("Post Added!", category="info")
    
    return render_template("add-post.html", form=form)

@main.route("/posts/<int:id>")
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("posts.html", post=post, username=current_user.username)

@main.route("/posts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post Edited Successfully", category="warning")
        current_app.logger.info(f"{post.author} Post Edited Successfully")
        return redirect(url_for('main.post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template("edit-post.html", form=form)

@main.route("/posts/delete/<int:id>")
@login_required
def delete_post(id: int):
    post_to_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post Deleted Successfully", category="warning")
        current_app.logger.info("Post Deleted Successfully")
        posts = Post.query.order_by(Post.date_posted)
        return render_template("main.html", posts=posts)
    except:
        flash("Post not Deleted", category="danger")
        posts = Post.query.order_by(Post.date_posted)
        return render_template("main.html", posts=posts)

@main.app_errorhandler(404)
@login_required
def page_not_found(e):
    return render_template("404.html"), 404