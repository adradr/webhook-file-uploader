import os
from urllib import response
from flask import Flask, flash, request, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER_MOVIES = 'files/' + \
    os.getenv('MOVIES_FOLDER')  # 'files/PLEX_movies'
UPLOAD_FOLDER_SERIES = 'files/' + \
    os.getenv('SERIES_FOLDER')  # 'files/PLEX_series'
UPLOAD_FOLDER_MOVIES_KIDS = 'files/' + \
    os.getenv('MOVIES_KIDS_FOLDER')  # 'files/PLEX_movies'
UPLOAD_FOLDER_SERIES_KIDS = 'files/' + \
    os.getenv('SERIES_KIDS_FOLDER')  # 'files/PLEX_series'
ALLOWED_EXTENSIONS = {'torrent'}

if not os.path.exists(UPLOAD_FOLDER_MOVIES):
    os.makedirs(UPLOAD_FOLDER_MOVIES)
if not os.path.exists(UPLOAD_FOLDER_SERIES):
    os.makedirs(UPLOAD_FOLDER_SERIES)

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER_MOVIES'] = UPLOAD_FOLDER_MOVIES
app.config['UPLOAD_FOLDER_SERIES'] = UPLOAD_FOLDER_SERIES
app.config['UPLOAD_FOLDER_MOVIES_KIDS'] = UPLOAD_FOLDER_MOVIES_KIDS
app.config['UPLOAD_FOLDER_SERIES_KIDS'] = UPLOAD_FOLDER_SERIES_KIDS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


users = {
    os.getenv('USERNAME'): generate_password_hash(os.getenv('PASSWORD')),
}
app.logger.info("Basic Auth:\n%s" % (users))


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/movies', methods=['POST'])
@auth.login_required
def upload_movies():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return Response(status=403)
        file = request.files['file']
        app.logger.info(file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return Response(status=403)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER_MOVIES'], filename))
            return Response(status=200)
    return Response(status=403)


@app.route('/series', methods=['POST'])
@auth.login_required
def upload_series():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return Response(status=403)
        file = request.files['file']
        app.logger.info(file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return Response(status=403)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER_SERIES'], filename))
            return Response(status=200)
    return Response(status=403)


@app.route('/movies-kids', methods=['POST'])
@auth.login_required
def upload_movies():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return Response(status=403)
        file = request.files['file']
        app.logger.info(file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return Response(status=403)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER_MOVIES_KIDS'], filename))
            return Response(status=200)
    return Response(status=403)


@app.route('/series-kids', methods=['POST'])
@auth.login_required
def upload_series():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return Response(status=403)
        file = request.files['file']
        app.logger.info(file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return Response(status=403)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER_SERIES_KIDS'], filename))
            return Response(status=200)
    return Response(status=403)


if __name__ == "__main__":
    sess.init_app(app)
    app.run(debug=True)
