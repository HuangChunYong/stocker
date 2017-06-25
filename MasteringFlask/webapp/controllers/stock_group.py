#coding=utf-8
from flask import Blueprint,redirect,render_template,url_for,request #me:request
from os import path
from webapp.models import * #me: stock_basics,finance_basics,invest_values,cns_stock_industry,cns_industry_detail
from webapp.forms import CodeForm,cns_UpdateForm,usa_UpdateForm,usa_filterForm1,usa_filterForm2,usa_filterForm3,usa_filterForm4,usa_update_department_Form,departmentForm,cns_filterForm1,cns_filterForm2,cns_filterForm3,cns_filterForm4,hks_filterForm1,hks_filterForm2,hks_filterForm3,hks_filterForm4
from flask_login import login_required,current_user
from webapp.extensions import finance_analyst_permission
# from flask_sqlalchemy import SQLAlchemy #me
from sqlalchemy import create_engine,or_,func,desc,distinct #me func用于计数,desc用于逆序找max值
from sqlalchemy.orm import sessionmaker #me
import MySQLdb,time
stockgroup_blueprint = Blueprint(
    'stock_group',
    __name__,
    template_folder=path.join(path.pardir,'templates','stock_group'),
    url_prefix="/stock_group"
)

# cns 大陆市场
@stockgroup_blueprint.route('/cns_home',methods=('GET','POST'))
@stockgroup_blueprint.route('/cns_home/<string:trade_code>',methods=('GET','POST'))
@login_required
# @finance_analyst_permission.require(http_exception=403)
def cns_home():
    cns_filterform1=cns_filterForm1()
    cns_filterform2=cns_filterForm2()
    cns_filterform3=cns_filterForm3()
    cns_filterform4=cns_filterForm4()
    page = request.args.get('page', 1, type=int)
    pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(cns_department_industry.industry_gics_1).join(zhengjianhui_1).add_columns(zhengjianhui_1.industry_CSRC12).filter(cns_group_industry.belong==cns_department_industry.industry_gicscode_1).filter(cns_industry.belong==cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong==cns_industry.industry_gicscode_3).filter(cns_stock_industry.belong==cns_sub_industry.industry_gicscode_4).filter(cns_stock_industry.belong_zhengjianhui==zhengjianhui_1.industry_CSRCcode12).order_by(cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False) #共有3197条记录 此为分页功能
    result = pagination.items
    length = len(result)
# filter(cns_department_industry.industry_gicscode_1=='10') 筛选行业类别OK
    v_stock_industry = cns_stock_industry.query.all() #以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/cns/cns_stock_industry.html",cns_filterform1=cns_filterform1,cns_filterform2=cns_filterform2,cns_filterform3=cns_filterform3,cns_filterform4=cns_filterform4,result=result,pagination=pagination,v_stock_industry=v_stock_industry, length=length)

