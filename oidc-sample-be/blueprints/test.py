from flask import Blueprint, jsonify

from services.auth_service import validate_token

test = Blueprint('test', __name__, url_prefix='/api/test')


# =========================================================================================
# This API is a private endpoint useful for testing the token validation.
# When a request arrives at this endpoint, the token validation method is called
# in order to handle whether granting the access.
# =========================================================================================
@test.get("/secret")
@validate_token
def secret():
    resp = jsonify({
        "secret": "This is the secret"
    })
    resp.status_code = 200
    return resp
