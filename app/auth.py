"""
This file contains the functions for password hashing and verification.
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Create a new CryptContext object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verifies a password against a hash.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Generates a hash for a password.

    Args:
        password (str): The password to hash.
    """
    return pwd_context.hash(password)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates an access token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta): The time delta for the token's expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verifies an access token.

    Args:
        token (str): The access token to verify.
        credentials_exception:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data
