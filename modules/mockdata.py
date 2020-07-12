from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class MockDataForm(FlaskForm):
    amount = IntegerField('amount', validators=[DataRequired()])
    submit = SubmitField('Enter')
