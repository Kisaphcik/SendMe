from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.user import User
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Login successful')
            return redirect(url_for('file.upload'))
        flash('Invalid credentials')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    flash('Logged out')
    return redirect(url_for('auth.login'))