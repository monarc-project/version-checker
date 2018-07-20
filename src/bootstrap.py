#! /usr/bin/env python
# -*- coding: utf-8 -

# required imports and code exection for basic functionning

import os
import errno
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

try:
    from data.software import RELEASES, CVE
except:
    # For examples, see in src/data/software.py.example
    RELEASES = {'MONARC':
                    {
                        'stable': '2.5.0'
                    }
    }
    CVE = {}


def set_logging(log_path=None, log_level=logging.INFO, modules=(),
                log_format='%(asctime)s %(levelname)s %(message)s'):
    if not modules:
        modules = ('bootstrap', 'runserver', 'web',)
    if log_path:
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        if not os.path.exists(log_path):
            open(log_path, 'w').close()
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
application = Flask('web', instance_relative_config=True)
try:
    application.config.from_pyfile('production.cfg', silent=False)
except:
    application.config.from_pyfile('development.cfg', silent=False)

db = SQLAlchemy(application)


# Jinja filters
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)
# def instance_domain_name(*args):
#     return request.url_root.replace('http', 'https').strip("/")

application.jinja_env.filters['datetimeformat'] = datetimeformat
# application.jinja_env.filters['instance_domain_name'] = instance_domain_name


# set_logging(application.config['LOG_PATH'])

# create_directory(application.config['GENERATED_SVG_FOLDER'])

CIPHER = None
with open(application.config['RSA_PRIVATE_KEY'], 'rb') as priv_key:
    rsa_private_key = priv_key.read()
    private_key = RSA.import_key(rsa_private_key)
    CIPHER = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)


def populate_g():
    from flask import g
    g.db = db
    g.app = application
