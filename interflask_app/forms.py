from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField,\
    FloatField, SelectMultipleField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from interflask_app.models import *


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


class QuestionForm(FlaskForm):

    question_text = TextAreaField("Question", validators=[DataRequired()])
    description = StringField("Short description", validators=[DataRequired()])
    answer = TextAreaField("Answer", validators=[DataRequired()])
    max_grade = IntegerField("Maximal Grade", validators=[DataRequired()], default=10)
    submit = SubmitField("Add")


class InterviewForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    candidate_name = StringField('Candidate Name', validators=[DataRequired()])
    questions_set = SelectMultipleField("Choose Questions", choices=Question.get_selector_list())
    users_set = SelectMultipleField("Choose Interviewers", choices=User.get_selector_list())
    start_time = DateTimeField("Choose Start Time (Y-m-d H:M)", format="%Y-%m-%d %H:%M")
    submit = SubmitField("Add")

    @classmethod
    def picks(cls):
        form = cls()
        form.questions_set.choices = Question.get_selector_list()
        form.users_set.choices = User.get_selector_list()
        return form


class GradeForm(FlaskForm):
    questions_set = SelectField("Choose Questions", choices=Question.get_selector_list())
    users_set = SelectField("Choose Interviewers", choices=User.get_selector_list())
    interviews = SelectField("Choose Interview", choices=Interview.get_selector_list())
    submit = SubmitField('add')

    @classmethod
    def picks(cls):
        form = cls()
        form.users_set.choices = User.get_selector_list()
        form.questions_set.choices = Question.get_selector_list()
        form.interviews.choices = Interview.get_selector_list()
        return form


class GradeRateForm(FlaskForm):
    # grade_field = IntegerField("Enter Grade")
    rate_picks = [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    ]
    grade_field = SelectField("Choose Questions", choices=rate_picks)