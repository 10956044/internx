from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
import os
from dotenv import load_dotenv
from extensions import db, login_manager
from models import User
from flask_migrate import Migrate
from auth import auth
from werkzeug.utils import secure_filename
import uuid

# 載入環境變數
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    
    # 資料庫配置
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 配置上傳文件夾
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # 確保上傳文件夾存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 初始化擴展
    db.init_app(app)
    login_manager.init_app(app)
    
    # 註冊認證藍圖
    app.register_blueprint(auth)

    migrate = Migrate(app, db)

    # 創建資料庫表
    with app.app_context():
        db.create_all()

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # 首頁路由
    @app.route('/')
    def index():
        return render_template('index.html')

    # 找實習頁面
    @app.route('/internships')
    def internships():
        return render_template('internships.html')

    # 職涯諮詢頁面
    @app.route('/consulting')
    def consulting():
        return render_template('consulting.html')

    # 經驗分享頁面
    @app.route('/experience')
    def experience():
        return render_template('experience.html')

    # 個人資料頁面
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    # 更新個人資料
    @app.route('/update_profile', methods=['POST'])
    @login_required
    def update_profile():
        username = request.form.get('username')
        
        if not username:
            flash('用戶名不能為空', 'error')
            return redirect(url_for('profile'))
        
        try:
            current_user.username = username
            db.session.commit()
            flash('個人資料更新成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash('更新失敗，請稍後再試', 'error')
        
        return redirect(url_for('profile'))

    # 更新密碼
    @app.route('/update_password', methods=['POST'])
    @login_required
    def update_password():
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # 驗證目前密碼
        if not current_user.check_password(current_password):
            flash('目前密碼錯誤', 'error')
            return redirect(url_for('profile'))
        
        # 驗證新密碼
        if not new_password:
            flash('新密碼不能為空', 'error')
            return redirect(url_for('profile'))
        
        if new_password != confirm_password:
            flash('兩次輸入的新密碼不一致', 'error')
            return redirect(url_for('profile'))
        
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash('密碼更新成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash('更新失敗，請稍後再試', 'error')
        
        return redirect(url_for('profile'))

    # 更新頭像
    @app.route('/update_avatar', methods=['POST'])
    @login_required
    def update_avatar():
        if 'avatar' not in request.files:
            flash('沒有選擇文件', 'error')
            return redirect(url_for('profile'))
        
        file = request.files['avatar']
        if file.filename == '':
            flash('沒有選擇文件', 'error')
            return redirect(url_for('profile'))
        
        if file and allowed_file(file.filename):
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            # 添加唯一標識符
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            # 保存文件
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            try:
                # 更新用戶頭像路徑
                current_user.image = f"/static/uploads/{unique_filename}"
                db.session.commit()
                flash('頭像更新成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash('更新失敗，請稍後再試', 'error')
        else:
            flash('不支持的文件類型', 'error')
        
        return redirect(url_for('profile'))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 