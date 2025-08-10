from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dasboard'),
    path('api/files/', FileCRUDView.as_view(), name='file-upload'),

]
