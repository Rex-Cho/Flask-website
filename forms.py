from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import TextArea
from wtforms import DecimalField


class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password_check', message='Password Must Match!')])
    password_check = PasswordField("Password check", validators=[DataRequired()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    submit = SubmitField("Submit")

class BusinessSignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password_check', message='Password Must Match!')])
    password_check = PasswordField("Password check", validators=[DataRequired()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SignInForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired()])
    password = PasswordField("Your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    money = IntegerField("Money", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    detail = StringField("Detail", validators=[DataRequired()], widget=TextArea())
    #image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), FileRequired()])
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField("Submit")

class ChatForm(FlaskForm):
    message = StringField("Message:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CreateCouponForm(FlaskForm):
    discount = DecimalField("Discount", validators=[DataRequired()], places=2)
    expire_date = DateField("Expire_Date", validators=[DataRequired()])
    submit = SubmitField("Submit")