
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path(
        "employee/<uuid:user_uuid>/",
        views.employee_dashboard,
        name='employee_dashboard'
    ),
]
