#! /usr/bin/env python
from flask import redirect
from flask import url_for
from flask_wtf import FlaskForm
from lib import misc_utils
from web.models import User
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators


class RedirectForm(FlaskForm):
    """
    Secure back redirects with WTForms.
    """

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = misc_utils.get_redirect_target() or ""

    def redirect(self, endpoint="services", **values):
        if misc_utils.is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = misc_utils.get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class SigninForm(RedirectForm):
    """
    Sign in form.
    """

    login = StringField(
        "Login",
        [
            validators.Length(min=3, max=30),
            validators.InputRequired("Please enter your login."),
        ],
    )
    password = PasswordField(
        "Password",
        [
            validators.InputRequired("Please enter your password."),
            validators.Length(min=6, max=100),
        ],
    )
    submit = SubmitField("Log In")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        validated = super().validate()
        user = User.query.filter(User.login == self.login.data).first()
        if not user:
            validated = False
        else:
            if not user.is_active:
                validated = False
            if not user.check_password(self.password.data):
                validated = False
            self.user = user
        if not validated:
            # intentionaly do not explain why it is impossible to login
            self.login.errors.append("Impossible to login.")
        return validated


class UserForm(FlaskForm):
    """
    Create or edit a user (for the administrator).
    """

    login = StringField(
        "Login",
        [
            validators.Length(min=3, max=30),
            validators.InputRequired("Please enter your login."),
        ],
    )
    password = PasswordField("Password")
    is_active = BooleanField("Active", default=True)
    is_admin = BooleanField("Admin", default=False)
    is_api = BooleanField("API", default=False)
    submit = SubmitField("Save")


class ProfileForm(FlaskForm):
    """
    Edit a profile.
    """

    login = StringField(
        "Login",
        [
            validators.Length(min=3, max=30),
            validators.InputRequired("Please enter your login."),
        ],
    )
    password = PasswordField("Password")
    submit = SubmitField("Save")
