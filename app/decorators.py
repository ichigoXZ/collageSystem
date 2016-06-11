from functools import wraps
from flask import abort
from flask.ext.login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(0)(f)

def teacher_required(f):
	return permission_required(1)(f)

def student_required(f):
	return permission_required(2)(f)