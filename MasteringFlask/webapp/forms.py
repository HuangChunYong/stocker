#coding=utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField,PasswordField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,EqualTo,URL
from models import users
import MySQLdb

class CodeForm(Form):
    code = StringField('Stock Code',validators=[DataRequired()])
class LoginForm(Form):
    username = StringField('Username',[DataRequired(),Length(max=20)])
    password = PasswordField('Password',[DataRequired()])
    remember = BooleanField("Remember Me")
    def validate(self):
        check_validate = super(LoginForm,self).validate()
        if not check_validate:
            return False
        user = users.query.filter_by(username = self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid password')
            return False
        return True

class RegisterForm(Form):
    username = StringField('Username',[DataRequired(),Length(max=255)])
    password = PasswordField('Password',[DataRequired()])
    confirm = PasswordField('Confirm Password',[DataRequired(),EqualTo('password')])
    def validate(self):
        check_validate = super(RegisterForm,self).validate()
        if not check_validate:
            return False
        user = users.query.filter_by(username = self.username.data).first()
        if user:
            self.username.errors.append("Users with that name already exists")
            return False
        return True

# cns市场的数据准备
# cns_list1 = cns_department_industry.query.with_entities(cns_department_industry.industry_gicscode_1,cns_department_industry.industry_gics_1).all()
# cns_list2 = cns_group_industry.query.with_entities(cns_group_industry.industry_gicscode_2,cns_group_industry.industry_gics_2).all()
# cns_list3 = cns_industry.query.with_entities(cns_industry.industry_gicscode_3,cns_industry.industry_gics_3).all()
# cns_list4 = cns_sub_industry.query.with_entities(cns_sub_industry.industry_gicscode_4,cns_sub_industry.industry_gics_4).all()

conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
cursor = conn.cursor()
cursor.execute('select industry_gicscode_1,industry_gics_1 from cns_department_industry')
value1 = cursor.fetchall()
cns_list1 = list(value1)
cursor.execute('select industry_gicscode_2,industry_gics_2 from cns_group_industry')
value2 = cursor.fetchall()
cns_list2 = list(value2)
cursor.execute('select industry_gicscode_3,industry_gics_3 from cns_industry')
value3 = cursor.fetchall()
cns_list3 = list(value3)
cursor.execute('select industry_gicscode_4,industry_gics_4 from cns_sub_industry')
value4 = cursor.fetchall()
cns_list4 = list(value4)
cursor.close()
conn.close()

class cns_filterForm1(Form):
    gics_code = SelectField('industry_gics_1',choices=cns_list1)
class cns_filterForm2(Form):
    gics_code = SelectField('industry_gics_2',choices=cns_list2)
class cns_filterForm3(Form):
    gics_code = SelectField('industry_gics_3',choices=cns_list3)
class cns_filterForm4(Form):
    gics_code = SelectField('industry_gics_4',choices=cns_list4)



# 创建list数据源(python的方法做不出来了:有办法做出来)
conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
cursor=conn.cursor()
cursor.execute('select industry_gicscode_4,industry_gics_4 from cns_sub_industry ')
cns_value=cursor.fetchall()
cns_dropdownlist = list(cns_value)

class cns_UpdateForm(Form):
#   trade_code = StringField('trade_code',[DataRequired()])
    gics_4 = SelectField('gics_4',choices=cns_dropdownlist)

# 创建list数据源
conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
cursor = conn.cursor()
cursor.execute('select industry_gicscode_4,industry_gics_4 from usa_sub_industry')
usa_value = cursor.fetchall()
usa_dropdownlist = list(usa_value)

class usa_UpdateForm(Form):
    trade_code = StringField('trade_code', [DataRequired()])
    gics_4 = SelectField('gics_4',choices=usa_dropdownlist)

#test    language = SelectField('Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

# 美国行业筛选数据源
conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
cursor = conn.cursor()
cursor.execute('select industry_gicscode_1,industry_gics_1 from usa_department_industry')
value1 = cursor.fetchall()
list1 = list(value1)
cursor.execute('select industry_gicscode_2,industry_gics_2 from usa_group_industry')
value2 = cursor.fetchall()
list2 = list(value2)
cursor.execute('select industry_gicscode_3,industry_gics_3 from usa_industry')
value3 = cursor.fetchall()
list3 = list(value3)
cursor.execute('select industry_gicscode_4,industry_gics_4 from usa_sub_industry')
value4 = cursor.fetchall()
list4 = list(value4)
cursor.close()
conn.close()

class usa_filterForm1(Form):
    gics_code = SelectField('industry_gics_1',choices=list1)
class usa_filterForm2(Form):
    gics_code = SelectField('industry_gics_2',choices=list2)
class usa_filterForm3(Form):
    gics_code = SelectField('industry_gics_3',choices=list3)
class usa_filterForm4(Form):
    gics_code = SelectField('industry_gics_4',choices=list4)

# 修改部门行业分类标准
class usa_update_department_Form(Form):
    old_industry = SelectField('old_industry', choices=list1)
    new_industry = StringField('new_industry', [DataRequired()])

class departmentForm(Form):
    gics_code_1 = SelectField('gics_code_1',choices=list1)

# 5-22 test
# class testForm(Form):
#      first = SelectField('first',choices = list1)
#      second = NonValidatingSelectField('second',choices = [])
#      def cascading(form,field):
#          choices =



conn = MySQLdb.connect(user="root", passwd="0000", db="test", charset="utf8")
cursor = conn.cursor()
cursor.execute('select industry_gicscode_1,industry_gics_1 from hks_department_industry')
value1 = cursor.fetchall()
hks_list1 = list(value1)
cursor.execute('select industry_gicscode_2,industry_gics_2 from hks_group_industry')
value2 = cursor.fetchall()
hks_list2 = list(value2)
cursor.execute('select industry_gicscode_3,industry_gics_3 from hks_industry')
value3 = cursor.fetchall()
hks_list3 = list(value3)
cursor.execute('select industry_gicscode_4,industry_gics_4 from hks_sub_industry')
value4 = cursor.fetchall()
hks_list4 = list(value4)
cursor.close()
conn.close()

class hks_filterForm1(Form):
    gics_code = SelectField('industry_gics_1',choices=hks_list1)
class hks_filterForm2(Form):
    gics_code = SelectField('industry_gics_2',choices=hks_list2)
class hks_filterForm3(Form):
    gics_code = SelectField('industry_gics_3',choices=hks_list3)
class hks_filterForm4(Form):
    gics_code = SelectField('industry_gics_4',choices=hks_list4)