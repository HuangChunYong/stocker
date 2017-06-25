from flask import Blueprint,redirect,render_template,url_for
from os import path
from webapp.extensions import finance_analyst_permission
from flask_principal import Permission,UserNeed,RoleNeed
from flask_login import login_required,current_user
stock_blueprint = Blueprint(
    'stock',
    __name__,
    template_folder=path.join(path.pardir,'templates','stock'),
    url_prefix="/stock"
)
@stock_blueprint.route('/',methods=('GET','POST'))
@login_required
def home():
    roles = current_user.roles
    return render_template("stock/home.html",current_user=current_user,roles=roles)