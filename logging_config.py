import logging
from logging.handlers import RotatingFileHandler

# 配置HTTP请求日志
http_logger = logging.getLogger('http_logger')
http_logger.setLevel(logging.INFO)
http_handler = RotatingFileHandler('server.log', maxBytes=10000000, backupCount=5)
http_handler.setFormatter(logging.Formatter('%(asctime)s - %(remote_ip)s - %(request_method)s - %(request_path)s - %(status_code)s - %(response_time)s - %(username)s'))
http_logger.addHandler(http_handler)

# 配置登录登出日志
login_logger = logging.getLogger('login_logger')
login_logger.setLevel(logging.INFO)
login_handler = RotatingFileHandler('login.log', maxBytes=10000000, backupCount=5)
login_handler.setFormatter(logging.Formatter('%(asctime)s - %(event)s - %(username)s - %(password)s - %(status)s'))
login_logger.addHandler(login_handler)

logout_logger = logging.getLogger('logout_logger')
logout_logger.setLevel(logging.INFO)
logout_handler = RotatingFileHandler('logout.log', maxBytes=10000000, backupCount=5)
logout_handler.setFormatter(logging.Formatter('%(asctime)s - %(event)s - %(username)s - %(status)s'))
logout_logger.addHandler(logout_handler)
