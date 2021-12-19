from interflask_app import app, db
from flask import render_template, url_for, request, redirect, session, flash
from .forms import LoginForm, RegisterForm, RoleForm
from interflask_app.models import User, Question
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
def index():
    user_t = User.query.all()
    return render_template('base.html', user_t=user_t)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("user has been created")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/users_view_adm')
def users_view_adm():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('users_view_adm.html', users=users)


@app.route('/users_view_adm/<username>/set_role', methods=['POST', 'GET'])
def user_set_role(username):
    if current_user.is_authenticated and current_user.user_role == 'Admin':
        user = User.query.filter_by(username=username).first_or_404()
        form = RoleForm()
        if request.method=="POST":
            if form.cancel.data:
                return redirect(url_for('users_view_adm'))
            user.user_role = form.role.data
            db.session.commit()
            return redirect(url_for('users_view_adm'))
        return render_template('set_user_role.html', form=form, user=user)
    else:
        return redirect(url_for('index'))


@app.route('/users_view_adm/<username>/delete', methods=['POST', 'GET'])
def user_delete(username):
    if current_user.is_authenticated and current_user.user_role == 'Admin':
        try:
            user = User.query.filter_by(username=username).first_or_404()
            db.session.delete(user)
            db.session.commit()
            flash('User removed')
            return redirect(url_for('users_view_adm'))
        except:
            return 'Error'
    else:
        return redirect(url_for('page_not_found'))


@app.route('/check_init_admin', methods=['POST', 'GET'])
def check_init_admin():
    try:
        user = User.query.filter_by(username='admin').first()
        if user is None:
            admin = User(username='admin', email='admin@admin.dd', first_name='First',
                    last_name='User', user_role='Admin')
            admin.set_password('interflask')
            db.session.add(admin)
            db.session.commit()
            flash("admin has been created")
            return redirect(url_for('login'))
        elif user.user_role != 'Admin':
            user.user_role = 'Admin'
            db.session.commit()
            flash("admin rights returned")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    except:
        return 'Error'


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = RegisterForm()
    if request.method == 'POST':
        if form.first_name.data:
            current_user.first_name = form.first_name.data
        if form.last_name.data:
            current_user.last_name = form.last_name.data
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        if form.cancel.data:
            return redirect(url_for('index'))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_user.html', user=user, form=form)
