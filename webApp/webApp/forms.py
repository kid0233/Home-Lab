from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError
from .model import User

#Create a form class
class SignupForm(FlaskForm):
    username = StringField("Username ", validators=[InputRequired(message="Username can't be blank"), Length(min=4)])
    email = StringField("Email", validators=[InputRequired(message="Email can't be blank"), Email()])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank"), Length(min=5)])
    confirm = PasswordField("Confirm Password", validators=[InputRequired(message="Password can't be blank"), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username alreasy exist. Please choose another!")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exist. Try the Login Page")
    


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(message="Email can't be blank"), Email()])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank"), Length(min=5)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Title cannot be blank"), Length(min=3)])
    content = TextAreaField("Content", validators=[InputRequired(message="Content cannot be blank"), Length(min=3)])
    author = StringField("Author", validators=[InputRequired(message="Missing Author"), Length(min=3)])
    slug = StringField("Slug", validators=[InputRequired(message="Cannot be Blank")])
    submit = SubmitField("Submit Post")
