from bootstrap import db
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from web.forms import ProfileForm
from web.models import User
from werkzeug.security import generate_password_hash


user_bp = Blueprint("user_bp", __name__, url_prefix="/user")


@user_bp.route("/profile", methods=["GET"])
@login_required
def form():
    user = User.query.filter(User.id == current_user.id).first()
    form = ProfileForm(obj=user)
    form.populate_obj(current_user)
    action = "Edit user"
    head_titles = [action]
    head_titles.append(user.login)
    return render_template(
        "edit_user.html", action=action, head_titles=head_titles, form=form, user=user
    )


@user_bp.route("/profile", methods=["POST"])
@login_required
def process_form():
    form = ProfileForm()

    if not form.validate():
        return render_template("edit_user.html", form=form)

    user = User.query.filter(User.id == current_user.id).first()
    form.populate_obj(user)
    if form.password.data:
        user.pwdhash = generate_password_hash(form.password.data)
    db.session.commit()
    flash(f"User {form.login.data} successfully updated.", "success")
    return redirect(url_for("admin_bp.form_user", user_id=user.id))
