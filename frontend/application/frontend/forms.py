# application/frontend/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import (StringField, PasswordField,
                     SubmitField, SelectField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import (InputRequired, Email, EqualTo,
                                ValidationError, Length, Optional)
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    '''Create post form'''
    title = StringField('Title', validators=[InputRequired(), Length(max=40)])
    category = SelectField('Category', choices=[
                            ('activities', 'Activities'),
                            ('courses&modules', 'Courses&Modules'),
                            ('societies','Societies'),
                            ('student_union','Student Union'),
                            ('accommodation','Accommodation'),
                            ('transportation','Transportation'),
                            ('lost&found', 'Lost&Found'),
                            ('sale&rental', 'Sale&Rental'),
                            ('other', 'Other'),
                            ])
    content = CKEditorField('Content', validators=[
                            InputRequired(), Length(min=20, max=300)])
    image = FileField('Upload an image')
    submit = SubmitField('CREATE POST', validators=[
                         FileAllowed(['jpg', 'jpeg', 'png'])])

class CommentForm(FlaskForm):
    '''Comment post form'''
    content = CKEditorField('Comment', validators=[InputRequired(), Length(max=120)])
    submit = SubmitField('SUBMIT')

class SearchForm(FlaskForm):
    keywords = StringField('Type keywords', validators=[InputRequired()])
    submit = SubmitField('Search')

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    email = StringField('Email address', validators=[InputRequired(), Email()])
    phone_number = StringField('Phone Number')
    uni_number = StringField('University Number')
    user_role = SelectField('Role', choices=[
                            ('staff', 'Staff'),
                            ('academic_staff', 'Academic Staff'),
                            ('student', 'Student'),
                            ('graduate', 'Graduate')
                            ])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Re-Enter Password*', validators=[
                    InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    '''Login form for registered users'''
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('LOGIN')

class AccountUpdateForm(FlaskForm):
    image = FileField('Upload an image')
    first_name = StringField('First name')
    last_name = StringField('Last name')
    phone_number = StringField('Phone Number')
    user_role = SelectField('Role', choices=[
                            ('graduate', 'Graduate')
                            ],validators = [Optional()])
    submit = SubmitField('Update',validators=[
                         FileAllowed(['jpg', 'jpeg', 'png'])])