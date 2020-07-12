from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    edit_first_name = StringField('First Name', validators=[DataRequired()])
    edit_age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Enter')
