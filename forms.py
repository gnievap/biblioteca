from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LibrosForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    fk_autor = SelectField('Autor', choices=[], validators=[DataRequired()], coerce=int)
    fk_editorial= SelectField('Editorial', choices=[], validators=[DataRequired()], coerce=int)
    edicion = IntegerField('Edicion', validators=[DataRequired()])
    submit = SubmitField('Agregar Libro')