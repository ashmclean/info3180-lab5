"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from app.forms import MovieForm
from app.models import Movie
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from flask_wtf.csrf import CSRFProtect, CSRFError
csrf = CSRFProtect(app)
###
# Routing for your application.
###

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@csrf.exempt
@app.route('/api/v1/movies', methods=['POST'])
def movies():
    if 'poster' not in request.files:
        return jsonify({"errors": [{"poster": "Poster is required"}]}), 400

    title = request.form.get('title')
    description = request.form.get('description')
    poster = request.files['poster']

    if not title or not description or poster.filename == '':
        return jsonify({"errors": [{"form": "All fields are required."}]}), 400

    try:
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save to DB only if model is ready
        # movie = Movie(title=title, description=description, poster=filename)
        # db.session.add(movie)
        # db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": title,
            "poster": filename,
            "description": description
        }), 201

    except Exception as e:
        return jsonify({"errors": [{"exception": str(e)}]}), 500

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({"csrf_token": generate_csrf()})