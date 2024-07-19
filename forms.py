from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class LibrosForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    fk_autor = IntegerField('Autor ID', validators=[DataRequired()])
    fk_editorial=IntegerField('Editorial ID', validators=[DataRequired()])
    edicion = IntegerField('Edicion', validators=[DataRequired()])
    submit = SubmitField('Agregar Libro')