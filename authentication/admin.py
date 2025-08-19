from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('User Type & Profile', {
            'fields': ('user_type', 'phone_number', 'profile_picture')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Type & Profile', {
            'fields': ('user_type', 'phone_number')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'zip_code')
    list_filter = ('state', 'city')
    search_fields = ('user__username', 'user__email', 'address', 'city')
    ordering = ('user__username',)
