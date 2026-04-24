import os
import urllib.parse


def get_database_uri() -> str:
    url = os.environ.get("DATABASE_URL")
    if url:
        return url

    db_user = os.environ.get("DB_USER", "root")
    db_pass = os.environ.get("DB_PASS", "root")
    db_name = os.environ.get("DB_NAME", "univ_music")
    db_host = os.environ.get("DB_HOST", "127.0.0.1")
    db_port = os.environ.get("DB_PORT", "3306")
    db_socket = os.environ.get("DB_SOCKET")

    password = urllib.parse.quote_plus(db_pass)
    if db_socket:
        return (
            f"mysql+pymysql://{db_user}:{password}@localhost/{db_name}"
            f"?unix_socket={urllib.parse.quote_plus(db_socket)}"
        )

    return f"mysql+pymysql://{db_user}:{password}@{db_host}:{db_port}/{db_name}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
