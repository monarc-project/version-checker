from datetime import datetime

from bootstrap import db

class Stat(db.Model):
    """
    Represent a stat.
    """
    id = db.Column(db.Integer, primary_key=True)
    http_referrer = db.Column(db.String())
    user_agent = db.Column(db.String()) # browser: name, version, language, platform
    monarc_version = db.Column(db.String())
    request_timestamp = db.Column(db.DateTime(), default=datetime.utcnow())

    def __str__(self):
        return self.id
