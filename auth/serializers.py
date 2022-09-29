from marshmallow import fields, post_load, validates, ValidationError
from marshmallow.validate import Email

from app import ma, bcrypt
from .models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class UserCreateSchema(ma.SQLAlchemyAutoSchema):
    email = fields.Str(required=True, validate=[Email()])
    password = fields.Str(required=True)

    class Meta:
        model = User
        exclude = ("creation_date", "id")

    @validates("email")
    def validate_unique_email(self, value):
        user = User.query.filter_by(email=value).first()
        if user is not None:
            raise ValidationError("A user with this email already exists.")

    @post_load()
    def hash_user_password(self, data, **kwargs):
        data["password"] = bcrypt.generate_password_hash(data.pop("password"))
        return data
