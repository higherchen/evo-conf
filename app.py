from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from service.auth import Auth
from service.config_app import ConfigApp

@app.errorhandler(404)
def not_found(error):
    return 'page not found', 404

# 获取应用指定环境下的所有namespace相关信息
@app.route('/api/namespaces', methods=['GET'])
def app_env():
    try:
        # 请求验证
        auth = Auth(request.args)
        config_app = auth.validate()
        app_service = ConfigApp(app.config['CONSUL_SITE'], config_app)
        ret = app_service.app()
        namespaces = []
        for item in ret:
            namespaces.append({
                'name': item.name,
                'src': item.src,
                'target': item.target
            })
        return jsonify(code = 1, data = namespaces)
    except Exception as err:
        return jsonify(code = 403, msg = format(err))
    else:
        return jsonify(code = 1, msg = 'ok')

@app.route('/api/namespace', methods=['GET'])
def namespace():
    try:
        auth = Auth(request.args)
        config_app = auth.validate()
        app_service = ConfigApp(app.config['CONSUL_SITE'], config_app)
        return jsonify(
            code = 1,
            data = app_service.namespace(request.args.get('namespace'))
        )
    except Exception as err:
        return jsonify(code = 403, msg = format(err))
    else:
        return jsonify(code = 1, msg = 'ok')

@app.route('/api/key', methods=['GET'])
def keys():
    try:
        auth = Auth(request.args)
        config_app = auth.validate()
        app_service = ConfigApp(app.config['CONSUL_SITE'], config_app)
        return jsonify(
            code = 1,
            data = app_service.key(
                request.args.get('namespace'),
                request.args.get('key')
            )
        )
    except Exception as err:
        return jsonify(code = 403, msg = format(err))
    else:
        return jsonify(code = 1, msg = 'ok')
