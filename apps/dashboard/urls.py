from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dasboard'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('activity/', ActivityView.as_view(), name='activity-list'),

    path('api/files/', FileCRUDView.as_view(), name='file-list'),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/activity/', ActivityListView.as_view(), name='activity'),
    path('api/initiate-payment/', PaymentView.as_view(), name='initiate-payment'),
    path('api/transactions/', TransactionView.as_view(), name='transactions'),
    path('api/payment/success/', payment_success, name='payment-success'),
    path('payment/fail/', payment_cancel, name='payment-fail'),
    path('payment/cancel/', payment_fail, name='payment-cancel'),

]
