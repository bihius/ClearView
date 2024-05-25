import sys
import os

# Dodaj ścieżkę do katalogu głównego projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions import db
from app import app
from models import Album, Photo


def create_database(load_dummy_data=False):
    with app.app_context():
        # Usuń istniejącą bazę danych, jeśli istnieje
        db_path = os.path.join(app.root_path, 'gallery.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        db.create_all()
        print("Database created successfully.")

        if load_dummy_data:
            load_dummy_photos()


def load_dummy_photos():
    album_name = "Default Album"
    album = Album.query.filter_by(name=album_name).first()
    if not album:
        album = Album(name=album_name)
        db.session.add(album)
        db.session.commit()

    for i in range(1, 21):
        photo = Photo(filename="dummy.png", description=f"Dummy photo {i}", album_id=album.id)
        db.session.add(photo)

    db.session.commit()
    print("20 dummy photos added to the database.")


if __name__ == "__main__":
    load_dummy_data = "--load-dummy-data" in sys.argv
    create_database(load_dummy_data)
