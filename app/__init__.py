from flask import Flask # type: ignore
from app.config import Config
from app.models import db

# Crear la app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.users import users_bp
    from app.routes.admin import admin_bp
    from app.routes.defaut import default_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(products_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(default_bp, url_prefix='/')

    return app