import requests
import time
from flask import Blueprint, request, redirect, session, current_app, jsonify
from services.auth_service import generate_code_verifier, generate_code_challenge, generate_state

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


# =========================================================================================
# This endpoint is used to check whether the user is authenticated.
# The check is based on the expiration date of the access token which is compared to the
# current timestamp.
# =========================================================================================
@auth.get("/is-authenticated")
def check_authentication():
    expires_in = session.get("expires_in")

    is_authenticated = (expires_in is not None) and (time.time() > expires_in)

    resp = jsonify({
        "isAuthenticated": is_authenticated
    })
    resp.status_code = 200
    return resp


# =========================================================================================
# This endpoint is used to contact the Identity Provider /authorize endpoint in order to
# obtain the authorization code, which will be used to get tokens.

# Even if it is not really necessary, it is used the PCKE (Proof Key for Code Exchange,
# https://datatracker.ietf.org/doc/html/rfc7636) in order to prevent CSRF and authorization
# code injection attacks.
# =========================================================================================
@auth.get("/login")
def login():
    # openid = tell the IdP that you intend to use OpenID Connect
    # profile = tell the IdP that you intend to access user personal information (email, ecc.)
    # offline_access = tell the IdP that you intend to use refresh token
    scope = "openid profile offline_access"
    response_type = "code"  # code = tell the IdP that you want the authorization code
    client_id = current_app.config['CLIENT_ID']
    redirect_uri = current_app.config['AUTH_REDIRECT_URI']
    audience = current_app.config['AUDIENCE']
    state = generate_state()
    code_verifier = generate_code_verifier()
    code_challenge, code_challenge_method = generate_code_challenge(code_verifier)

    location = f"{current_app.config['AUTHORITY']}/authorize?" \
               f"audience={audience}&" \
               f"scope={scope}&" \
               f"response_type={response_type}&" \
               f"client_id={client_id}&" \
               f"redirect_uri={redirect_uri}&" \
               f"state={state}&" \
               f"code_challenge={code_challenge}&" \
               f"code_challenge_method={code_challenge_method}"
    resp = redirect(location)
    return resp


# =========================================================================================
# This endpoint is used to contact the Identity Provider /token endpoint, using the
# authorization code obtained earlier to get the tokens.
# Once the tokens are obtained, they are saved in a session cookie and then the endpoint
# performs a redirect to the frontend.
# =========================================================================================
@auth.get("/oauth-callback")
def oauth_callback():
    if request.args["state"] != session["state"]:
        redirect(current_app.config["FE_ENDPOINT"])
        return

    code = request.args.get("code")
    code_verifier = session.get("code_verifier")

    as_token_endpoint = f"{current_app.config['AUTHORITY']}/oauth/token"
    form_data = {
        "grant_type": "authorization_code",
        "client_id": current_app.config['CLIENT_ID'],
        "client_secret": current_app.config['CLIENT_SECRET'],
        "code": code,
        "code_verifier": code_verifier,
        "redirect_uri": current_app.config['AUTH_REDIRECT_URI']
    }

    as_response = requests.post(as_token_endpoint, data=form_data)

    session.clear()
    session["access_token"] = as_response.json()["access_token"]
    session["id_token"] = as_response.json()["id_token"]
    session["refresh_token"] = as_response.json()["refresh_token"]
    session["expires_in"] = as_response.json()["expires_in"]

    return redirect(f"{current_app.config['FE_ENDPOINT']}/dashboard")


@auth.get("/logout")
def logout():
    client_id = current_app.config['CLIENT_ID']
    return_to = current_app.config['FE_ENDPOINT']

    location = f"{current_app.config['AUTHORITY']}/v2/logout?" \
               f"client_id={client_id}&" \
               f"returnTo={return_to}"

    session.clear()
    return redirect(location)
