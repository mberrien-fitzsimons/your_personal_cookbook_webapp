
import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

class cartForm(FlaskForm):
    meal = StringField('What meal would you like to plan for?', validators=[DataRequired()])
    dietrest = (StringField('Omnivore or vegetarian', validators=[DataRequired()]))

    def validate_dietrest(form, field):
        diet_rest = ['omnivore', 'vegetarian']
        if field.data.lower() not in diet_rest:
            raise ValidationError('Must enter either omnivore or vegetarian')

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
        session['meal'] = form.meal.data
        session['dietary_restrictions'] = form.dietrest.data
        return redirect(url_for('index'))
    return render_template('index.html',
                            form=form, meal=session.get('meal'),
                            dietary_restrictions=session.get('dietary_restrictions'))
