from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from interflask_app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    role = StringField("Role", default="Guest")
    submit = SubmitField("Submit")
    cancel = SubmitField("Cancel")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RoleForm(FlaskForm):
    role = SelectField('Role', choices=[('Guest', 'Guest'), ('Admin', 'Admin'), ('HR', 'HR'), ('Moderator', 'Moderator'),
                                        ('Python Expert', 'Python Expert'), ('DevOps Expert', 'DevOps Expert')])
    submit = SubmitField("Save")
    cancel = SubmitField("Cancel")

