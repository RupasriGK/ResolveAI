
from django.urls import path
from . import views
from tickets import views as ticket_views

app_name = 'dashboard'

urlpatterns = [
    # Employee Dashboard
    path(
        "employee/<uuid:user_uuid>/",
        views.employee_dashboard,
        name="employee_dashboard"
    ),

    # Create Ticket
    path(
        "employee/<uuid:user_uuid>/create-ticket/",
        ticket_views.create_ticket,
        name="create_ticket"
    ),

    # My Tickets
    path(
        "employee/<uuid:user_uuid>/my-tickets/",
        ticket_views.my_tickets,
        name="my_tickets"
    ),

    # Ticket Details
    path(
        "employee/<uuid:user_uuid>/tickets/<uuid:ticket_uuid>/",
        ticket_views.ticket_detail,
        name="ticket_detail"
    ),
]
