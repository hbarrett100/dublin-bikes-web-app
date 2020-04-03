from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dublinbikes.users import check_email

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if check_email(email.data):
            raise ValidationError("This email is already in use.")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateEmail(FlaskForm):
    email = StringField('New Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Please enter password', validators=[DataRequired()])
    submit = SubmitField('Update Email')

    def validate_email(self, email):
        if check_email(email.data):
            raise ValidationError("This email is already in use.")

class UpdatePassword(FlaskForm):
    old_password = PasswordField('Please enter current password',
                             validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

