from collections import Counter
from flask import Blueprint, render_template, jsonify
from sqlalchemy import func

from bootstrap import db, RELEASES
from web.models import Log

stats_bp = Blueprint('stats_bp', __name__, url_prefix='/stats')


@stats_bp.route('/<software>', methods=['GET'])
def stats(software=None):
    head_titles = ['Statistics for', software]
    return render_template('stats.html', software=software,
                            last_release=RELEASES[software]['stable'],
                            head_titles=head_titles)


@stats_bp.route('/<software>/versions.json', methods=['GET'])
def versions(software=None):
    """Returns a JSON with the repartition of versions."""
    result = db.session.query(func.lower(Log.software_version),
                Log.http_referrer). \
                group_by(func.lower(Log.software_version), Log.http_referrer). \
                filter(Log.software==software, Log.software_version!=None). \
                all()

    count = Counter()
    for version, http_referrer in result:
        count[version] += 1

    return jsonify(dict(count))

@stats_bp.route('/<software>/browsers.json', methods=['GET'])
def browsers(software=None):
    """Returns a JSON with the repartition of browsers."""
    result = db.session.query(func.lower(Log.user_agent_browser),
                func.count(func.lower(Log.user_agent_browser))). \
                group_by(func.lower(Log.user_agent_browser)). \
                filter(Log.software==software, Log.user_agent_browser!=None). \
                all()
    return jsonify(dict(result))

@stats_bp.route('/<software>/languages.json', methods=['GET'])
def languages(software=None):
    """Returns a JSON with the repartition of languages."""
    result = db.session.query(func.lower(Log.user_agent_language),
                func.count(func.lower(Log.user_agent_language))). \
                group_by(func.lower(Log.user_agent_language)). \
                filter(Log.software==software, Log.user_agent_language!=None). \
                all()
    return jsonify(dict(result))
