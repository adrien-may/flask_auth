from .factories import UserFactory


def test_user_repr(db_session):
    user = UserFactory()
    db_session.commit()
    assert repr(user) == user.email


def test_generate_hash(db_session):
    user = UserFactory()
    previous_password = user.password
    db_session.commit()
    user.hash_password("foo")
    new_password = user.password

    assert "foo" != new_password != previous_password
