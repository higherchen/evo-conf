import hashlib
import json
import time
from models import App, AppEnv
from app import app

class Auth:

    __request_data = {}

    def __init__(self, request_data):
        # 验证时间戳参数
        if not 'timestamp' in request_data:
            raise Exception('timestamp can not be empty')

        timestamp = request_data['timestamp']
        if not timestamp.isnumeric():
            raise Exception('timestamp must be a number')

        timestamp = int(timestamp)
        now = int(time.time())
        if timestamp > now + 30 or timestamp < now - 30:
            raise Exception('timestamp is expired')

        # 验证app id
        if not 'app_id' in request_data:
            raise Exception('app_id can not be empty')

        # 验证环境参数
        if not 'env' in request_data:
            raise Exception('env can not be empty')

        # 验证签名参数
        if not 'sign' in request_data:
            raise Exception('sign can not be empty')

        self.__request_data = request_data

    def validate(self):
        request_data = {}
        for key in self.__request_data:
            request_data[key] = self.__request_data[key]

        sign = request_data['sign']
        app_id = request_data['app_id']
        env = request_data['env']
        del request_data['sign']

        sorted_data = sorted(request_data.items(), key=lambda value:value[0])
        query_string = []
        for item in sorted_data:
            query_string.append(item[0] + '=' + item[1])

        # 生成签名
        query_string = '&'.join(query_string)
        accessed_sign = {}

        # 检查应用
        config_app = App.query.filter_by(name = app_id).first()
        if not config_app:
            raise Exception('app not exists')

        # 检查环境
        config_app_env = AppEnv.query.filter_by(app_id = config_app.id, name = env).first()
        if not config_app_env:
            raise Exception('app `' + app_id + '` do not have the env `' + env + '`')

        # 普通token生成的签名
        hl = hashlib.md5()
        hl.update((query_string + config_app_env.token).encode(encoding='utf-8'))
        accessed_sign[hl.hexdigest()] = config_app_env.token

        # 超级token生成的签名
        hl = hashlib.md5()
        hl.update((query_string + app.config['CONSUL_TOKEN']).encode(encoding='utf-8'))
        accessed_sign[hl.hexdigest()] = app.config['CONSUL_TOKEN']

        if not sign in accessed_sign:
            raise Exception('sign error')

        return {
            'app_id': config_app.id,
            'app_name': app_id,
            'env_id': config_app_env.id,
            'env_name': env,
            'token': accessed_sign[sign]
        }
