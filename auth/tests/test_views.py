import json

from ..models import User
from .factories import UserFactory


def test_users_create(app, client, db_session):
    email = "bli@blo.fr"
    User.query.filter_by(email=email).delete()
    db_session.commit()

    response = client.post(
        "/auth/users",
        data=json.dumps({"email": email, "password": "password"}),
        content_type="application/json",
    )
    assert response.status_code == 201, response.json

    response = client.post(
        "/auth/users",
        data=json.dumps({"email": email, "password": "password"}),
        content_type="application/json",
    )
    assert response.status_code == 422


def test_get_protected(app, client, db_session):
    user = UserFactory()
    db_session.commit()

    token_request = client.post(
        "/auth/login",
        data=json.dumps({"username": user.email, "password": user.email.split("@")[0]}),
        content_type="application/json",
    )
    assert token_request.status_code == 200
    token = token_request.json["access_token"]

    response = client.get("auth/protected", headers={"Authorization": f"Bearer {token}"})
    assert 'Hello' in response.json["details"]

def test_get_protected_wrong_user_password(app, client, db_session):
    user = UserFactory()
    db_session.commit()

    token_request = client.post(
        "/auth/login",
        data=json.dumps({"username": user.email, "password": "wrong"}),
        content_type="application/json",
    )
    assert token_request.status_code == 403


# def test_tasks_create(app, client, db_session):
#     title = "my_test"
#     # Ensure no task persist with this title
#     Task.query.filter_by(title=title).delete()
#     data = json.dumps({"title": "my_test"})
#     response = client.post("/tasks/", data=data, content_type="application/json")
#     assert response.status_code == 201

#     response = client.post("/tasks/", data=data, content_type="application/json")
#     assert response.status_code == 400


# def test_tasks_get_one(app, client, db_session):
#     task = TaskFactory()
#     db_session.commit()
#     task = Task.query.filter_by(title=task.title).first()
#     response = client.get(f"/tasks/{task.id}")
#     assert response.status_code == 200


# def test_tasks_update_one(app, client, db_session):
#     new_title = "new_title"
#     # Ensure no task persist with this title
#     Task.query.filter_by(title=new_title).delete()

#     task = TaskFactory()
#     db_session.commit()
#     task = Task.query.filter_by(title=task.title).first()
#     response = client.put(f"/tasks/{task.id}", data=json.dumps({"title": new_title}))
#     assert response.status_code == 200

#     Task.query.filter_by(title="already_existing").delete()
#     old_task = TaskFactory(title="already_existing")
#     response = client.put(
#         f"/tasks/{task.id}", data=json.dumps({"title": "already_existing"})
#     )
#     assert response.status_code == 400


# def test_tasks_delete_one(app, client, db_session):
#     task = TaskFactory()
#     db_session.commit()

#     task = Task.query.filter_by(title=task.title).first()
#     response = client.delete(f"/tasks/{task.id}")
#     assert response.status_code == 204
