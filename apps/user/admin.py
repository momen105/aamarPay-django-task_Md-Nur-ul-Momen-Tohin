from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserModel

@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    ordering = ['-id']
    list_display = ['id', 'email', 'name','is_paid_user', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'name']
    readonly_fields = ['last_login']
    
    fieldsets = (
        (None, {'fields': ('email', 'password','is_paid_user')}),
        (_('Personal Info'), {'fields': ('name', 'mobile_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
