from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(f"收到註冊請求: username={username}, email={email}")  # 調試信息

        # 檢查密碼是否匹配
        if password != confirm_password:
            flash('密碼不匹配', 'error')
            return redirect(url_for('auth.register'))

        # 檢查郵箱是否已存在
        user = User.query.filter_by(email=email).first()
        if user:
            flash('該電子郵件已被註冊', 'error')
            return redirect(url_for('auth.register'))

        # 生成用戶ID
        user_id = User.generate_user_id()
        print(f"生成的用戶ID: {user_id}")  # 調試信息

        # 創建新用戶
        new_user = User(
            user_id=user_id,
            username=username,
            email=email,
            permission='default user'
        )
        new_user.set_password(password)

        try:
            print("嘗試添加用戶到資料庫...")  # 調試信息
            db.session.add(new_user)
            print("嘗試提交事務...")  # 調試信息
            db.session.commit()
            print("用戶成功添加到資料庫")  # 調試信息
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"註冊失敗，錯誤信息: {str(e)}")  # 調試信息
            db.session.rollback()
            flash('註冊失敗，請稍後再試', 'error')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        print(f"收到登入請求: email={email}")  # 調試信息

        user = User.query.filter_by(email=email).first()

        # 檢查用戶是否存在且密碼是否正確
        if not user or not user.check_password(password):
            flash('電子郵件或密碼錯誤', 'error')
            return redirect(url_for('auth.login'))

        # 登入用戶
        login_user(user, remember=remember)
        print(f"用戶 {user.username} 登入成功")  # 調試信息
        flash('登入成功！歡迎回來', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已成功登出', 'success')
    return redirect(url_for('index')) 