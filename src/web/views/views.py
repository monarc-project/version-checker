import os
import logging
from datetime import datetime
from pkg_resources import parse_version
from flask import (render_template, url_for, redirect, current_app, flash,
                  send_from_directory, request, jsonify)

from bootstrap import application, db, RELEASES, CVE
from web.models import Log
from lib import svg

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


@current_app.route('/check/<software>', methods=['GET'])
def check_version(software=None):
    """Checks the version of the requested software and stores some
    information about the client."""
    state = None
    text = None
    last_version = None
    client_version = request.args.get('version', None)

    if software in RELEASES.keys():
        last_version = RELEASES[software]['stable']
    else:
        software = None

    # Check the version of the client
    if client_version and last_version:
        if parse_version(last_version) > parse_version(client_version):
            state = 'update-available'
        elif parse_version(last_version) == parse_version(client_version):
            state = 'up-to-date'
    if not state:
        state = 'unknown'

    # Check if vulnerabilities in client version of the softwares
    if software in CVE.keys() and client_version:
        if CVE[software].get(client_version, False):
            # send the id of the CVE
            state = 'security-update-available'
            text = "security update available: "
            text += ", ".join(CVE[software].get(client_version))

    # Generate the image to return
    file_name = svg.simple_text(state, svg.STYLE[state], text)

    if request.referrer and software:
        # Log some information about the client
        log = Log(software=software, software_version=client_version,
                    http_referrer=request.referrer,
                    user_agent_browser=request.user_agent.browser,
                    user_agent_version=request.user_agent.version,
                    user_agent_language=request.user_agent.language,
                    user_agent_platform=request.user_agent.platform,
                    timestamp=datetime.utcnow())
        try:
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            print(e)

    return send_from_directory(
            os.path.abspath(application.config['GENERATED_SVG_FOLDER']),
                            file_name)


@current_app.route('/version/<software>', methods=['GET'])
def version(software=None):
    """Gives information about current version of a software."""
    if software in RELEASES.keys():
        return jsonify(RELEASES[software])
    else:
        return 'Unknown software.', 404
