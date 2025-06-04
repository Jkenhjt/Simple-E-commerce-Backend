from authlib.jose import jwt

key: str = """
30d27a1df78b0fc4fc4e97ee357abf61
01b350ddbaaf7ae0d07519627ffbc436
1e770c618cbaaf92445bc0ad78fbc6dd
70e1f99db7f9d39d72aab2c47e5c89bd
c26055f1dd34510290fd8aa2307ae9fc
340bba236cad53113ed5f93a09de5ba8
b1d0e40aff615c3cabb9ae2ba6463a6b
fb420480425aa17126aca27897659c12
9a079db1f31206423c7fcd4e4f1596f3
08fe0475e61c42d8aec48e2605293154
9adfb6f60d00aaf8cc51d1268795c57d
4e1d5704bf104c8cf5204e37b6792c8c
da2e9925979136d6e1b6de123f473a25
6b28493a18754e9f93c996127a0b670b
cfda5dc946cdd112cb00d759770101e8
b8aeea0a9367cd09b521836568967df9
"""


def gen_jwt(id: int, username: str, key: str = key) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"name": username, "sub": id, "exp": -1}

    return jwt.encode(header, payload, key, check=True).decode()
