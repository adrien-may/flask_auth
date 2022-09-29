import factory

from app import db, bcrypt
from ..models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    email = factory.Faker("email")

    @factory.lazy_attribute
    def password(self):
        username = self.email.split("@")[0]
        return bcrypt.generate_password_hash(username)

    class Meta:
        model = User
        sqlalchemy_session = db.session
