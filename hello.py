#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)


class NameForm(FlaskForm):
    username = StringField('What is your username?', validators=[Required()])
    password = PasswordField('What is your password?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_username = session.get('username')
        old_password = session.get('password')
        if old_username is not None and old_username != form.username.data:
            flash('Looks like you have change your username!')
        elif old_password is not None and old_password != form.password.data:
            flash('Looks like you have change your password!')
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('username'), pwd=session.get('password'))


if __name__ == '__main__':
    app.run(port=5555, debug=True)
