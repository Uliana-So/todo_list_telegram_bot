import secrets


def generate_id():
    """Генерация уникального PK"""
    return secrets.token_hex(4)
