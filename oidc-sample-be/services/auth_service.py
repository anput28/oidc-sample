import json
import secrets
import hashlib
import base64

import requests
from jose import jwt
from functools import wraps
from urllib.request import urlopen

from flask import session, current_app
from werkzeug.exceptions import Unauthorized


def generate_code_verifier() -> str:
    code_verifier = secrets.token_urlsafe(32)
    session["code_verifier"] = code_verifier
    return code_verifier


def generate_code_challenge(code_verifier: str) -> tuple[str, str]:
    hashed = hashlib.sha256(code_verifier.encode('ascii')).digest()
    encoded = base64.urlsafe_b64encode(hashed)
    code_challenge = encoded.decode('ascii')[:-1]
    session["code_challenge"] = code_challenge
    return code_challenge, 'S256'


def generate_state() -> str:
    state = secrets.token_urlsafe(64)
    session["state"] = state
    return state


# =========================================================================================
# This function uses refresh token to maintain user authentication when the access token
# is expired
# =========================================================================================
def keep_authenticated():
    refresh_token = session.get("refresh_token")
    if refresh_token is None:
        raise Unauthorized("Token is expired")

    as_token_endpoint = f"{current_app.config['AUTHORITY']}/oauth/token"

    form_data = {
        "grant_type": "refresh_token",
        "client_id": current_app.config['CLIENT_ID'],
        "client_secret": current_app.config['CLIENT_SECRET'],
        "refresh_token": refresh_token,
    }

    as_response = requests.post(as_token_endpoint, data=form_data)
    if as_response.status_code == 403:
        raise Unauthorized("Token is expired")

    session.pop("access_token")
    session.pop("id_token")
    session.pop("expires_in")
    session["access_token"] = as_response.json()["access_token"]
    session["id_token"] = as_response.json()["id_token"]
    session["expires_in"] = as_response.json()["expires_in"]


# =========================================================================================
# This function is a decorator that validate the access token using a JWK.
# =========================================================================================
def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            unverified_token = session.get("access_token")
        except KeyError:
            raise Unauthorized("Access token not found")

        jwks_url = urlopen(f"{current_app.config['AUTHORITY']}/.well-known/jwks.json")
        jwks = json.loads(jwks_url.read())
        unverified_header = jwt.get_unverified_header(unverified_token)

        signing_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                signing_key = key

        if signing_key:
            try:
                jwt.decode(
                    unverified_token,
                    signing_key,
                    algorithms=["RS256"],
                    audience=current_app.config['AUDIENCE'],
                    issuer=f"{current_app.config['AUTHORITY']}/"
                )
            except jwt.ExpiredSignatureError:
                keep_authenticated()
                validate_token(f)
            except jwt.JWTError:
                raise Unauthorized("Unable to validate the token")

            return f(*args, **kwargs)

        raise Unauthorized("Unable to find appropriate key")

    return wrapper
