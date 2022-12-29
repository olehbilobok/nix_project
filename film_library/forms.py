from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, FileField, \
    validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    # def validate_username(self, username):
    #     user = CustomUser.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Username already exists!')
    #
    # def validate_email(self, email):
    #     user = CustomUser.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateFilmForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=1, max=20)])
    release = DateField('Release', validators=[DataRequired()])
    description = StringField('Description')
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    poster = FileField('Poster', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    director = StringField('Director', validators=[DataRequired()])


class EditFilmForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=1, max=20)])
    release = DateField('Release', validators=[DataRequired()])
    description = StringField('Description')
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    poster = FileField('Poster', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    director = StringField('Director', validators=[DataRequired()])


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])


class SearchForm(FlaskForm):
    name = StringField('Searched', validators=(validators.Optional(),))


class FilterForm(FlaskForm):
    genre = StringField('Genre', validators=(validators.Optional(),))
    release_date_from = DateField('Release_date_from', validators=(validators.Optional(),))
    release_date_to = DateField('Release_date_to', validators=(validators.Optional(),))
    director = StringField('Director', validators=(validators.Optional(),))

