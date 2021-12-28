from flask import jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_restful import Resource

from interflask_app import db, bp
from interflask_app.forms import LoginForm
from interflask_app.models import User, Question, Interview, Grade
from interflask_app.schema import *


# class MainResource(Resource):
#
#     def get_model_query(self):
#         pass
#
#     def edit_object(self):
#         pass
#
#     def create_object(self):
#         pass
#
#     def get_schema(self):
#         pass
#
#     @login_required
#     def get(self):
#         schema = self.get_schema()
#         model_schema = schema(many=True)
#         if isinstance(model_schema, UserSchema) and not current_user.is_admin:
#             return {"error": "you are not admin"}
#         args = request.args
#         model_objects = self.get_model_query(args=args).all()
#         output = model_schema.dump(model_objects)
#         return jsonify(output)


# class UserAPI(MainResource):
#
#     @staticmethod
#     @bp.route('/users/<username>', methods=['GET'])
#     def get_user(username):
#         return jsonify(User.query.get_or_404(username=username).to_dict())