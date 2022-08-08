#! /usr/bin/env python
import manager
from bootstrap import application


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(manager.uml_graph)
    app.cli.add_command(manager.db_empty)
    app.cli.add_command(manager.db_create)
    app.cli.add_command(manager.db_init)
    app.cli.add_command(manager.create_admin)
    app.cli.add_command(manager.create_user)
    app.cli.add_command(manager.logs)


with application.app_context():

    from web import views

    application.register_blueprint(views.admin_bp)
    application.register_blueprint(views.user_bp)
    application.register_blueprint(views.stats_bp)

    register_commands(application)


if __name__ == "__main__":
    application.run(host=application.config["HOST"], port=application.config["PORT"])
