from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") # Cambia esto a un valor seguro
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = 30 #os.getenv(ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE = 7 #os.getenv(REFRESH_TOKEN_EXPIRE_DAYS)

# Validar el token de acceso
def verify_token(token: str, credentials_exception=HTTPException(status_code=401, detail="No autorizado", headers={"WWW-Authenticate":
"Bearer"})):
    """
    Verifica el token de acceso.
    Args:
        token (str): Token de acceso.
    Returns:
        Token: Datos del token decodificados.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = Token(**payload)
    except JWTError:
        raise credentials_exception
    return token_data

# Decodificar el token de acceso 
def decode_access_token(token: str):
    """
    Decodifica el token de acceso.
    Args:
        token (str): Token de acceso.
    Returns:
        dict: Datos del token decodificados.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #print(f"Decode_Access_Token:Payload decodificado: {payload}") # Debug
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Decodificar el token de acceso 
def decode_refresh_token(token: str):
    """
    Decodifica el token de acceso.
    Args:
        token (str): Token de acceso.
    Returns:
        dict: Datos del token decodificados.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #print(f"Decode_Access_Token:Payload decodificado: {payload}") # Debug
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Generar un token de acceso
def create_access_token(data: dict, expires_delta: int = None, description="Generar un token JWT con los datos del usuario y una fecha de expiración opcional."):
    """
    Genera un access token con expiración corta.
    Args:
        data (dict): Datos del usuario a codificar en el token.
        expires_delta (int): Tiempo de expiración del token.
    Return:
        El token JWT codificado.
    """
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    else:
        expires_delta = timedelta(minutes=expires_delta)

    expire = datetime.now(timezone.utc) + (expires_delta)
    # Se añade el tipo de token para distinguirlo en el refresh endpoint
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, description="Generar un refresh token con expiración larga."):
    """
    Genera un refresh token con expiración larga.
    Args:
        data (dict): Datos del usuario a codificar en el token.
    Return:
        El token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (timedelta(days=REFRESH_TOKEN_EXPIRE))
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
