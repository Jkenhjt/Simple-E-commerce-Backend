import bcrypt


def gen_secured(data: str) -> bytes:
    return bcrypt.hashpw(data.encode(), bcrypt.gensalt(15))
