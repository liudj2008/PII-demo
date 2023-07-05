import json
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {
                "message": "Authorization Token is missing!",
                "error": "Unauthorized"
            }, 401
        try:
            with open('Constants/ValidUserId', 'r') as file:
                valid_users = json.load(file)

            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data.get('user_id')
            is_valid_user = current_user in valid_users['validUserId']

            if current_user is None:
                return {
                    "message": "Invalid Authorization token!",
                    "error": "Unauthorized"
                }, 401
            if not is_valid_user:
                abort(403)
        except Exception as e:
            return {
                "message": "Internal Server Error",
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated
