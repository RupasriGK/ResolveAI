
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from tickets.models import Ticket


@login_required
def employee_dashboard(request, user_uuid):

    # Prevent employees from accessing another employee's dashboard
    if request.user.id != user_uuid:
        raise Http404("Dashboard not found")

    employee_tickets = Ticket.objects.filter(
        created_by=request.user
    )

    context = {
        "username": request.user.username,

        "total_tickets": employee_tickets.count(),

        "open_tickets": employee_tickets.filter(
            status=Ticket.Status.OPEN
        ).count(),

        "in_progress_tickets": employee_tickets.filter(
            status=Ticket.Status.IN_PROGRESS
        ).count(),

        "resolved_tickets": employee_tickets.filter(
            status=Ticket.Status.RESOLVED
        ).count(),
    }

    return render(
        request,
        "dashboard/employee_dashboard.html",
        context
    )
