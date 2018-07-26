from web.views import views, session_mgmt
from web.views.admin import admin_bp
from web.views.user import user_bp
from web.views.stats import stats_bp
from web.views.api import v1

__all__ = ['views', 'session_mgmt', 'admin_bp', 'user_bp', 'stats_bp']
