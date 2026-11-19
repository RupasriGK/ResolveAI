
from django.urls import path
from . import views

app_name = "knowledge"

urlpatterns = [
    # Category management
    path(
        "categories/",
        views.category_list,
        name="category_list"
    ),
    path(
        "categories/create/",
        views.create_category,
        name="create_category"
    ),

    # Article management
    path(
        "articles/",
        views.article_list,
        name="article_list"
    ),
    path(
        "articles/create/",
        views.create_article,
        name="create_article"
    ),
    path(
        "articles/<uuid:article_id>/edit/",
        views.edit_article,
        name="edit_article"
    ),

    # Document management
    path(
        "documents/",
        views.document_list,
        name="document_list"
    ),
    path(
        "documents/upload/",
        views.upload_document,
        name="upload_document"
    ),
]
