
from django.contrib import admin
from .models import Conversation, Message, ConversationFeedback


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("id", "created_at")
    fields = ("id", "role", "content", "created_at")
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "employee", "title", "status",
        "ticket", "created_at", "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = (
        "employee__username", "employee__email", "title", "id",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = [MessageInline]
    ordering = ("-updated_at",)
    list_per_page = 25


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role", "created_at")
    list_filter = ("role", "created_at")
    search_fields = (
        "content",
        "conversation__title",
        "conversation__employee__username",
    )
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at",)
    list_per_page = 25


@admin.register(ConversationFeedback)
class ConversationFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id", "conversation", "employee", "feedback", "created_at",
    )
    list_filter = ("feedback", "created_at")
    search_fields = (
        "employee__username",
        "employee__email",
        "conversation__title",
        "comments",
        "id",
    )
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at",)
    list_per_page = 25
