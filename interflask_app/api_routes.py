from flask import jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_restful import Resource

from interflask_app import db
from interflask_app.forms import LoginForm
from interflask_app.models import User, Question, Interview, Grade
from interflask_app.schema import *


class MainResource(Resource):

    def get_model_query(self):
        pass

    def edit_object(self):
        pass

    def create_object(self):
        pass

    def get_schema(self):
        pass


    @login_required
    def get(self):
        schema = self.get_schema()
        model_schema = schema(many=True)
        if isinstance(model_schema, UserSchema) and current_user.user_role != 'Admin':
            return {"error": "you are not admin"}
        args = request.args
        model_objects = self.get_model_query(args=args).all()
        output = model_schema.dump(model_objects)
        return jsonify(output)

    @login_required
    def delete(self):
        if isinstance(self.get_schema()(), UserSchema) and current_user.user_role != 'Admin':
            return {"error": "you are not admin"}
        args = request.args
        model_object = self.get_model_query(args).first()
        db.session.delete(model_object)
        db.session.commit()
        return {'success': 'True'}

    @login_required
    def patch(self):
        object_schema = self.get_schema()()
        if isinstance(object_schema, UserSchema) and current_user.user_role != 'Admin':
            return {"error": "you are not admin"}
        args = request.args
        model_object = self.get_model_query(args).first()
        form = request.form
        model_object = self.edit_object(model_object, form)
        output = object_schema.dump(model_object)
        db.session.commit()
        return jsonify(output)

    @login_required
    def post(self):
        if isinstance(self.get_schema()(), UserSchema) and current_user.user_role != 'Admin':
            return {"error": "you are not admin"}
        form = request.form
        model_object = self.create_object(form=form)
        db.session.add(model_object)
        db.session.commit()
        return {'result': 'done'}


class UserApi(MainResource):

    def get_model_query(self, args):
        users = User.query
        if args.get("id"):
            users = users.filter_by(id=args.get('id'))
        if args.get("username"):
            users = users.filter_by(username=args.get('username'))
        if args.get('email'):
            users = users.filter_by(email=args.get('email'))
        if args.get("first_name"):
            users = users.filter_by(first_name=args.get('first_name'))
        if args.get("last_name"):
            users = users.filter_by(last_name=args.get("last_name"))
        return users

    def edit_object(self, user, form):
        if form.get("username"):
            user.username = form.get('username')
        if form.get('email'):
            user.email = form.get('email')
        if form.get("first_name"):
            user.first_name = form.get('first_name')
        if form.get("last_name"):
            user.last_name = form.get('last_name')
        if form.get("user_role"):
            if form.get("user_role") == "True":
                user.is_admin = True
            elif form.get("is_admin") == "False":
                user.is_admin = False
        return user

    def create_object(self, form):
        user = User()
        if not form.get("username") or not form.get("password"):
            raise Exception("no username or password")
        user = self.edit_object(user, form)
        return user

    def get_schema(self):
        return UserSchema


class QuestionApi(MainResource):

    def get_model_query(self, args):
        question = Question.query
        if args.get("id"):
            question = question.filter_by(id=args.get('id'))
        if args.get("question_text"):
            question = question.filter_by(question_text=args.get('question_text'))
        if args.get('answer'):
            question = question.filter_by(answer=args.get('answer'))
        if args.get("max_grade"):
            question = question.filter_by(max_grade=args.get('max_grade'))
        if args.get("description"):
            question = question.filter_by(description=args.get("description"))
        return question

    def edit_object(self, question, form):
        if form.get("question_text"):
            question.question_text = form.get('question_text')
        if form.get('answer'):
            question.answer = form.get('answer')
        if form.get("max_grade"):
            question.max_grade = form.get('max_grade')
        if form.get("description"):
            question.description = form.get('description')
        return question

    def get_schema(self):
        return QuestionSchema

    def create_object(self, form):
        question = Question()
        if not form.get('candidate_name'):
            raise Exception("no candidate name")
        question = self.edit_object(question, form)
        return question
