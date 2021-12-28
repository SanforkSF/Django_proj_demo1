# from marshmallow import fields, validate
# from interflask_app import db, ma
# from interflask_app.models import *
#
#
# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         exclude = ['password_hash']
#
#         id = ma.auto_field()
#         username = fields.Str(validate=[validate.Length(64)], required=True)
#         email = fields.Str(required=True)
#         first_name = fields.Str(validate=[validate.Length(64)], required=True)
#         last_name = fields.Str(validate=[validate.Length(64)], required=True)
#         password_hash = fields.Str(validate=[validate.Length(255)], required=True)
#         user_role = fields.Str(validate=[validate.Length(64)], required=True)
#
#
# class QuestionSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Question
#
#     id = ma.auto_field()
#     question_text = fields.Str(required=True)
#     description = fields.Str(required=True, validate=validate.Length(128))
#     answer = fields.Str(required=True, validate=validate.Length(64))
#     max_grade = fields.Int(required=True)
#
#
# class InterviewSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Interview
#         sqla_session = db.session
#
#     id = ma.auto_field()
#     candidate_name = fields.Str(required=True, validate=[validate.Length(64)])
#     questions_set = fields.Nested("QuestionSchema", default=[], many=True, required=True)
#     users_set = fields.Nested("UserSchema", default=[], many=True, required=True)
#     start_time = fields.DateTime(format="%Y-%m-%d %H:%M")
#
#
# class GradeSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Grade
#
#     id = ma.auto_field()
#     question_id = fields.Int(required=True)
#     question = fields.Nested("QuestionSchema", default=[], required=True)
#     interviewer_id = fields.Int(required=True)
#     interviewer = fields.Nested("UserSchema", default=[], required=True)
#     interview_id = fields.Int(required=True)
#     interview = fields.Nested("InterviewSchema", default=[], required=True)
#     grade = fields.Int(nullable=True)