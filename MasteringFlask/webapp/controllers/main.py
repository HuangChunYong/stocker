#coding=utf-8
from flask import Blueprint,redirect,url_for,flash,render_template
from webapp.forms import LoginForm,RegisterForm
from webapp.models import users,db
from flask_login import login_user,login_required,logout_user,current_user,current_app
from flask_principal import Identity,AnonymousIdentity,identity_changed
main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)

@main_blueprint.route('/')
def index():
    return redirect(url_for('main.login'))

@main_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    register_form = RegisterForm()
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).one()
        login_user(user,remember=form.remember.data)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.username)
        )
        flash("You have been logged in",category="success")
        return redirect(url_for('stock.home'))
    return render_template('main/login.html',form=form,register_form=register_form)

@main_blueprint.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = users()
        new_user.username = register_form.username.data
        new_user.set_password(register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(
            "注册成功！请登录",
            category="success"
        )
        return redirect(url_for('.login'))
    else:
        return redirect(url_for('.login'))



# @main_blueprint.route('/register',methods=['GET','POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         new_user = users()
#         new_user.username = form.username.data
#         new_user.set_password(form.password.data)
#         db.session.add(new_user)
#         db.session.commit()
#         flash(
#             "注册成功！请登录",
#             category="success"
#         )
#         return redirect(url_for('.login'))
#     return render_template("main/register.html",form=form)

@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )
    return redirect(url_for('main.login'))



