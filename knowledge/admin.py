
from django.contrib import admin
from .models import KnowledgeCategory, KnowledgeArticle, KnowledgeDocument


@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
        "updated_at",
    )

    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("name",)


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "status",
        "created_by",
        "published_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
        "published_at",
    )

    search_fields = (
        "title",
        "summary",
        "content",
        "category__name",
    )

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "category",
        "created_by",
        "updated_by",
    )

    ordering = ("-updated_at",)
    list_per_page = 20


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "uploaded_by",
        "processing_status",
        "uploaded_at",
        "processed_at",
    )

    list_filter = (
        "processing_status",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "uploaded_by__username",
    )

    readonly_fields = (
        "id",
        "uploaded_at",
        "processed_at",
        "processing_error",
    )

    autocomplete_fields = ("uploaded_by",)

    ordering = ("-uploaded_at",)
    list_per_page = 20
