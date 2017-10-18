from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class LoginForm(Form):
    # response = TextField('response', validators=[DataRequired()])
    response = TextField('response')
    exp_response = TextField('exp_response', validators=[DataRequired()])
