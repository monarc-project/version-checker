
import logging
from flask import Blueprint, current_app, render_template, flash, redirect, \
                  url_for

from bootstrap import db
from web.views.common import admin_permission

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')
