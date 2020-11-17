from app import app, db
from app.models import User, Feedback
from flask import render_template, redirect, flash, url_for, request
from app.forms import FeedbackForm, AdminForm
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()
    if form.validate_on_submit():
        f = Feedback(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            feedback=form.feedback.data)
        db.session.add(f)
        db.session.commit()
        flash(f'Thanks for the feedback {form.first_name.data}!')
        redirect(url_for('index'))
    return render_template('index.html', title='Give Feedback', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('admin'))
    form = AdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(admin)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin', next=request.url))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    feedback = Feedback.query.all()
    return render_template('admin.html', title='Admin Panel', feedback=feedback)