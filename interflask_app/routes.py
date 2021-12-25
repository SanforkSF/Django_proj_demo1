from interflask_app import app, db
from flask import render_template, url_for, request, redirect, session, flash
from .forms import *
from interflask_app.models import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
def index():
    questions = Question.query.all()
    user_t = User.query.all()
    return render_template('base.html', user_t=user_t, questions=questions)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html')


@app.errorhandler(403)
def permission_denied(error):
    return render_template('permission_denied403.html')


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


@app.route('/users_view_adm/<username>/delete', methods=['POST', 'GET']) # /admin address change
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
        return redirect(url_for('permission_denied'))


@app.route('/check_init_admin', methods=['POST', 'GET'])
def check_init_admin():
    try:
        user = User.query.filter_by(username='admin').first()
        if user is None:
            admin = User(username='admin', email='admin@admin.dd', first_name='Admin',
                    last_name='Interflask', user_role='Admin')
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
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_user.html', user=user, form=form)


@app.route('/all-questions')
@login_required
def all_questions():
    questions = Question.query.all()
    return render_template('all_questions.html', questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
@login_required
def add_question():
    if current_user.is_authenticated and current_user.user_role != 'Guest':
        form = QuestionForm()
        if form.validate_on_submit():
            question = Question(question_text=form.question_text.data, description=form.description.data,
                                answer=form.answer.data, max_grade=form.max_grade.data)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('all_questions'))
        return render_template('add_question.html', form=form)
    else:
        return render_template('permission_denied403.html')


@app.route('/question/<id>/delete', methods=['POST', 'GET'])
def question_delete(id):
    if current_user.is_authenticated and current_user.user_role != 'Guest':
        try:
            question = Question.query.filter_by(id=id).first_or_404()
            db.session.delete(question)
            db.session.commit()
            flash('Question removed')
            return redirect(url_for('all_questions'))
        except:
            return render_template('permission_denied403.html')
    else:
        return render_template('permission_denied403.html')


@app.route('/all-interviews')
def all_interviews():
    interviews = Interview.query.all()
    return render_template('all_interviews.html', interviews=interviews)


@app.route('/add-interview', methods=["GET", "POST"])
def add_interview():
    if current_user.is_authenticated and current_user.user_role != 'Guest':
        form = InterviewForm().picks()
        if form.validate_on_submit():
            questions_set = []
            users_set = []
            for question_id in form.questions_set.data:
                question = Question.query.filter_by(id=question_id).first()
                questions_set.append(question)
            for user_id in form.users_set.data:
                user = User.query.filter_by(id=user_id).first()
                users_set.append(user)
            interview = Interview(candidate_name=form.candidate_name.data,
                                questions_set=questions_set,
                                users_set=users_set,
                                start_time=form.start_time.data)
            all_objects = [interview]
            for user in users_set:
                for question in questions_set:
                    grade = Grade(
                        question=question,
                        interviewer=user,
                        interview=interview
                    )
                    all_objects.append(grade)
            db.session.add_all(all_objects)
            db.session.commit()
            return redirect(url_for('all_interviews'))
        return render_template('add_interview.html', form=form)
    else:
        return render_template('permission_denied403.html')


@app.route('/all-interviews/<id>/delete', methods=['POST', 'GET'])
@login_required
def interview_delete(id):
    if current_user.is_authenticated and current_user.user_role != 'Guest':
        try:
            interview = Interview.query.filter_by(id=id).first_or_404()
            db.session.delete(interview)
            db.session.commit()
            flash('Interview removed')
            return redirect(url_for('all_interviews'))
        except:
            return render_template('permission_denied403.html')
    else:
        return render_template('permission_denied403.html')


@app.route('/my-interviews')
@login_required
def my_interviews():
    interviews = Interview.query.all()
    list_interview = []
    for interview in interviews:
        if current_user in interview.users_set:
            list_interview.append(interview)
    return render_template('my_interviews.html', list_interview=list_interview, interviews=interviews)


@app.route('/my-interviews/<id>')
def interview_detail(id):
    interview = Interview.query.filter_by(id=id).first_or_404()
    grades = Grade.query.filter_by(interview_id=id)
    return render_template('interview_detail.html', interview=interview, grades=grades)


@app.route('/add-grade', methods=["POST", "GET"])
@login_required
def add_grade():
    form = GradeForm()
    if form.validate_on_submit():
        question = Question.query.filter_by(id=form.questions_set.data).first()
        user = User.query.filter_by(id=form.users_set.data).first()
        interview = Interview.query.filter_by(id=form.interviews.data).first()
        grade = Grade(
            interviewer=user,
            question=question,
            interview=interview,
            grade=1
        )
        db.session.add(grade)
        db.session.commit()
        return redirect('/add-grade')
    return render_template('form.html', form=form)


@app.route('/my-interviews/<id>/rate/<question_id>', methods=["POST", "GET"])
@login_required
def rate_question(id, question_id):
    form = GradeRateForm()
    question = Question.query.filter_by(id=question_id).first_or_404()
    if form.validate_on_submit():
        grade_select = Grade.query.filter_by(question_id=question_id,
                                             interview_id=id,
                                             interviewer_id=current_user.id).first_or_404()
        if 0 < int(form.grade_field.data) <= int(grade_select.question.max_grade):
            grade_select.grade = form.grade_field.data
            db.session.commit()
        else:
            flash("You gave it more points than the question deserves. Try again. ")
        return redirect(f'/my-interviews/{id}')
    return render_template('rate_question.html', form=form, question=question)
