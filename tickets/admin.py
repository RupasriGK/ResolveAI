
from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "uuid",
        "title",
        "category",
        "priority",
        "status",
        "created_by",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "category",
        "created_at",
    )

    search_fields = (
        "id",
        "uuid",
        "title",
        "description",
        "created_by__username",
        "assigned_to__username",
    )

    readonly_fields = (
        "id",
        "uuid",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 20
