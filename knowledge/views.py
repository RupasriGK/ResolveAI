
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    KnowledgeCategory,
    KnowledgeArticle,
    KnowledgeDocument,
)
from .forms import (
    KnowledgeCategoryForm,
    KnowledgeArticleForm,
    KnowledgeDocumentForm,
)


# Only IT agents and administrators can manage the Knowledge Base.
def knowledge_manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ["IT_AGENT", "ADMIN"]:
            return HttpResponseForbidden(
                "You do not have permission to manage the Knowledge Base."
            )
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@knowledge_manager_required
def category_list(request):
    categories = KnowledgeCategory.objects.all()

    return render(request, "knowledge/category_list.html", {
        "categories": categories,
    })


@login_required
@knowledge_manager_required
def create_category(request):
    if request.method == "POST":
        form = KnowledgeCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge category created successfully.")
            return redirect("knowledge:category_list")
    else:
        form = KnowledgeCategoryForm()

    return render(request, "knowledge/create_category.html", {
        "form": form,
    })


@login_required
@knowledge_manager_required
def article_list(request):
    articles = KnowledgeArticle.objects.select_related(
        "category", "created_by"
    ).all()

    search_query = request.GET.get("search", "").strip()

    if search_query:
        articles = articles.filter(title__icontains=search_query)

    selected_status = request.GET.get("status", "")

    valid_statuses = [
        choice[0] for choice in KnowledgeArticle.Status.choices
    ]

    if selected_status in valid_statuses:
        articles = articles.filter(status=selected_status)
    else:
        selected_status = ""

    return render(request, "knowledge/article_list.html", {
        "articles": articles,
        "search_query": search_query,
        "selected_status": selected_status,
        "status_choices": KnowledgeArticle.Status.choices,
    })


@login_required
@knowledge_manager_required
def create_article(request):
    if request.method == "POST":
        form = KnowledgeArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user

            if article.status == KnowledgeArticle.Status.PUBLISHED:
                article.published_at = timezone.now()

            article.save()

            messages.success(request, "Knowledge article created successfully.")
            return redirect("knowledge:article_list")
    else:
        form = KnowledgeArticleForm()

    return render(request, "knowledge/create_article.html", {
        "form": form,
    })


@login_required
@knowledge_manager_required
def edit_article(request, article_id):
    article = get_object_or_404(KnowledgeArticle, id=article_id)

    if request.method == "POST":
        form = KnowledgeArticleForm(request.POST, instance=article)

        if form.is_valid():
            updated_article = form.save(commit=False)
            updated_article.updated_by = request.user

            if (
                updated_article.status == KnowledgeArticle.Status.PUBLISHED
                and not updated_article.published_at
            ):
                updated_article.published_at = timezone.now()

            updated_article.save()

            messages.success(request, "Knowledge article updated successfully.")
            return redirect("knowledge:article_list")
    else:
        form = KnowledgeArticleForm(instance=article)

    return render(request, "knowledge/edit_article.html", {
        "form": form,
        "article": article,
    })


@login_required
@knowledge_manager_required
def document_list(request):
    documents = KnowledgeDocument.objects.select_related(
        "uploaded_by"
    ).all()

    return render(request, "knowledge/document_list.html", {
        "documents": documents,
    })


@login_required
@knowledge_manager_required
def upload_document(request):
    if request.method == "POST":
        form = KnowledgeDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()

            messages.success(
                request,
                "Knowledge document uploaded successfully."
            )
            return redirect("knowledge:document_list")
    else:
        form = KnowledgeDocumentForm()

    return render(request, "knowledge/upload_document.html", {
        "form": form,
    })
