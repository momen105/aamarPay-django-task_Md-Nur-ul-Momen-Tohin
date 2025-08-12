from django.contrib import admin
from .models import PaymentTransaction, ActivityLog, FileUpload

class BaseAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(BaseAdmin):
    pass

@admin.register(ActivityLog)
class ActivityLogAdmin(BaseAdmin):
    pass

@admin.register(FileUpload)
class FileUploadAdmin(BaseAdmin):
    pass
