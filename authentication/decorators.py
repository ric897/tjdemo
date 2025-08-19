from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def landlord_required(view_func):
    """
    Decorator that requires the user to be logged in and be a landlord.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_landlord:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Access denied. Landlords only.')
            return redirect('dashboard')
    return _wrapped_view


def tenant_required(view_func):
    """
    Decorator that requires the user to be logged in and be a tenant.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_tenant:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Access denied. Tenants only.')
            return redirect('dashboard')
    return _wrapped_view


def user_type_required(*user_types):
    """
    Decorator that requires the user to be one of the specified user types.
    Usage: @user_type_required('landlord', 'tenant')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type in user_types:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Access denied. Only {", ".join(user_types)} allowed.')
                return redirect('dashboard')
        return _wrapped_view
    return decorator


def anonymous_required(redirect_url='dashboard'):
    """
    Decorator that requires the user to NOT be logged in.
    Useful for login/register pages.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator