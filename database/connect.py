import psycopg2
from environs import Env


env  = Env()
env.read_env()

def get_connect():
    return psycopg2.connect(
        database = env.str("DBNAME"),
        user = env.str("USER"),
        password = env.str("PASSWORD"),
        host = env.str("HOST"),
        port = 5432
        
    )