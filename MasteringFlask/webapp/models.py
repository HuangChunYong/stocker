#coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import AnonymousUserMixin
db = SQLAlchemy()

roles = db.Table(
    'role_users',
    db.Column('user_name',db.String(80),db.ForeignKey('users.username')),
    db.Column('role_id',db.Integer,db.ForeignKey('role.id'))

)
class stock_basics(db.Model):
    __tablename__='stock_basics'
    trade_code = db.Column(db.String(20),primary_key=True)
    sec_name = db.Column(db.String(20))
    ipo_date = db.Column(db.DateTime())
    exch_city = db.Column(db.String(20))
    industry_gics = db.Column(db.String(20))
    concept = db.Column(db.String(200))
    curr = db.Column(db.String(20))
    fiscaldate = db.Column(db.String(20))
    auditor = db.Column(db.String(200))
    province = db.Column(db.String(20))
    city = db.Column(db.String(20))
    founddate = db.Column(db.DateTime())
    nature1 = db.Column(db.String(20))
    boardchairmen = db.Column(db.String(20))
    holder_controller = db.Column(db.String(20))
    website = db.Column(db.String(10000))
    phone = db.Column(db.String(200))
    majorproducttype = db.Column(db.String(200))
    majorproductname = db.Column(db.String(2000))

class finance_basics(db.Model):
    __tablename__='finance_basics'
    trade_code = db.Column(db.String(10),primary_key=True)
    sec_name = db.Column(db.String(40))
    the_year = db.Column(db.String(40),primary_key=True)
    tot_oper_rev = db.Column(db.Numeric(20,3))
    tot_oper_cost = db.Column(db.Numeric(20,3))
    fin_exp_is = db.Column(db.Numeric(20,3))
    tot_profit = db.Column(db.Numeric(20,3))
    net_profit_is = db.Column(db.Numeric(20,3))
    wgsd_net_inc = db.Column(db.Numeric(20,3))
    tot_assets = db.Column(db.Numeric(20,3))
    tot_cur_assets = db.Column(db.Numeric(20,3))
    tot_non_cur_assets = db.Column(db.Numeric(20,3))
    tot_liab = db.Column(db.Numeric(20,3))
    tot_cur_liab = db.Column(db.Numeric(20,3))
    tot_non_cur_liab = db.Column(db.Numeric(20,3))
    wgsd_com_eq = db.Column(db.Numeric(20,3))
    operatecashflow_ttm2 = db.Column(db.Numeric(20,3))
    investcashflow_ttm2 = db.Column(db.Numeric(20,3))
    financecashflow_ttm2 = db.Column(db.Numeric(20,3))
    cashflow_ttm2 = db.Column(db.Numeric(20,3))
    monetary_cap = db.Column(db.Numeric(20,3))
    grossprofitmargin = db.Column(db.Numeric(20,4))
    roic = db.Column(db.Numeric(20,4))
    turndays = db.Column(db.Numeric(20,4))
    invturndays = db.Column(db.Numeric(20,4))
    arturndays = db.Column(db.Numeric(20,4))
    apturndays = db.Column(db.Numeric(20,4))

class invest_values(db.Model):
    __tablename__='invest_values'
    trade_code = db.Column(db.String(40),primary_key=True)
    sec_name = db.Column(db.String(40))
    the_year = db.Column(db.String(40),primary_key=True)
    total_shares = db.Column(db.Numeric(38,6))
    div_cashandstock = db.Column(db.Numeric(38,6))
    ev = db.Column(db.Numeric(38,6))
    dividendyield2 = db.Column(db.Numeric(38,8))
    ev1 = db.Column(db.Numeric(38,6))
    ev2 = db.Column(db.Numeric(38,6))
    employee = db.Column(db.String(40))


class cns_department_industry(db.Model):
    __tablename__='cns_department_industry'
    industry_gicscode_1 = db.Column(db.String(40),primary_key = True)
    industry_gics_1 = db.Column(db.String(40))

class cns_group_industry(db.Model):
    industry_gicscode_2 = db.Column(db.String(40),primary_key = True)
    industry_gics_2 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('cns_department_industry.industry_gicscode_1'))

class cns_industry(db.Model):
    industry_gicscode_3 = db.Column(db.String(40),primary_key = True)
    industry_gics_3 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('cns_group_industry.industry_gicscode_2'))

class cns_sub_industry(db.Model):
    industry_gicscode_4 = db.Column(db.String(40),primary_key = True)
    industry_gics_4 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('cns_industry.industry_gicscode_3'))

class cns_stock_industry(db.Model):
    __tablename__='cns_stock_industry'
    trade_code = db.Column(db.String(40),primary_key=True)
    sec_name = db.Column(db.String(40))
    industry_gicscode_4 = db.Column(db.String(40))
    industry_gics_4 = db.Column(db.String(40))
    belong = db.Column(db.String(40),db.ForeignKey('cns_sub_industry.industry_gicscode_4'))
    ipo_date = db.Column(db.DateTime)
    business = db.Column(db.String(5000))
    province = db.Column(db.String(40))
    city = db.Column(db.String(40))
    exch_city = db.Column(db.String(40))
    country = db.Column(db.String(40))
    curr = db.Column(db.String(40))
    nature = db.Column(db.String(40))
    hushen_300 = db.Column(db.String(40))
    shangzheng_50 = db.Column(db.String(40))
    SHSC = db.Column(db.String(40))
    SHSC2 = db.Column(db.String(40))
    industry_CSRCcode12 = db.Column(db.String(40))
    industry_CSRC12 = db.Column(db.String(40))
    belong_zhengjianhui = db.Column(db.String(40), db.ForeignKey('zhengjianhui_1.industry_CSRCcode12'))

