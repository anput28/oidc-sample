from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
AUTHORITY = getenv("AUTHORITY")
AUDIENCE = getenv("AUDIENCE")
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
AUTH_REDIRECT_URI = "http://localhost:5000/api/auth/oauth-callback"
FE_ENDPOINT = "http://localhost:4200"
