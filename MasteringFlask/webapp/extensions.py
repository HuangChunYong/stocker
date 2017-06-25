# coding=utf-8
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection="strong"
login_manager.login_message=u"您没有访问该页面的权限！"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(username):
    from models import users
    return users.query.get(username)

from flask_principal import Principal,Permission,RoleNeed
principals = Principal()
admin_permission = Permission(RoleNeed('admin'))
finance_analyst_permission = Permission(RoleNeed('finance_analyst'))
default_permission = Permission(RoleNeed('default'))

