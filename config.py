SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/conf?charset=utf8'
SQLALCHEMY_POOL_RECYCLE = 600
SQLALCHEMY_TRACK_MODIFICATIONS = False
CONSUL_SITE = 'http://127.0.0.1:8500' # consul服务地址
CONSUL_TOKEN = '3d9d58e6' # 设置一个随机字符串作为管理令牌