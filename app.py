from flask import Flask, request, jsonify, render_template, session, redirect, url_for, g
from models import db, User, LoginLogoutLog
from logging_config import http_logger, login_logger, logout_logger
import base64
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# MySQL 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123123445@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 创建数据库和表
with app.app_context():
    db.create_all()

# 添加示例用户
def add_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

with app.app_context():
    if not User.query.filter_by(username='adm').first():
        add_user('adm', 'admin123')
    if not User.query.filter_by(username='root').first():
        add_user('root', '1234')

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path == '/favicon.ico' or request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    method = request.method
    path = request.path
    status = response.status_code
    username = session.get('username', 'Anonymous')
    log_params = {
        'remote_ip': ip,
        'request_method': method,
        'request_path': path,
        'status_code': status,
        'response_time': duration,
        'username': username
    }
    http_logger.info('', extra=log_params)
    return response

@app.route("/")
@app.route("/index")
def index():
    if 'username' in session:
        return "Hello, " + session['username'] + "!"
    return redirect(url_for('login_page'))

@app.route('/auth', methods=['GET'])
def auth():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({"error": "Unauthorized1"}), 401
    try:
        auth_type, credentials = auth.split(None, 1)
        decoded_credentials = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
    except Exception as e:
        return jsonify({"error": "Unauthorized2"}), 401

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return jsonify({"message": "OK"}), 200
    else:
        return jsonify({"error": "Unauthorized3"}), 401

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            event = 'login'
            status = 'success'
            db.session.add(LoginLogoutLog(event=event, username=username, password=password, status=status))
            db.session.commit()
            login_logger.info('', extra={'event': event, 'username': username, 'password': password, 'status': status})
            return redirect(url_for('index'))
        else:
            event = 'login'
            status = 'failure'
            db.session.add(LoginLogoutLog(event=event, username=username, password=password, status=status))
            db.session.commit()
            login_logger.info('', extra={'event': event, 'username': username, 'password': password, 'status': status})
            return render_template("login.html", error="Incorrect username or password.")
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    username = session.get('username')
    if username:
        event = 'logout'
        status = 'success'
        db.session.add(LoginLogoutLog(event=event, username=username, password='', status=status))
        db.session.commit()
        logout_logger.info('', extra={'event': event, 'username': username, 'status': status})
        session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
