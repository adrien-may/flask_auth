from .models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password.encode("utf-8")):
        return user