# 显示“主营业务”详情
@stockgroup_blueprint.route('/cns_business_detail/',methods=('GET','POST'))
@stockgroup_blueprint.route('/cns_business_detail/<string:trade_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def cns_business_detail(trade_code='000895'): #需要这个默认trade_code吗？
    trade_code = trade_code # 哈哈，成功了！！
    result = cns_stock_industry.query.filter_by(trade_code=trade_code).first_or_404()
    return render_template("stock_group/cns/cns_business_detail.html",result=result)

# cns行业筛选
@stockgroup_blueprint.route('/cns_filter/',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def cns_filter():
    cns_filterform1 = cns_filterForm1()
    cns_filterform2= cns_filterForm2()
    cns_filterform3 = cns_filterForm3()
    cns_filterform4 = cns_filterForm4()
    if cns_filterform1.validate_on_submit():
        gics_code = request.form.get('gics_code')
       # industry_gics_1 = request.form.get('industry_gics_1')
        page = request.args.get('page',1,type=int)
        pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(cns_department_industry.industry_gics_1).filter(cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(cns_stock_industry.industry_gicscode_4 == cns_sub_industry.industry_gicscode_4).filter(cns_department_industry.industry_gicscode_1==gics_code).order_by(cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False) # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/cns/cns_stock_industry_filter.html", result=result, pagination=pagination, length=length,cns_filterform1=cns_filterform1,cns_filterform2=cns_filterform2,cns_filterform3=cns_filterform3,cns_filterform4=cns_filterform4)
    if cns_filterform2.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(cns_department_industry.industry_gics_1).filter(cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(cns_stock_industry.industry_gicscode_4 == cns_sub_industry.industry_gicscode_4).filter(cns_group_industry.industry_gicscode_2 == gics_code).order_by(cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/cns/cns_stock_industry_filter.html", result=result, pagination=pagination,length=length,cns_filterform1=cns_filterform1,cns_filterform2=cns_filterform2,cns_filterform3=cns_filterform3,cns_filterform4=cns_filterform4)
    if cns_filterform3.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(cns_department_industry.industry_gics_1).filter(cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(cns_stock_industry.industry_gicscode_4 == cns_sub_industry.industry_gicscode_4).filter(cns_industry.industry_gicscode_3 == gics_code).order_by(cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/cns/cns_stock_industry_filter.html", result=result, pagination=pagination,length=length, cns_filterform1=cns_filterform1,cns_filterform2=cns_filterform2,cns_filterform3=cns_filterform3,cns_filterform4=cns_filterform4)
    if cns_filterform4.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(cns_department_industry.industry_gics_1).filter(cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(cns_stock_industry.industry_gicscode_4 == cns_sub_industry.industry_gicscode_4).filter(cns_sub_industry.industry_gicscode_4 == gics_code).order_by(cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/cns/cns_stock_industry_filter.html", result=result, pagination=pagination,length=length, cns_filterform1=cns_filterform1,cns_filterform2=cns_filterform2,cns_filterform3=cns_filterform3,cns_filterform4=cns_filterform4)
    return render_template("404.html") # 或许可用if-elif来改写一下



# 修改“子行业”信息
@stockgroup_blueprint.route('/update_gics_4/',methods=('GET','POST'))
@stockgroup_blueprint.route('/update_gics_4/<string:trade_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def update_gics_4(trade_code='000001'): #疑问：这一行是什么意思？
    form = cns_UpdateForm()
    trade_code = trade_code
    information = cns_stock_industry.query.filter_by(trade_code=trade_code).first_or_404()

    if form.validate_on_submit():
        trade_code = request.form.get('trade_code')
        gics_4 = request.form.get('gics_4')
        db_engine = create_engine('mysql://root:0000@localhost/test?charset=utf8')
        Session = sessionmaker(bind=db_engine)
        session = Session()
        session.query(cns_stock_industry).filter(cns_stock_industry.trade_code == trade_code).update({'belong': gics_4}) #改为belong
        session.commit() # 少写了这一行，所以修改没成功
        return redirect(url_for('.home'))
    return render_template('stock_group/cns/update_gics_4.html',form=form,information=information)

# 创建dropdownlist数据源
# def dropdownlist():
#      list=[]
#      rs = cns_sub_industry.query.all()
#      for x in range(len(rs)):
#          list.append((rs[x].industry_gicscode_4 , rs[x].industry_gics_4))
#      return list

# 沪深300指数筛选
@stockgroup_blueprint.route('/hushen_300', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/hushen_300/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def hushen_300():
    page = request.args.get('page', 1, type=int)
    pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(
        cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(
        cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(
        cns_department_industry.industry_gics_1).filter(
        cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(
        cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(
        cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(
        cns_stock_industry.belong == cns_sub_industry.industry_gicscode_4).filter(cns_stock_industry.hushen_300=='是').order_by(
        cns_stock_industry.trade_code).paginate(page, per_page=300, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items
    length = len(result)

    v_stock_industry = cns_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/cns/cns_hushen_300.html", result=result, pagination=pagination,
                            v_stock_industry=v_stock_industry, length=length)

# 上证50指数筛选
@stockgroup_blueprint.route('/shangzheng_50', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/shangzheng_50/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def shangzheng_50():
    page = request.args.get('page', 1, type=int)
    pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(
        cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(
        cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(
        cns_department_industry.industry_gics_1).filter(
        cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(
        cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(
        cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(
        cns_stock_industry.belong == cns_sub_industry.industry_gicscode_4).filter(
        cns_stock_industry.shangzheng_50 == '是').order_by(
        cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items
    length = len(result)

    v_stock_industry = cns_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/cns/cns_shangzheng_50.html", result=result, pagination=pagination,
                            v_stock_industry=v_stock_industry, length=length)

# 陆股通指数筛选
@stockgroup_blueprint.route('/lugutong', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/lugutong/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def lugutong():
    page = request.args.get('page', 1, type=int)
    pagination = cns_stock_industry.query.join(cns_sub_industry).add_columns(cns_sub_industry.industry_gics_4).join(cns_industry).add_columns(cns_industry.industry_gics_3).join(cns_group_industry).add_columns(cns_group_industry.industry_gics_2).join(cns_department_industry).add_columns(cns_department_industry.industry_gics_1).filter(cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(cns_stock_industry.belong == cns_sub_industry.industry_gicscode_4).filter(or_(cns_stock_industry.SHSC == '是',cns_stock_industry.SHSC2 == '是')).order_by(cns_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items
    length = len(result)
# or_要从sqlalchemy中加载
    v_stock_industry = cns_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/cns/cns_lugutong.html", result=result, pagination=pagination,
                            v_stock_industry=v_stock_industry, length=length)
    # page = request.args.get('page', 1, type=int)
#以下是联合查询
    # engine = create_engine('mysql+pymysql://root:0000@localhost:3306/test?charset=utf8', echo=True)
    # Session = sessionmaker(bind=engine)
    # session = Session()



  #  test_list = cns_stock_industry.query.join(cns_sub_industry).join(cns_industry).join(cns_group_industry).join(cns_department_industry).filter(cns_group_industry.belong==cns_department_industry.industry_gicscode_1).filter(cns_industry.belong==cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong==cns_industry.industry_gicscode_3).filter(cns_stock_industry.belong==cns_sub_industry.industry_gicscode_4)

    # pagination = session.query(cns_department_industry.industry_gics_1,cns_group_industry.industry_gics_2,cns_industry.industry_gics_3,cns_stock_industry.industry_gics_4).filter(cns_group_industry.belong == cns_department_industry.industry_gicscode_1).filter(cns_industry.belong == cns_group_industry.industry_gicscode_2).filter(cns_sub_industry.belong == cns_industry.industry_gicscode_3).filter(cns_stock_industry.belong == cns_sub_industry.industry_gicscode_4).order_by('trade_code')\
    # .paginate(page, per_page=300, error_out=False)
    # result = pagination.items

# 注意：‘trade_code’ 改一下
# pagination = stock_basics.query.order_by(stock_basics.trade_code).paginate(page, per_page=10,error_out=False)
# per_page是用于表示每页显示的数目


# usa美国市场
@stockgroup_blueprint.route('/usa_home',methods=('GET','POST'))
@stockgroup_blueprint.route('/usa_home/<string:trade_code>',methods=('GET','POST'))
@login_required
# 有什么用？@finance_analyst_permission.require(http_exception=403)
def usa_home():
    usa_filterform1 = usa_filterForm1()
    usa_filterform2 = usa_filterForm2()
    usa_filterform3 = usa_filterForm3()
    usa_filterform4 = usa_filterForm4()
    page = request.args.get('page', 1, type=int)
    pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(usa_department_industry.industry_gics_1).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False) #这一段去掉了也无影响：.filter(usa_group_industry.belong==usa_department_industry.industry_gicscode_1).filter(usa_industry.belong==usa_group_industry.industry_gicscode_2).filter(usa_sub_industry.belong==usa_industry.industry_gicscode_3).filter(usa_stock_industry.industry_gicscode_4==usa_sub_industry.industry_gicscode_4)
    result = pagination.items # per_page从300改成了200
    length = len(result)
    # v_stock_industry = usa_stock_industry.query.all() #以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/usa/usa_stock_industry.html",usa_filterform1=usa_filterform1,usa_filterform2=usa_filterform2,usa_filterform3=usa_filterform3,usa_filterform4=usa_filterform4,result=result,pagination=pagination,length=length)

# usa-显示“主营业务”详情
@stockgroup_blueprint.route('/usa_business_detail/',methods=('GET','POST'))
@stockgroup_blueprint.route('/usa_business_detail/<string:trade_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_business_detail(trade_code='000895'): # 没写usa_就会报错，怎么回事？
    trade_code = trade_code # 哈哈，成功了！！
    result = usa_stock_industry.query.filter_by(trade_code=trade_code).first_or_404()
    return render_template("stock_group/usa/usa_business_detail.html",result=result)

# usa修改“子行业”信息
@stockgroup_blueprint.route('/usa_update_gics_4/',methods=('GET','POST'))
@stockgroup_blueprint.route('/usa_update_gics_4/<string:trade_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_update_gics_4(trade_code='A'): #疑问：这一行是什么意思？之前写的‘000001’就不对，必须改成‘A’
    form = usa_UpdateForm()
    trade_code = trade_code
    information = usa_stock_industry.query.filter_by(trade_code=trade_code).first_or_404()
    if form.validate_on_submit():
        trade_code = request.form.get('trade_code')
        gics_4 = request.form.get('gics_4')
        db_engine = create_engine('mysql://root:0000@localhost/test?charset=utf8')
        Session = sessionmaker(bind=db_engine)
        session = Session()
        session.query(usa_stock_industry).filter(usa_stock_industry.trade_code == trade_code).update({'industry_gicscode_4': gics_4}) #改为belong
        session.commit() # 少写了这一行，所以修改没成功
        return redirect(url_for('.usa_home'))
    return render_template('stock_group/usa/usa_update_gics_4.html',form=form,information=information)

# usa修改行业分类标准
@stockgroup_blueprint.route('/usa_update_industry/',methods=('GET','POST'))
@stockgroup_blueprint.route('/usa_update_industry/<string:trade_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_update_industry(trade_code='A'): #疑问：这一行是什么意思？之前写的‘000001’就不对，必须改成‘A’
    form = usa_Update_department_1_Form()
    if form.validate_on_submit():
        old_industry = request.form.get('old_industry')
        new_industry = request.form.get('new_industry')
        db_engine = create_engine('mysql://root:0000@localhost/test?charset=utf8')
        Session = sessionmaker(bind=db_engine)
        session = Session()
        session.query(usa_department_industry).filter(usa_department_industry.industry_gicscode_1 == old_industry).update({'industry_gics_1': new_industry}) #改为belong
        session.commit() # 少写了这一行，所以修改没成功
        return redirect(url_for('.usa_home'))
    return render_template('stock_group/usa/usa_Update_department_1.html',form=form)

# usa行业筛选
@stockgroup_blueprint.route('/usa_filter/',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_filter():
    usa_filterform1 = usa_filterForm1()
    usa_filterform2= usa_filterForm2()
    usa_filterform3 = usa_filterForm3()
    usa_filterform4 = usa_filterForm4()
    if usa_filterform1.validate_on_submit():
        gics_code = request.form.get('gics_code')
       # industry_gics_1 = request.form.get('industry_gics_1')
        page = request.args.get('page',1,type=int)
        pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(usa_department_industry.industry_gics_1).filter(usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(usa_stock_industry.industry_gicscode_4 == usa_sub_industry.industry_gicscode_4).filter(usa_department_industry.industry_gicscode_1==gics_code).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False) # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/usa/usa_stock_industry_filter.html", result=result, pagination=pagination, length=length,usa_filterform1=usa_filterform1,usa_filterform2=usa_filterform2,usa_filterform3=usa_filterform3,usa_filterform4=usa_filterform4)
    if usa_filterform2.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(usa_department_industry.industry_gics_1).filter(usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(usa_stock_industry.industry_gicscode_4 == usa_sub_industry.industry_gicscode_4).filter(usa_group_industry.industry_gicscode_2 == gics_code).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/usa/usa_stock_industry_filter.html", result=result, pagination=pagination,length=length,usa_filterform1=usa_filterform1,usa_filterform2=usa_filterform2,usa_filterform3=usa_filterform3,usa_filterform4=usa_filterform4)
    if usa_filterform3.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(usa_department_industry.industry_gics_1).filter(usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(usa_stock_industry.industry_gicscode_4 == usa_sub_industry.industry_gicscode_4).filter(usa_industry.industry_gicscode_3 == gics_code).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/usa/usa_stock_industry_filter.html", result=result, pagination=pagination,length=length, usa_filterform1=usa_filterform1,usa_filterform2=usa_filterform2,usa_filterform3=usa_filterform3,usa_filterform4=usa_filterform4)
    if usa_filterform4.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(usa_department_industry.industry_gics_1).filter(usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(usa_stock_industry.industry_gicscode_4 == usa_sub_industry.industry_gicscode_4).filter(usa_sub_industry.industry_gicscode_4 == gics_code).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/usa/usa_stock_industry_filter.html", result=result, pagination=pagination,length=length, usa_filterform1=usa_filterform1,usa_filterform2=usa_filterform2,usa_filterform3=usa_filterform3,usa_filterform4=usa_filterform4)
    return render_template("404.html") # 或许可用if-elif来改写一下

# # usa 行业筛选
# @stockgroup_blueprint.route('/usa_filter/',methods=('GET','POST'))
# # @stockgroup_blueprint.route('/usa_filter/<string:trade_code>',methods=('GET','POST'))
# @login_required
# @finance_analyst_permission.require(http_exception=403)
# def usa_filter(gics_code=None):
#     trade_code = request.args.get("trade_code") #超链接传过来的值获取下来了
#     gics_code = gics_code
#     if gics_code is None:
#         result = usa_department_industry.query.all()
#         length = 0
#         num = range(len(result))
#     elif len(gics_code) == 2:
#         result = usa_group_industry.query.filter_by(belong=gics_code).all()
#         length = len(gics_code)
#         num = range(len(result))
#     elif len(gics_code)==4:
#         result = usa_industry.query.filter_by(belong=gics_code).all()
#         length = len(gics_code)
#         num = range(len(result))
#     elif len(gics_code)==6:
#         result = usa_sub_industry.query.filter_by(belong=gics_code).all() #少写个.query,要细心！
#         length = len(gics_code)
#         num = range(len(result))
#     elif len(gics_code) == 8:
#         db_engine = create_engine('mysql://root:0000@localhost/test?charset=utf8')
#         Session = sessionmaker(bind=db_engine)
#         session = Session()
#         session.query(usa_stock_industry).filter(usa_stock_industry.trade_code == trade_code).update(
#             {'industry_gicscode_4': gics_code})  # 改为belong
#         session.commit()  # 少写了这一行，所以修改没成功
#         return redirect(url_for('.usa_home'))
#     if request.method == 'POST':
#         gics_code = request.form['gics_code']
#         trade_code = request.form['trade_code']
#         return redirect(url_for('stock_group.usa_filter', gics_code=gics_code,trade_code=trade_code))
#     return render_template("stock_group/usa/industry_filter.html", gics_code=gics_code,trade_code=trade_code,result=result,length=length,num=num)


    # if form.validate_on_submit():
    #     gics_code = request.form.get('gics_code')
    # #   industry_gics_1 = request.form.get('industry_gics_1')
    # #   trade_code = request.form['trade_code']
    #     page = request.args.get('page',1,type=int)
    #     pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(
    #         usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(
    #         usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(
    #         usa_department_industry.industry_gics_1).filter(
    #         usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(
    #         usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(
    #         usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(
    #         usa_stock_industry.industry_gicscode_4 == usa_sub_industry.industry_gicscode_4).filter(usa_department_industry.industry_gicscode_1==gics_code).order_by(
    #         usa_stock_industry.trade_code).paginate(page, per_page=300, error_out=False)
    #     result = pagination.items
    #     length = len(result)
    #     return render_template("stock_group/usa/usa_stock_industry.html", result=result, pagination=pagination, length=length)
    #     # v_stock_industry = usa_stock_industry.query.all()  # 以下是获取数据总共有多少个
    #     # stock_length = len(v_stock_industry)
    # return render_template("stock_group/usa/usa_filter.html",form=form)

# 道琼斯工业指数成份股
@stockgroup_blueprint.route('/usa_djia', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/usa_djia/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_djia():
# 获取道琼斯名单列表
    conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
    cursor=conn.cursor()
    cursor.execute('select trade_code from usa_djia ')
    value=cursor.fetchall()
    djia_list = list(value)

    page = request.args.get('page', 1, type=int)
    pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(
        usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(
        usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(
        usa_department_industry.industry_gics_1).filter(
        usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(
        usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(
        usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(usa_stock_industry.trade_code.in_(djia_list) ).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items #???这里只有26个
    length = len(result)

    v_stock_industry = usa_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/usa/usa_djia.html", result=result, pagination=pagination,
                            v_stock_industry=v_stock_industry, length=length)

# 标准普尔500成份股
@stockgroup_blueprint.route('/usa_sp500', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/usa_sp500/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_sp500():
# 获取标准普尔500名单列表
    conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
    cursor=conn.cursor()
    cursor.execute('select trade_code from usa_sp500 ')
    value=cursor.fetchall()
    sp500_list = list(value)

    page = request.args.get('page', 1, type=int)
    pagination = usa_stock_industry.query.join(usa_sub_industry).add_columns(usa_sub_industry.industry_gics_4).join(
        usa_industry).add_columns(usa_industry.industry_gics_3).join(usa_group_industry).add_columns(
        usa_group_industry.industry_gics_2).join(usa_department_industry).add_columns(
        usa_department_industry.industry_gics_1).filter(
        usa_group_industry.belong == usa_department_industry.industry_gicscode_1).filter(
        usa_industry.belong == usa_group_industry.industry_gicscode_2).filter(
        usa_sub_industry.belong == usa_industry.industry_gicscode_3).filter(usa_stock_industry.trade_code.in_(sp500_list) ).order_by(usa_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有条记录 此为分页功能
    result = pagination.items #???这里只有26个
    length = len(result)

    v_stock_industry = usa_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/usa/usa_sp500.html", result=result, pagination=pagination,v_stock_industry=v_stock_industry, length=length)

# hks 香港市场
@stockgroup_blueprint.route('/hks_home',methods=('GET','POST'))
@stockgroup_blueprint.route('/hks_home/<string:trade_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def hks_home():
    hks_filterform1 = hks_filterForm1()
    hks_filterform2 = hks_filterForm2()
    hks_filterform3 = hks_filterForm3()
    hks_filterform4 = hks_filterForm4()
    page = request.args.get('page', 1, type=int)
    pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(hks_department_industry.industry_gics_1).filter(hks_group_industry.belong==hks_department_industry.industry_gicscode_1).filter(hks_industry.belong==hks_group_industry.industry_gicscode_2).filter(hks_sub_industry.belong==hks_industry.industry_gicscode_3).filter(hks_stock_industry.industry_gicscode_4==hks_sub_industry.industry_gicscode_4).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False) #共有?条记录 此为分页功能
    result = pagination.items
    length = len(result)
    # v_stock_industry = hks_stock_industry.query.all() #以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/hks/hks_stock_industry.html",hks_filterform1=hks_filterform1,hks_filterform2=hks_filterform2,hks_filterform3=hks_filterform3,hks_filterform4=hks_filterform4,result=result,pagination=pagination,length=length)

# hks行业筛选
@stockgroup_blueprint.route('/hks_filter/',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def hks_filter():
    hks_filterform1 = hks_filterForm1()
    hks_filterform2= hks_filterForm2()
    hks_filterform3 = hks_filterForm3()
    hks_filterform4 = hks_filterForm4()
    if hks_filterform1.validate_on_submit():
        gics_code = request.form.get('gics_code')
       # industry_gics_1 = request.form.get('industry_gics_1')
        page = request.args.get('page',1,type=int)
        pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(hks_department_industry.industry_gics_1).filter(hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.industry_gicscode_4 == hks_sub_industry.industry_gicscode_4).filter(hks_department_industry.industry_gicscode_1==gics_code).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False) # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/hks/hks_stock_industry_filter.html", result=result, pagination=pagination, length=length,hks_filterform1=hks_filterform1,hks_filterform2=hks_filterform2,hks_filterform3=hks_filterform3,hks_filterform4=hks_filterform4)
    if hks_filterform2.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(hks_department_industry.industry_gics_1).filter(hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.industry_gicscode_4 == hks_sub_industry.industry_gicscode_4).filter(hks_group_industry.industry_gicscode_2 == gics_code).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/hks/hks_stock_industry_filter.html", result=result, pagination=pagination,length=length,hks_filterform1=hks_filterform1,hks_filterform2=hks_filterform2,hks_filterform3=hks_filterform3,hks_filterform4=hks_filterform4)
    if hks_filterform3.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(hks_department_industry.industry_gics_1).filter(hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.industry_gicscode_4 == hks_sub_industry.industry_gicscode_4).filter(hks_industry.industry_gicscode_3 == gics_code).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/hks/hks_stock_industry_filter.html", result=result, pagination=pagination,length=length, hks_filterform1=hks_filterform1,hks_filterform2=hks_filterform2,hks_filterform3=hks_filterform3,hks_filterform4=hks_filterform4)
    if hks_filterform4.validate_on_submit():
        gics_code=request.form.get('gics_code')
        page = request.args.get('page', 1, type=int)
        pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(hks_department_industry.industry_gics_1).filter(hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.industry_gicscode_4 == hks_sub_industry.industry_gicscode_4).filter(hks_sub_industry.industry_gicscode_4 == gics_code).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 300改为200
        result = pagination.items
        length = len(result)
        return render_template("stock_group/hks/hks_stock_industry_filter.html", result=result, pagination=pagination,length=length, hks_filterform1=hks_filterform1,hks_filterform2=hks_filterform2,hks_filterform3=hks_filterform3,hks_filterform4=hks_filterform4)
    return render_template("404.html") # 或许可用if-elif来改写一下

# 恒生成份股
@stockgroup_blueprint.route('/hks_hengsheng_index', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/hks_hengsheng_index/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def hks_hengsheng_index():
# 获取道琼斯名单列表
    conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
    cursor=conn.cursor()
    cursor.execute('select trade_code from hks_hengsheng_index ')
    value=cursor.fetchall()
    hks_hengsheng_index_list = list(value)

    page = request.args.get('page', 1, type=int)
    pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(
        hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(
        hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(
        hks_department_industry.industry_gics_1).filter(
        hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(
        hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(
        hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.trade_code.in_(hks_hengsheng_index_list) ).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items #???这里只有26个
    length = len(result)

    # v_stock_industry = hks_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/hks/hks_hengsheng_index.html", result=result, pagination=pagination, length=length)

# hengsheng成份股2
@stockgroup_blueprint.route('/hks_hengsheng_comindex', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/hks_hengsheng_comindex/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def hks_hengsheng_comindex():
# 获取道琼斯名单列表
    conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
    cursor=conn.cursor()
    cursor.execute('select trade_code from hks_hengsheng_comindex ')
    value=cursor.fetchall()
    hks_hengsheng_comindex_list = list(value)

    page = request.args.get('page', 1, type=int)
    pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(
        hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(
        hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(
        hks_department_industry.industry_gics_1).filter(
        hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(
        hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(
        hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.trade_code.in_(hks_hengsheng_comindex_list) ).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items #???这里只有26个
    length = len(result)

    # v_stock_industry = hks_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/hks/hks_hengsheng_comindex.html", result=result, pagination=pagination, length=length)


# 港股通
@stockgroup_blueprint.route('/hks_ganggutong', methods=('GET', 'POST'))
@stockgroup_blueprint.route('/hks_ganggutong/<string:trade_code>', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def hks_ganggutong():
# 获取名单列表
    conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
    cursor=conn.cursor()
    cursor.execute('select trade_code from hks_ganggutong ')
    value=cursor.fetchall()
    hks_ganggutong_list = list(value)

    page = request.args.get('page', 1, type=int)
    pagination = hks_stock_industry.query.join(hks_sub_industry).add_columns(hks_sub_industry.industry_gics_4).join(
        hks_industry).add_columns(hks_industry.industry_gics_3).join(hks_group_industry).add_columns(
        hks_group_industry.industry_gics_2).join(hks_department_industry).add_columns(
        hks_department_industry.industry_gics_1).filter(
        hks_group_industry.belong == hks_department_industry.industry_gicscode_1).filter(
        hks_industry.belong == hks_group_industry.industry_gicscode_2).filter(
        hks_sub_industry.belong == hks_industry.industry_gicscode_3).filter(hks_stock_industry.trade_code.in_(hks_ganggutong_list)).order_by(hks_stock_industry.trade_code).paginate(page, per_page=200, error_out=False)  # 共有3197条记录 此为分页功能
    result = pagination.items #???这里只有26个
    length = len(result)

    # v_stock_industry = hks_stock_industry.query.all()  # 以下是获取数据总共有多少个
    # stock_length = len(v_stock_industry)
    return render_template("stock_group/hks/hks_ganggutong.html", result=result, pagination=pagination, length=length)

# test z行业级联菜单<string:trade_code> # 终于做出来了。。。心累
@stockgroup_blueprint.route('/usa_alter_sub_industry/',methods=('GET','POST')) # 这里也需要,methods=('GET','POST')
@stockgroup_blueprint.route('/usa_alter_sub_industry/<string:gics_code>',methods=('GET','POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def usa_alter_sub_industry(gics_code=None):
    sec_name = request.args.get("sec_name") #超链接传过来的值获取下来了
    gics_code = gics_code
    if gics_code is None:
        result = usa_department_industry.query.all()
        length = 0
        num = range(len(result))
    elif len(gics_code) == 2:
        result = usa_group_industry.query.filter_by(belong=gics_code).all()
        length = len(gics_code)
        num = range(len(result))
    elif len(gics_code)==4:
        result = usa_industry.query.filter_by(belong=gics_code).all()
        length = len(gics_code)
        num = range(len(result))
    elif len(gics_code)==6:
        result = usa_sub_industry.query.filter_by(belong=gics_code).all() #少写个.query,要细心！
        length = len(gics_code)
        num = range(len(result))
    elif len(gics_code) == 8:
        db_engine = create_engine('mysql://root:0000@localhost/test?charset=utf8')
        Session = sessionmaker(bind=db_engine)
        session = Session()
        session.query(usa_stock_industry).filter(usa_stock_industry.sec_name == sec_name).update(
            {'industry_gicscode_4': gics_code})  # 改为belong
        session.commit()  # 少写了这一行，所以修改没成功
        return redirect(url_for('.usa_home'))
    if request.method == 'POST':
        gics_code = request.form['gics_code']
        sec_name = request.form['sec_name']
        return redirect(url_for('stock_group.usa_alter_sub_industry', gics_code=gics_code,sec_name=sec_name))
    return render_template("stock_group/usa/usa_alter_sub_industry.html", gics_code=gics_code,sec_name=sec_name,result=result,length=length,num=num)


    # @stockgroup_blueprint.route('/first/', methods=('GET', 'POST'))
    # @stockgroup_blueprint.route('/first/<string:department>', methods=('GET', 'POST'))
    # # @stockgroup_blueprint.route('/first/<string:department>/<string:group>/<string:global_industry>/<string:sub>',methods=('GET','POST'))
    # @login_required
    # @finance_analyst_permission.require(http_exception=403)
    # def first(department=None, group=None, global_industry=None, sub=None):
    #     test = request.form['department']
    #     return render_template("stock_group/second.html", test=test)


# @stockgroup_blueprint.route('/second/',methods=('GET','POST'))
# def second(department=None, group=None, global_industry=None, sub=None):
#     if request.method == "POST":
#         gics_code_1 = request.form.get('gics_code_1')
#         conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
#         cursor = conn.cursor()
#         cursor.execute("select industry_gicscode_2,industry_gics_2 from usa_group_industry where belong ="+gics_code_1+"")
#         value2 = cursor.fetchall()
#         list2 = list(value2)
#         cursor.close()
#         conn.close()
#         return render_template("stock_group/second.html", list2=list2)

# if request.method == "POST":
#     gics_code_1 = request.form.get('gics_code_1')
    #     db_query = usa_group_industry.query.filter(usa_group_industry.industry_gicscode_2.like(gics_code_1+"%")).all()

# 行业分类计数
#
@stockgroup_blueprint.route('/industry_count', methods=('GET', 'POST'))
@login_required
@finance_analyst_permission.require(http_exception=403)
def industry_count():
    db_engine = create_engine('mysql://root:0000@localhost/test?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
#统计行业组
    group_industry_count = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_group_industry.industry_gics_2).order_by(cns_group_industry.industry_gicscode_2)
    group_industry_count_max_r = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_group_industry.industry_gics_2).order_by(func.count(cns_stock_industry.industry_gics_4).desc()).first()
    group_industry_count_max_value = group_industry_count_max_r[0]
    group_industry_count_group = session.query(func.count(distinct(cns_group_industry.industry_gics_2)))
#统计行业
    industry_count = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_industry.industry_gics_3).order_by(cns_industry.industry_gicscode_3)
    industry_count_max_r = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_industry.industry_gics_3).order_by(func.count(cns_stock_industry.industry_gics_4).desc()).first()
    industry_count_max_value = industry_count_max_r[0]
    industry_count_group = session.query(func.count(distinct(cns_industry.industry_gics_3)))
#统计子行业
    sub_industry_count = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_stock_industry.industry_gics_4).order_by(cns_stock_industry.industry_gicscode_4)
    sub_industry_count_max_r = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_stock_industry.industry_gics_4).order_by(func.count(cns_stock_industry.industry_gics_4).desc()).first()
    sub_industry_count_max_value = sub_industry_count_max_r[0]
    sub_industry_count_group = session.query(func.count(distinct(cns_stock_industry.industry_gics_4)))
#统计省份
    province_count = session.query(cns_stock_industry.province,func.count(cns_stock_industry.province)).group_by(cns_stock_industry.province).order_by(cns_stock_industry.industry_gicscode_4)
    province_count_max_r = session.query(cns_stock_industry.province,func.count(cns_stock_industry.province)).group_by(cns_stock_industry.province).order_by(func.count(cns_stock_industry.province).desc()).first()
    province_count_max_value = province_count_max_r[1]
    # 获取group_by后分组数
    province_count_group = session.query(func.count(distinct(cns_stock_industry.province)))

    return render_template("stock_group/cns/cns_industry_count.html", sub_industry_count=sub_industry_count , sub_industry_count_max_value=sub_industry_count_max_value,sub_industry_count_group=sub_industry_count_group,province_count=province_count,province_count_group=province_count_group,province_count_max_value=province_count_max_value,industry_count=industry_count,industry_count_max_value=industry_count_max_value,industry_count_group=industry_count_group,group_industry_count=group_industry_count,group_industry_count_max_value=group_industry_count_max_value,group_industry_count_group=group_industry_count_group)

# 逆序排序，用于找最大值
# count_query = session.query(func.count(cns_stock_industry.industry_gics_4)).join(cns_sub_industry).add_column(cns_sub_industry.industry_gics_4).join(cns_industry).add_column(cns_industry.industry_gics_3).join(cns_group_industry).add_column(cns_group_industry.industry_gics_2).join(cns_department_industry).add_column(cns_department_industry.industry_gics_1).group_by(cns_stock_industry.industry_gics_4).order_by(func.count(cns_stock_industry.industry_gics_4).desc()).first() # 添加了first后相当于选择了结果集中的第一行记录

# max_value = max_value_ready[0]
