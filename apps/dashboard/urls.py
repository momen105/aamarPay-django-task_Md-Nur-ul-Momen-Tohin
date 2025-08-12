from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dasboard'),
    path('api/files/', FileCRUDView.as_view(), name='file-upload'),
    path('api/initiate-payment/', PaymentView.as_view(), name='initiate-payment'),
    path('api/payment/success/', payment_success, name='payment-success'),
    path('payment/fail/', payment_cancel, name='payment-fail'),
    path('payment/cancel/', payment_fail, name='payment-cancel'),

]
