import time
import jwt
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

key = "key"


def encode_token(username):
    if username:
        payload = {
            'exp': datetime.now(tz=timezone.utc) + timedelta(hours=1),
            'iat': datetime.now(tz=timezone.utc),
            'scope': 'access_token',
            'data': username
        }
        return jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )
    else:
        return ValueError("Invaild username")


def decode_token(token):
    return jwt.decode(token, key, algorithms='HS256')
