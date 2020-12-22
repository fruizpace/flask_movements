# nuestro fichero de formularios
from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length



class MovementForm(FlaskForm):
    #id = IntegerField('id') # no lo necesitamos
    fecha = DateField('Fecha', validators=[DataRequired()]) # le ponemos el nombre que tendrá y lo validamos
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=5, message="El concepto debe tener más de 5 caracteres")])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])

    submit = SubmitField('Aceptar')
