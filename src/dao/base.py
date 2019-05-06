import pymysql
from src import config

conn = None


def get_connection():
    global conn
    if conn and conn.open:
        return conn

    conn = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASS,
    )
    return conn


def close_connection():
    if conn and conn.open:
        conn.close()


def write_commit():
    get_connection().commit()


