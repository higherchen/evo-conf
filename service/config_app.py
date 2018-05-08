import base64
import json
import urllib.request
from models import AppNamespace

class ConfigApp:

    __site = {}
    __app = {}

    def __init__(self, site, app):
        self.__site = site
        self.__app = app

    def app(self):
        app = self.__app
        return AppNamespace.query.filter_by(app_id = app['app_id'], env_id = app['env_id']).all()

    def namespace(self, name):
        app = self.__app

        namespace = AppNamespace.query.filter_by(app_id = app['app_id'], env_id = app['env_id'], name = name).first()
        if not namespace:
            raise Exception('namespace not exists')

        # 生成namespace key
        keys_url = self.__site + '/v1/kv/' + '/'.join([app['env_name'], app['app_name'], name, '']) + "?keys&token=" + app['token']
        req = urllib.request.Request(keys_url)
        data = urllib.request.urlopen(req)
        keys = json.loads(data.read())

        # 获取键值
        items = {}
        for key in keys:
            url = self.__site + '/v1/kv/' + key + "?token=" + app['token']
            req = urllib.request.Request(url)
            data = urllib.request.urlopen(req)
            ret = json.loads(data.read())
            items[key.split('/').pop()] = base64.b64decode(ret[0]['Value']).decode()

        return {
            'configs': items,
            'namespace': {
                'src': namespace.src,
                'target': namespace.target
            }
        }

    def key(self, name, key):
        app = self.__app

        namespace = AppNamespace.query.filter_by(app_id = app['app_id'], env_id = app['env_id'], name = name).first()
        if not namespace:
            raise Exception('namespace not exists')

        url = self.__site + '/v1/kv/' + '/'.join([app['env_name'], app['app_name'], name, key]) + "?token=" + app['token']
        req = urllib.request.Request(url)
        data = urllib.request.urlopen(req)
        ret = json.loads(data.read())

        return base64.b64decode(ret[0]['Value']).decode()
