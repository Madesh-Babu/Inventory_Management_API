from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from werkzeug.exceptions import Forbidden,Unauthorized
from app.models import User

def role_required(*roles):
    """Restrict route access to specific roles."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)
                if user.role not in roles:
                    raise Forbidden("Access forbidden: insufficient permissions")
                return fn(*args, **kwargs)
            except Exception as e:
                raise e
        return decorator
    return wrapper

