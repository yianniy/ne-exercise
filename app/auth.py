from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def check_auth(token: str = Security(security)):
  secrets_file = open('.secrets', 'r')
  secrets = secrets_file.read().split("\n")

  if token.credentials in secrets:
    return token
  raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Missing or invalid API key"
  )