import os
import logging
from flask import (render_template, url_for, redirect, current_app, flash,
                  send_from_directory, request, jsonify)
from flask_login import login_required

from bootstrap import application

logger = logging.getLogger(__name__)


@current_app.errorhandler(401)
def authentication_required(error):
    flash(gettext('Authentication required.'), 'info')
    return redirect(url_for('login'))


@current_app.errorhandler(403)
def authentication_failed(error):
    flash(gettext('Forbidden.'), 'danger')
    return redirect(url_for('login'))


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@current_app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


@current_app.errorhandler(503)
def internal_server_error(error):
    return render_template('errors/503.html'), 503


@current_app.errorhandler(AssertionError)
def handle_sqlalchemy_assertion_error(error):
    return error.args[0], 400


@current_app.route('/public/<path:filename>', methods=['GET'])
def uploaded_pictures(filename='Ladybug.jpg', methods=['GET']):
    """
    Exposes public files (media uploaded by users, etc.).
    """
    last_version = '2.5.0'
    client_version = request.args.get('monarc_version')

    print(request.args.get('monarc_version'))
    print(request.referrer)
    print(request.headers)
    print(request.user_agent)


    # if parse_version(last_version) > parse_version('client_version):
    #     filename = 'update-available.png'
    # else:
    #     filename = 'up-to-date.png'


    return send_from_directory(os.path.abspath(application.config['UPLOAD_FOLDER']), filename)


@current_app.route('/', methods=['GET'])
def index():
    last_version = 'v2.5.0'
    print(request.args.get('monarc_version'))
    # print(request.referrer)
    if not request.referrer:
        print('The referrer header is missing.')
    else:
        print(request.referrer)
    print(request.user_agent)
    print(dir(request))

    monarc = {'last_version': last_version}
    return jsonify(monarc)
    #return render_template('index.html')
