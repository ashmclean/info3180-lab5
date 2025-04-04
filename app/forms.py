# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(message="Title is required.")])
    description = TextAreaField('Description', validators=[DataRequired(message="Description is required.")])
    poster = FileField('Movie Poster', validators=[
        FileRequired(message="A movie poster is required."),
        FileAllowed(['jpg', 'jpeg', 'png'], message="Only image files are allowed (jpg, png, gif).")
    ])
