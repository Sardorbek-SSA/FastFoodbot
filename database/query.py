from .connect import get_connect

def is_register(chat_id: int):
    with get_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
            return cur.fetchone()

def save_user(user_id: int, fullname: str, phone: str, lat: float, lon: float):
    with get_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (chat_id, fullname, phone, lat, lon)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (chat_id) DO UPDATE
                SET fullname = EXCLUDED.fullname,
                    phone = EXCLUDED.phone,
                    lat = EXCLUDED.lat,
                    lon = EXCLUDED.lon
                """,
                (user_id, fullname, phone, lat, lon)
            )
            conn.commit()

def get_food_by_name(name: str):
    with get_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM food WHERE lower(name) = %s", (name.lower(),))
            return cur.fetchone()

def get_all_foods():
    with get_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM food")
            return cur.fetchall()
