from flask import Blueprint
from .health import health_check
from .stock import get_stock_history, get_indicators, fetch_stock_data
from .user import register, login, logout, user_info
from .. import login_manager
from ..models import User

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    if user_id and user_id != "None":
        return User.get_by_id(record_id=user_id)


v1_blueprint = Blueprint(name='v1', import_name='api1')


v1_blueprint.add_url_rule(
    '/health-check', view_func=health_check, methods=['GET'])
v1_blueprint.add_url_rule(
    '/user/register', view_func=register, methods=['POST'])
v1_blueprint.add_url_rule(
    '/user/login', view_func=login, methods=['GET', 'POST'])
v1_blueprint.add_url_rule(
    '/user/logout', view_func=logout, methods=['POST'])
v1_blueprint.add_url_rule(
    '/user/info', view_func=user_info, methods=['GET'])


v1_blueprint.add_url_rule(
    '/stock/<symbol>/history', view_func=get_stock_history, methods=['GET'])
v1_blueprint.add_url_rule(
    '/stock/<symbol>/indicators', view_func=get_indicators, methods=['GET'])
v1_blueprint.add_url_rule(
    '/stock/fetch', view_func=fetch_stock_data, methods=['POST'])






