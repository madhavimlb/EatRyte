from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class SignupForm(Form):
    firstName=StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired()])
    password = PasswordField('New Password')
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

