import os
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url

from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

DEFAULT_DATABASE_URI = "mysql+pymysql://root:password@127.0.0.1:3306/univ_music"


def is_mysql_uri(database_uri):
    return database_uri.startswith("mysql://") or database_uri.startswith("mysql+pymysql://") or database_uri.startswith("mariadb://")


def ensure_database_exists(database_uri):
    """Crée la base de données MariaDB si elle n'existe pas encore."""
    url = make_url(database_uri)
    if not url.database:
        return

    database_name = url.database
    url = url.set(database=None)
    engine = create_engine(url)
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
    engine.dispose()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    database_uri = app.config["SQLALCHEMY_DATABASE_URI"]

    if is_mysql_uri(database_uri):
        try:
            ensure_database_exists(database_uri)
        except Exception:
            print("[ERROR] MariaDB est inaccessible. Vérifie DATABASE_URL ou les variables DB_...")
            raise

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.routes import main_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    login_manager.login_view = "main.login"
    login_manager.login_message_category = "warning"
    login_manager.login_message = "Veuillez vous connecter pour accéder à l’administration."

    with app.app_context():
        from app.models import seed_data

        db.create_all()
        seed_data()

    return app
