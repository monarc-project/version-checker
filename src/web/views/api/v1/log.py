#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import application, manager

from web import models
from web.views.api.v1 import processors
from web.views.api.v1.common import url_prefix


blueprint_log = manager.create_api_blueprint(
    models.Log,
    url_prefix=url_prefix,
    methods=['GET'],
    preprocessors=dict(
            GET=[processors.auth_func],
            GET_MANY=[processors.auth_func]))
