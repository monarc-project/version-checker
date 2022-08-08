from datetime import datetime

from web.models.right_mixin import RightMixin
from bootstrap import db


class Log(db.Model, RightMixin):
    """
    Represent a log.
    """

    id = db.Column(db.Integer, primary_key=True)
    software = db.Column(db.String())
    software_version = db.Column(db.String())
    http_referrer = db.Column(db.String())
    user_agent_browser = db.Column(db.String())
    user_agent_version = db.Column(db.String())
    user_agent_language = db.Column(db.String())
    user_agent_platform = db.Column(db.String())
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return """Software: {}
Software version: {}
HTTP Referrer: {}
Browser: {}
Timestamp: {}\n""".format(
            self.software,
            self.software_version,
            self.http_referrer,
            self.user_agent_browser,
            self.timestamp,
        )
