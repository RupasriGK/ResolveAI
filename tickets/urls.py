
from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("create/", views.create_ticket, name="create_ticket"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
]
