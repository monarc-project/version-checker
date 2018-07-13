import logging

from datetime import datetime
from flask import render_template, session, url_for, redirect, current_app
from flask_login import (LoginManager, logout_user, login_required,
                        current_user, login_user)
from flask_principal import (Principal, AnonymousIdentity, UserNeed,
                             identity_changed, identity_loaded,
                             session_identity_loader, Identity,
                             Permission, RoleNeed)

from bootstrap import db, application, RELEASES
from web.models import User
from web.forms import SigninForm

admin_role = RoleNeed('admin')
api_role = RoleNeed('api')

admin_permission = Permission(admin_role)
api_permission = Permission(api_role)

Principal(current_app)
# Create a permission with a single Need, in this case a RoleNeed.

login_manager = LoginManager()
login_manager.init_app(current_app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

logger = logging.getLogger(__name__)


@identity_loaded.connect_via(current_app._get_current_object())
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        if current_user.is_admin:
            identity.provides.add(admin_role)
        if current_user.is_api:
            identity.provides.add(api_role)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id, User.is_active == True).first()


@current_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@current_app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.list_logs'))
    form = SigninForm()
    if form.validate_on_submit():
        login_user(form.user)
        identity_changed.send(current_app, identity=Identity(form.user.id))
        session_identity_loader()
        return form.redirect()
    return render_template('index.html', form=form,
                            releases=RELEASES)


@current_app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app, identity=AnonymousIdentity())
    session_identity_loader()

    return redirect(url_for('login'))
