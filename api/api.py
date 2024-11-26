from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt
from link import *
from api.sql import *

bcrypt = Bcrypt()

api = Blueprint('api', __name__, template_folder='../templates')
login_manager = LoginManager(api)
login_manager.login_view = 'api.login'
login_manager.login_message = "請先登入"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(account):  
    user = User()
    user.id = account
    data = Administrator.get_admin(account)
    try:
        user.account = data[0]
    except:
        pass
    return user

@api.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']

        # 查詢資料
        data = Administrator.get_admin(account)
        if not data:
            flash('*沒有此帳號')
            return redirect(url_for('api.login'))
        
        DB_password = data[1]

        # 驗證密碼
        if bcrypt.check_password_hash(DB_password, password):
            user = User()
            user.id = account
            login_user(user)
            return redirect(url_for('manager.patent_case'))     
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('api.login'))

    return render_template('login.html')

@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('api.login'))