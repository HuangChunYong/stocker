#coding=utf-8
from flask import Blueprint,redirect,render_template,url_for
from os import path
from webapp.models import stock_basics,finance_basics,invest_values
from webapp.forms import CodeForm
from flask_login import login_required,current_user
from webapp.extensions import finance_analyst_permission # 这个就是经济师权限
import MySQLdb,time,re #re用于判断是否含中文
globalindustry_blueprint = Blueprint(
    'global_industry',
    __name__,
    template_folder=path.join(path.pardir,'templates','grobal_industry'),
    url_prefix="/global_industry"
)
@globalindustry_blueprint.route('/',methods=('GET','POST'))
@login_required
def basic():
    return render_template("global_industry/global_industry_basic.html")