from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, Optional
import datetime

class LoginForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired()])
	birthday = DateField('birthday (YYYY/MM/DD)', format='%Y%m%d')
	gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Not To Tell')])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	address = StringField("Address")
	phone_number = StringField("Phone Number")
	submit = SubmitField('Sign Up')

class ProductForm(FlaskForm):
	quantity = SelectField('Quantity',
						   choices=[('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5')])
	submit = SubmitField('ADD TO CART')

class ProfileForm(FlaskForm):
	comment = StringField('Leave comment messages here zph!', validators=[DataRequired()])
	rating = SelectField('Rate here!',
						   choices=[('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5')])
	submit = SubmitField('Submit')
	"""def validate_username(self, username):
		user = find_first_query(engine, username.data, "username", "users")
	"""