from flask import Flask


def test_app(app):
    assert app is not None
    assert isinstance(app, Flask)
