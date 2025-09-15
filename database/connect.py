import psycopg2
from psycopg2.extras import RealDictCursor
from environs import Env

env = Env()
env.read_env()

def get_connect():
    return psycopg2.connect(
        dbname=env.str("DBNAME"),
        user=env.str("USER"),
        password=env.str("PASSWORD"),
        host=env.str("HOST"),
        port=env.str("PORT", 5432),
        cursor_factory=RealDictCursor
    )