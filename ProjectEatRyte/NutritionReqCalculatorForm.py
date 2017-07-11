from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,DecimalField,IntegerField
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class NutritionReqCalculatorForm(Form):
    Weight = DecimalField('Weight')
    Age = IntegerField('Age' )
    submit = SubmitField('Submit')

