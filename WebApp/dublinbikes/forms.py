from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dublinbikes.users import check_email


# ==== Register ====

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


# ==== Login ====

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me (uses cookies)')
    submit = SubmitField('Login')


# ==== Account ====

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


class SendConfirmEmail(FlaskForm):
    submit = SubmitField('Send Confimation Email')


class DeleteAccount(FlaskForm):
    password = PasswordField('Please enter password',
                             validators=[DataRequired()])
    submit = SubmitField('Delete Account')
    confirm = BooleanField(
        'Tick to confirm that you wish to delete your account. Once deleted, you will not be able to recover this account.',
         validators=[DataRequired(), ])



# ==== Password Reset ====

class ForgotPassword(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if not check_email(email.data):
            raise ValidationError("Email address not found.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
