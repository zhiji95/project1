from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField,HiddenField, TextAreaField, IntegerField
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
	quantity = SelectField('Quantity',coerce=int,
						   choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
	submit = SubmitField('ADD TO CART')

class ProfileForm(FlaskForm):
	oid = StringField()
	pid = StringField()
	comment = StringField('Leave comment messages here zph!', validators=[DataRequired()])
	rating = SelectField('Rate here!',coerce=int,
						   choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
	submit = SubmitField('Submit')

class CartForm(FlaskForm):
	uid = StringField()
	pid = StringField()
	submit = SubmitField('Remove')

class CheckoutForm(FlaskForm):
	hidden = HiddenField()
	submit = SubmitField('Checkout')
	"""def validate_username(self, username):
		user = find_first_query(engine, username.data, "username", "users")
	"""

class PaymentForm(FlaskForm):
	payname = StringField('Name', validators=[DataRequired()])
	payphone = StringField('Phone Number', validators=[DataRequired()])
	paybank = SelectField('Bank', choices=[('Chase', 'Chase'), ('BOA', 'Bank of America'), ('Citi', 'Citibank')])
	account = StringField('Account Number', validators=[DataRequired()])
	billaddress = StringField('Billing Address', validators=[DataRequired()])
	submit = SubmitField('Add New Payment Method')
