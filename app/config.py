from sqlalchemy import create_engine # type: ignore

# Configuración de la base de datos
class Config:
    DATABASE = {
        'drivername': 'mysql+pymysql',
        'host': '',
        'port': '3',
        'username': '',
        'password': '',
        'database': ''
    }

    SQLALCHEMY_DATABASE_URI = f"{DATABASE['drivername']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'a3f5b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5'

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)