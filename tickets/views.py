
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import Http404

from .models import Ticket
from .forms import TicketCreateForm

from django.shortcuts import get_object_or_404


@login_required
def create_ticket(request, user_uuid):

    # Validate employee UUID
    if request.user.id != user_uuid:
        raise Http404("Page not found")

    if request.method == "POST":
        form = TicketCreateForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            messages.success(
                request,
                "Your support ticket has been created successfully!"
            )

            return redirect(
                "dashboard:employee_dashboard",
                user_uuid=request.user.id
            )

    else:
        form = TicketCreateForm()

    return render(
        request,
        "tickets/create_ticket.html",
        {"form": form}
    )


@login_required
def my_tickets(request, user_uuid):

    # Validate employee UUID
    if request.user.id != user_uuid:
        raise Http404("Page not found")

    # Fetch only tickets created by the logged-in employee
    tickets = Ticket.objects.filter(
        created_by=request.user
    ).order_by("-created_at")

    # Search by ticket title or category
    search_query = request.GET.get("search", "").strip()

    if search_query:
        tickets = tickets.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    # Filter by ticket status
    selected_status = request.GET.get("status", "")

    valid_statuses = [
        choice[0] for choice in Ticket.Status.choices
    ]

    if selected_status in valid_statuses:
        tickets = tickets.filter(status=selected_status)
    else:
        selected_status = ""

    context = {
        "tickets": tickets,
        "search_query": search_query,
        "selected_status": selected_status,
    }

    return render(
        request,
        "tickets/my_tickets.html",
        context
    )

@login_required
def ticket_detail(request, user_uuid, ticket_uuid):

    # Verify that the logged-in employee owns this URL
    if request.user.id != user_uuid:
        raise Http404("Page not found")

    # Retrieve only this employee's ticket
    ticket = get_object_or_404(
        Ticket,
        uuid=ticket_uuid,
        created_by=request.user
    )

    context = {
        "ticket": ticket,
    }

    return render(
        request,
        "tickets/ticket_detail.html",
        context
    )
