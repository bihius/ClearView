from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from models import Album

class UploadForm(FlaskForm):
    album_name = StringField('Album Name', validators=[Optional()])
    existing_album = SelectField('Choose Existing Album', coerce=int, validators=[Optional()])
    photos = FileField('Photos', validators=[DataRequired()], render_kw={"multiple": True})
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Upload')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_album.choices = [(album.id, album.name) for album in Album.query.all()]
