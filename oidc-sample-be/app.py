from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, InternalServerError

from blueprints.auth import auth
from blueprints.test import test


# =========================================================================================
# This function is a global error handler for HTTPException.
# =========================================================================================
def handle_error(e: HTTPException):
    if isinstance(e, InternalServerError) and e.description is None:
        e.description = "An error occurred while processing the request"

    response = jsonify({
        "description": e.description,
    })
    response.status_code = e.code
    return response


app = Flask(__name__)
app.config.from_pyfile("config.py")

app.register_blueprint(test)
app.register_blueprint(auth)
app.register_error_handler(HTTPException, handle_error)

CORS(app, supports_credentials=True, origins="http://localhost:4200")

if __name__ == "__main__":
    app.run()
