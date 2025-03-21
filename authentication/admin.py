from authentication.models import *
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserAdmin(UserAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('email', 'username',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal Info', {'fields': ('username',
         'last_login', 'date_joined', 'profile_picture',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser',  'is_verified', 'is_blocked', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'profile_picture'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login',)
    search_fields = ('email', 'username',)
    ordering = ('-id',)


admin.site.register(User, UserAdmin)

admin.site.register(OTPVerification)
admin.site.register(PasswordReset)
