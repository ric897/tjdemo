from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, CustomLoginForm, UserProfileForm, UserUpdateForm
from .models import User, UserProfile
from .mixins import AnonymousRequiredMixin, TenantRequiredMixin
from .decorators import tenant_required


class CustomLoginView(AnonymousRequiredMixin, LoginView):
    form_class = CustomLoginForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().first_name}!')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_landlord:
            return reverse_lazy('dashboard')
        elif user.is_tenant:
            return reverse_lazy('tenant_dashboard')
        return reverse_lazy('dashboard')


class RegisterView(AnonymousRequiredMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Registration successful! You can now log in with your credentials.'
        )
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            context['profile'] = self.request.user.profile
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist
            context['profile'] = UserProfile.objects.create(user=self.request.user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'authentication/profile_update.html'
    success_url = reverse_lazy('auth:profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = UserProfileForm(
                self.request.POST, 
                instance=self.request.user.profile
            )
        else:
            try:
                context['profile_form'] = UserProfileForm(
                    instance=self.request.user.profile
                )
            except UserProfile.DoesNotExist:
                # Create profile if it doesn't exist
                profile = UserProfile.objects.create(user=self.request.user)
                context['profile_form'] = UserProfileForm(instance=profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        
        if profile_form.is_valid():
            self.object = form.save()
            profile_form.instance = self.object.profile
            profile_form.save()
            messages.success(self.request, 'Your profile has been updated successfully!')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


def logout_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been logged out successfully.')
    logout(request)
    return redirect('auth:login')


# Dashboard views (temporary placeholders)
@login_required
def dashboard_view(request):
    context = {
        'user': request.user,
        'user_type': request.user.get_user_type_display()
    }
    return render(request, 'dashboard/dashboard.html', context)


@tenant_required
def tenant_dashboard_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/tenant_dashboard.html', context)
