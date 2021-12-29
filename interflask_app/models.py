from interflask_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from interflask_app import login
from flask import url_for

interview_question = db.Table('interview_question',
                              db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
                              db.Column('interview_id', db.Integer, db.ForeignKey('interviews.id'), primary_key=True)
                              )

interview_user = db.Table('interview_user',
                          db.Column('users_id', db.ForeignKey('users.id'), primary_key=True),
                          db.Column('interview_id', db.ForeignKey('interviews.id'), primary_key=True)
                          )


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(255))
    user_role = db.Column(db.String(64), default='Guest')

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def delete_user(self, username):
        user = User.query.get(username=username)
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_selector_list():
        result = []
        for u in User.query.all():
            result.append((f"{u.id}", f"{u.first_name} {u.last_name}"))
        return result


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    description = db.Column(db.String(128))
    answer = db.Column(db.String(255), nullable=True)
    max_grade = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.description}"

    @staticmethod
    def get_selector_list():
        questions_list = []
        for q in Question.query.all():
            questions_list.append((f"{q.id}", f"{q.description}"))
        return questions_list


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String)
    questions_set = db.relationship('Question', secondary=interview_question, lazy='subquery',
                                    backref=db.backref('interviews', lazy=True))
    users_set = db.relationship('User', secondary=interview_user, lazy='subquery',
                                backref=db.backref('interviews', lazy=True))
    start_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"{self.candidate_name}"

    @staticmethod
    def get_selector_list():
        interviews_list = []
        for i in Interview.query.all():
            interviews_list.append((f"{i.id}", f"{i.candidate_name}"))
        return interviews_list

    def get_max_points(self):
        max_points = 0
        for q in self.questions_set:
            max_points += q.max_grade
        return max_points

    def get_count_interviewers(self):
        count_interviewers = 0
        for i in self.users_set:
            count_interviewers += 1
        return count_interviewers

    def get_count_questions(self):
        count_questions = 0
        for q in self.questions_set:
            count_questions += 1
        return count_questions

    def get_final_grade(self):
        max_points = self.get_max_points()
        count_users = self.get_count_interviewers()
        count_questions = self.get_count_questions()
        user_points = 0
        count_votes = 0
        check_full = False

        for i in Grade.query.filter_by(interview_id=self.id):
            if i.grade:
                user_points += i.grade
                count_votes += 1
        if count_votes == count_users * count_questions:
            check_full = True

        if check_full:
            result = (user_points / count_users) / max_points * 100
            return round(result, 2)


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question = db.relationship("Question", backref="grades", cascade="all,delete")
    interviewer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    interviewer = db.relationship("User", backref="grades", cascade="all,delete")
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id', ondelete='CASCADE'))
    interview = db.relationship("Interview", backref="grades", cascade="all,delete")
    grade = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"{self.interviewer} gives {self.interview} {self.grade} for question '{self.question}'"
