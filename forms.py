from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import input_required, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    user_id = StringField('User Id:', validators=[input_required()])
    password = PasswordField('Password:', validators=[input_required()])
    password2 = PasswordField('Confirm password:', validators=[
                              input_required(), EqualTo('password')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_id = StringField('User Id:', validators=[input_required()])
    password = PasswordField('Password:', validators=[input_required()])
    submit = SubmitField('Submit')


class InsertForm(FlaskForm):
    name = StringField("New activity:")
    score = StringField("Score:")
    description = StringField("Description:")
    comment = StringField("Your Comments:")
    submit = SubmitField()


class EncryptForm(FlaskForm):
    encrypt = SubmitField('Encrypt')


# class CheckoutForm(FlaskForm):
#     checkout = SubmitField('Confirm')


# class GreetingForm(FlaskForm):
#     name = StringField("Your name")
#     submit = SubmitField()

# class WeatherForm(FlaskForm):
#     cityName = StringField('City', validators=[input_required()])
#     submit = SubmitField()
#     weatherData = StringField('Weather:')
