from app import db

class App(db.Model):
    __tablename__ = 'config_app'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=True)
    state = db.Column(db.Integer)

class AppEnv(db.Model):
    __tablename__ = 'config_app_env'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(16), nullable=True)
    token = db.Column(db.String(40), nullable=True)
    __table_args__ = (
        db.UniqueConstraint('app_id', 'name', name='ux_config_app_env_1'),
    )

class AppNamespace(db.Model):
    __tablename__ = 'config_namespace'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=True)
    app_id = db.Column(db.Integer, nullable=True)
    env_id = db.Column(db.Integer, nullable=True)
    src = db.Column(db.String(128), nullable=True, default='')
    target = db.Column(db.String(128), nullable=True, default='')
    __table_args__ = (
        db.UniqueConstraint('name', 'app_id', 'env_id', name='ux_config_namespace_1'),
    )
