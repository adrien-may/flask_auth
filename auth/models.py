import datetime

from app import db, bcrypt


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, index=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.email

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
