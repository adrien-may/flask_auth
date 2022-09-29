from auth.models import User
from auth.services import authenticate
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from app import db
from .serializers import UserCreateSchema, UserSchema

user_blueprint = Blueprint(
    "auth", "auth", url_prefix="/auth", description="Authentication"
)


@user_blueprint.route("/protected")
@jwt_required()
def protected_view():
    return {"details": f"Hello {get_jwt_identity()}"}

@user_blueprint.route("/login", methods=['POST'])
def login():

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    auth = authenticate(username, password)
    if (not auth):
        abort(403, message="Invalid username or password")

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@user_blueprint.route("/users")
class AuthViews(MethodView):
    @user_blueprint.arguments(UserCreateSchema)
    @user_blueprint.response(201, UserSchema(only=["email", "creation_date"]))
    def post(self, new_data):
        """Creates a new user"""
        user = User(**new_data)
        db.session.add(user)
        db.session.commit()
        return new_data
