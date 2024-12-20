from flask import session, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user
from app import db
from .models import User
from .forms import RegisterForm, LoginForm
from . import bp

# Registration route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match!', 'error')
            return render_template('auth/register.html', form=form)

        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken!', 'error')
            return render_template('auth/register.html', form=form)

        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


# Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect them to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Log in successful!', 'success')  # Flash message only after successful login
            return redirect(url_for('main.homepage'))

        else:
            flash('Log in unsuccessful. Invalid username or password', 'error')  # Error if login fails

    return render_template('auth/login.html', form=form)


# Logout route
@bp.route('/logout')
def logout():
    
    session.pop('_flashes', None)
    logout_user()  # Logs the user out
    flash('You have been logged out.', 'info')  # Flash logout message
    return redirect(url_for('auth.login'))  # Redirect to login page after logging out

