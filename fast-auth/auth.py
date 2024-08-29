import time
import jwt
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer


key = "key"
TOKEN_PREFIX = "Barerer "

def encode_token(username):
    if username:
        payload = {
            'exp': datetime.now(tz=timezone.utc) + timedelta(hours=1),
            'iat': datetime.now(tz=timezone.utc),
            'scope': 'access_token',
            'data': username
        }
        return TOKEN_PREFIX + jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )
    else:
        return ValueError("Invaild username")


def decode_token(barerer_token: str):
    token = barerer_token.split(" ")[-1]
    return jwt.decode(token.encode(), key, algorithms='HS256')

# {'exp': 1724933846, 'iat': 1724930246, 'scope': 'access_token', 'data': 'hoon'}
def is_valid_token(barerer_token) -> bool:
    decoded = decode_token(barerer_token)
    if time.time() >= decoded["exp"]:  #time.time은 항상 utc
        return False
    return True