from functools import wraps
from django.core.exceptions import PermissionDenied

def requires_role(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_role(role):
                raise PermissionDenied("You don't have enough privileges to perform this action.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



