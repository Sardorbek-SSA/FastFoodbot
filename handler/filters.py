import re

def check_phone(phone: str) -> bool:
    """
    Uzbekistan telefon raqamini tekshiradi.
    To'g'ri format: +998XXXXXXXXX yoki 998XXXXXXXXX
    (jami 12 yoki 13 belgidan iborat bo'ladi).
    """
    pattern = r"^(?:\+998|998)\d{9}$"
    return bool(re.match(pattern, phone))

def check_location(lat: float, lon: float) -> bool:
    return 37 <= lat <= 45 and 55 <= lon <= 73