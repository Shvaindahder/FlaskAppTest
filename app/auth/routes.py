from flask import redirect, render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.models import UserAccount
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from werkzeug.urls import url_parse


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password! Try again')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@bp.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserAccount(form.username.data, form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration was fine ^.^')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', title='Registration', form=form)


@bp.route('/logout')
def logot():
    logout_user()
    return redirect(url_for('index'))