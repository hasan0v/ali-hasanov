# filepath: c:\Users\alien\Desktop\Test Projects\Port-1\app\auth\routes.py
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from ..forms import LoginForm, RegistrationForm
from peewee import DoesNotExist
from werkzeug.urls import url_parse

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.home')
                return redirect(next_page)
        except DoesNotExist:
            pass
        flash('Invalid email or password.')
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.password = form.password.data
        user.save()
        flash('Your registration was successful! You can now log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)
