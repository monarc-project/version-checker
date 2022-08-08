#! /usr/bin/env python
# required imports and code exection for basic functionning
import errno
import logging
import os
from contextlib import contextmanager

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

try:
    from data.software import RELEASES, CVE
except Exception:
    # For examples, see in src/data/software.py.example
    RELEASES = {"MONARC": {"stable": "2.12.2"}}
    CVE = {}


@contextmanager
def open_r_error(filename, mode="r"):
    try:
        f = open(filename, mode)
    except OSError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()


def set_logging(
    log_path=None,
    log_level=logging.INFO,
    modules=(),
    log_format="%(asctime)s %(levelname)s %(message)s",
):
    if not modules:
        modules = (
            "bootstrap",
            "runserver",
            "web",
        )
    if log_path:
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        if not os.path.exists(log_path):
            open(log_path, "w").close()
        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler()
    formater = logging.Formatter(log_format)
    handler.setFormatter(formater)
    for logger_name in modules:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        for handler in logger.handlers:
            handler.setLevel(log_level)
        logger.setLevel(log_level)


def create_directory(directory):
    """Creates the necessary directories (public uploads, etc.)."""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


# Create Flask application
application = Flask("web", instance_relative_config=True)
try:
    application.config.from_pyfile("production.cfg", silent=False)
except Exception:
    application.config.from_pyfile("development.cfg", silent=False)

db = SQLAlchemy(application)
migrate = Migrate(application, db)


# Jinja filters
def datetimeformat(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)


# def instance_domain_name(*args):
#     return request.url_root.replace('http', 'https').strip("/")

application.jinja_env.filters["datetimeformat"] = datetimeformat
# application.jinja_env.filters['instance_domain_name'] = instance_domain_name


# set_logging(application.config['LOG_PATH'])

# create_directory(application.config['GENERATED_SVG_FOLDER'])

CIPHER = None
with open_r_error(application.config["RSA_PRIVATE_KEY"], "rb") as (priv_key, err):
    if err:
        CIPHER = None
    else:
        rsa_private_key = priv_key.read()
        private_key = RSA.import_key(rsa_private_key)
        CIPHER = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
