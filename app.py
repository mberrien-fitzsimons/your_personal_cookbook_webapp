
import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from models import *
import os
from dotenv import load_dotenv

app = Flask(__name__)
bootstrap = Bootstrap(app)

project_folder = os.path.expanduser('~/coding_projects/python_projects/personal_projects/your_personal_cookbook_api/your_personal_cookbook_webapp')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

app.config['SECRET_KEY']='hard to guess string'
app.config['ENV']='HEROKU_BUILDPACK_GIT_LFS_REPO'
HEROKU_BUILDPACK_GIT_LFS_REPO = os.getenv("HEROKU_BUILDPACK_GIT_LFS_REPO")

class cartForm(FlaskForm):
    meal = StringField('What meal would you like to plan for?', validators=[DataRequired()])
    # dietrest = StringField('Omnivore or vegetarian?', validators=[DataRequired()])
    item1 = StringField('First item', validators=[DataRequired()])
    item2 = StringField('Second item', validators=[DataRequired()])
    item3 = StringField('Third item', validators=[DataRequired()])

    # def validate_dietrest(form, field):
    #     diet_rest = ['omnivore', 'vegetarian']
    #     if field.data.lower() not in diet_rest:
    #         raise ValidationError('Must enter either omnivore or vegetarian')

    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = cartForm()
    if form.validate_on_submit():
        meal = form.meal.data
        # dietary_restrictions = form.dietrest.data
        item1 = form.item1.data
        item2 = form.item2.data
        item3 = form.item3.data

        user_instance = recipeRecommender([item1, item2, item3], meal)
        user_instance.similair_food_items()

        random_recipes, random_links = user_instance.recipe_recommendations()
        return render_template('recommendations.html',
                               recipes=random_recipes,
                               links=random_links)
    return render_template('index.html', form=form)
