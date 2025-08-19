from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


class LandlordRequiredMixin(LoginRequiredMixin):
    """
    Mixin that requires the user to be logged in and be a landlord.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.is_landlord:
            messages.error(request, 'Access denied. Landlords only.')
            return redirect('dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class TenantRequiredMixin(LoginRequiredMixin):
    """
    Mixin that requires the user to be logged in and be a tenant.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.is_tenant:
            messages.error(request, 'Access denied. Tenants only.')
            return redirect('dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class UserTypeRequiredMixin(LoginRequiredMixin):
    """
    Mixin that requires the user to be one of the specified user types.
    Set allowed_user_types as a list/tuple in the view class.
    """
    allowed_user_types = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.user_type not in self.allowed_user_types:
            messages.error(
                request, 
                f'Access denied. Only {", ".join(self.allowed_user_types)} allowed.'
            )
            return redirect('dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class AnonymousRequiredMixin:
    """
    Mixin that requires the user to NOT be logged in.
    Useful for login/register views.
    """
    redirect_url = 'dashboard'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)