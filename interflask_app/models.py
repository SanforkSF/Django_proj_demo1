from interflask_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from interflask_app import login


class User(UserMixin, db.Model):
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
    def get_selection_list():
        result = []
        for u in User.query.all():
            result.append((f"{u.id}", f"{u.first_name} {u.last_name}"))
        return result


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    description = db.Column(db.String(128))
    answer = db.Column(db.String(64))
    max_grade = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.description}"

    @staticmethod
    def get_selection_list():
        result = []
        for q in Question.query.all():
            result.append((f"{q.id}", f"{q.description}"))
        return result