class zhengjianhui_1(db.Model):
    __tablename__='zhengjianhui_1'
    industry_CSRCcode12 = db.Column(db.String(40),primary_key=True)
    industry_CSRC12 = db.Column(db.String(40))

class zhengjianhui_2(db.Model):
    __tablename__='zhengjianhui_2'
    trade_code = db.Column(db.String(40),primary_key=True)
    industry_CSRCcode12 = db.Column(db.String(40))
    industry_CSRC12 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('zhengjianhui_1.industry_CSRCcode12'))

# 美国市场
class usa_department_industry(db.Model):
    __tablename__='usa_department_industry'
    industry_gicscode_1 = db.Column(db.String(40),primary_key = True)
    industry_gics_1 = db.Column(db.String(40))

class usa_group_industry(db.Model):
    __tablename__='usa_group_industry'
    industry_gicscode_2 = db.Column(db.String(40),primary_key = True)
    industry_gics_2 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('usa_department_industry.industry_gicscode_1'))

class usa_industry(db.Model):
    __tablename__='usa_industry'
    industry_gicscode_3 = db.Column(db.String(40), primary_key=True)
    industry_gics_3 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('usa_group_industry.industry_gicscode_2'))

class usa_sub_industry(db.Model):
    __tablename__ = 'usa_sub_industry'
    industry_gicscode_4 = db.Column(db.String(40),primary_key = True)
    industry_gics_4 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('usa_industry.industry_gicscode_3'))

class usa_stock_industry(db.Model):
    __tablename__ = 'usa_stock_industry'
    trade_code = db.Column(db.String(40),primary_key=True)
    sec_name = db.Column(db.String(40))
    ipo_date = db.Column(db.DateTime)
    industry_gicscode_4 = db.Column(db.String(40),db.ForeignKey('usa_sub_industry.industry_gicscode_4'))
    industry_gics_4 = db.Column(db.String(40))
    business = db.Column(db.String(5000))
    address = db.Column(db.String(5000))
    exch_city = db.Column(db.String(40))
    country = db.Column(db.String(40))
    curr = db.Column(db.String(40))
    briefing = db.Column(db.String(5000))

class usa_djia(db.Model):
    __tablename__ = 'usa_djia'
    trade_code = db.Column(db.String(40),primary_key=True)
    sec_name = db.Column(db.String(40))

# 香港市场
class hks_department_industry(db.Model):
    __tablename__='hks_department_industry'
    industry_gicscode_1 = db.Column(db.String(40),primary_key = True)
    industry_gics_1 = db.Column(db.String(40))

class hks_group_industry(db.Model):
    __tablename__='hks_group_industry'
    industry_gicscode_2 = db.Column(db.String(40),primary_key = True)
    industry_gics_2 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('hks_department_industry.industry_gicscode_1'))

class hks_industry(db.Model):
    __tablename__='hks_industry'
    industry_gicscode_3 = db.Column(db.String(40), primary_key=True)
    industry_gics_3 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('hks_group_industry.industry_gicscode_2'))

class hks_sub_industry(db.Model):
    __tablename__='hks_sub_industry'
    industry_gicscode_4 = db.Column(db.String(40),primary_key = True)
    industry_gics_4 = db.Column(db.String(40))
    belong = db.Column(db.String(40), db.ForeignKey('hks_industry.industry_gicscode_3'))

class hks_stock_industry(db.Model):
    __tablename__ = 'hks_stock_industry'
    trade_code = db.Column(db.String(40),primary_key=True)
    sec_name = db.Column(db.String(40))
    ipo_date = db.Column(db.DateTime)
    industry_gicscode_4 = db.Column(db.String(40),db.ForeignKey('hks_sub_industry.industry_gicscode_4'))
    industry_gics_4 = db.Column(db.String(40))
    business = db.Column(db.String(5000))
    address = db.Column(db.String(5000))
    exch_city = db.Column(db.String(40))
    country = db.Column(db.String(40))
    curr = db.Column(db.String(40))
    comp_name = db.Column(db.String(5000))

# 不要这个表了
# class cns_industry_detail(db.Model):
#     __tablename__='cns_industry_detail'
#     trade_code = db.Column(db.String(40),primary_key=True)
#     sec_name = db.Column(db.String(40))


class users(db.Model):
    __tablename__='users'
    username = db.Column(db.String(20),primary_key=True)
    password = db.Column(db.String(45))
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users',lazy='dynamic')
    )
    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def is_authenticated(self):
        if isinstance(self,AnonymousUserMixin):
            return False
        else:
            return True
    def is_active(self):
        return True
    def is_anonymous(self):
        if isinstance(self,AnonymousUserMixin):
            return True
        else:
            return False
    def get_id(self):
        return unicode(self.username)

class Role(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(80),unique=True)
    description = db.Column(db.String(255))



