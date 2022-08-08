#! /usr/bin/python
from bootstrap import db
from web.models import User
from werkzeug.security import generate_password_hash


def create_user(login, password, is_admin):
    user = User(
        login=login,
        pwdhash=generate_password_hash(password),
        is_active=True,
        is_admin=is_admin,
    )
    db.session.add(user)
    db.session.commit()
