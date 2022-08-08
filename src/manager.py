#! /usr/bin/env python
import logging

import click
import scripts
import web.models
from bootstrap import application
from bootstrap import db


logger = logging.getLogger("commands")


@application.cli.command("uml_graph")
def uml_graph():
    "UML graph from the models."
    with application.app_context():
        web.models.uml_graph(db)


@application.cli.command("db_empty")
def db_empty():
    "Will drop every datas stocked in db."
    with application.app_context():
        web.models.db_empty(db)


@application.cli.command("db_create")
def db_create():
    "Will create the database."
    print("created")
    with application.app_context():
        web.models.db_create(
            db,
            application.config["DB_CONFIG_DICT"],
            application.config["DATABASE_NAME"],
        )


@application.cli.command("db_init")
def db_init():
    "Will create the database from conf parameters."
    with application.app_context():
        web.models.db_init(db)


@application.cli.command("create_user")
@click.option("--login", default="admin", help="Login")
@click.option("--password", default="password", help="Password")
def create_user(login, password):
    "Initializes a user"
    print(f"Creation of the user {login}…")
    with application.app_context():
        scripts.create_user(login, password, False)


@application.cli.command("create_admin")
@click.option("--login", default="admin", help="Login")
@click.option("--password", default="password", help="Password")
def create_admin(login, password):
    "Initializes an admin user"
    print(f"Creation of the admin user {login}…")
    with application.app_context():
        scripts.create_user(login, password, True)


@application.cli.command("logs")
@click.option("--software", default="MONARC", help="Name of a software.")
def logs(software):
    result = web.models.Log.query.filter(web.models.Log.software == software).all()
    print(*result, sep="\n")
