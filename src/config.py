from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    conn_str  = os.getenv("CONN_STR")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    debug = True 
    SQLALCHEMY_DATABASE_URI  = "CONN_STR"