from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from forms import UploadForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gallery.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'website/static/uploads'

db.init_app(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

from models import Album, Photo

@app.route('/')
def index():
    albums = Album.query.all()
    return render_template('index.html', albums=albums)

@app.route('/album/<int:album_id>')
def gallery(album_id):
    album = Album.query.get_or_404(album_id)
    return render_template('gallery.html', album=album)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.album_name.data:
            album_name = form.album_name.data
            album = Album.query.filter_by(name=album_name).first()
            if not album:
                album = Album(name=album_name)
                db.session.add(album)
                db.session.commit()
        elif form.existing_album.data:
            album = Album.query.get(form.existing_album.data)
        else:
            flash("Please select an existing album or enter a new album name.")
            return redirect(url_for('upload'))

        files = request.files.getlist(form.photos.name)
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = Photo(filename=filename, description=form.description.data, album_id=album.id)
                db.session.add(photo)

        db.session.commit()
        flash("Photos uploaded successfully!")
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
