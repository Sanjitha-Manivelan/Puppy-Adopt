from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField

from wtforms.validators import DataRequired
class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Fill In This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Fill In This Field")])

class RegisterForm(Form):
    username = StringField("Username", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Fill This Field")])
    email = StringField("Email", validators=[validators.Email(message="Enter A Valid Email")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Fill In This Field"),
        validators.EqualTo(fieldname="confirm", message="Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Fill In This Field")])
