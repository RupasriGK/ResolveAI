
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

from knowledge.services.retriever import retrieve_relevant_chunks
from knowledge.services.answer_generator import generate_answer

from django.db import transaction
from support.models import Conversation, Message, ConversationFeedback

from knowledge.services.document_processor import process_knowledge_document

from django.views.decorators.http import require_POST

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

            try:
                # Process the uploaded document using the RAG pipeline.
                result = process_knowledge_document(document.id)

                messages.success(
                    request,
                    f"Document processed successfully! "
                    f"{result['total_chunks']} chunks stored in the AI Knowledge Base."
                )

            except Exception:
                messages.error(
                    request,
                    "Document uploaded, but processing failed. "
                    "Please check the processing error."
                )

            return redirect("knowledge:document_list")

    else:
        form = KnowledgeDocumentForm()

    return render(request, "knowledge/upload_document.html", {
        "form": form,
    })

@login_required
def ai_assistant(request):
    """
    AI Assistant with persistent, context-aware conversations.
    """

    if request.user.role not in ["EMPLOYEE", "IT_AGENT", "ADMIN"]:
        return HttpResponseForbidden(
            "You do not have permission to access the AI Assistant."
        )

    if request.method == "POST":

        question = request.POST.get("question", "").strip()
        conversation_id = request.POST.get("conversation_id", "").strip()

        if not question:
            messages.error(request, "Please enter your IT-related question.")
            return redirect("knowledge:ai_assistant")

        conversation = None

        # Retrieve an existing conversation belonging to this user.
        if conversation_id:
            conversation = get_object_or_404(
                Conversation,
                id=conversation_id,
                employee=request.user,
                status=Conversation.Status.ACTIVE
            )

        try:
            # Retrieve previous conversation messages BEFORE saving
            # the current question.
            conversation_history = []

            if conversation:
                conversation_history = list(
                    conversation.messages
                    .order_by("-created_at")
                    .values("role", "content")[:10]
                )

                # Restore chronological order.
                conversation_history.reverse()

            # Retrieve relevant Knowledge Base chunks.
            retrieved_chunks = retrieve_relevant_chunks(
                question=question,
                top_k=5,
                conversation_history=conversation_history
            )

            # Generate an answer using previous conversation context.
            answer = generate_answer(
                question=question,
                retrieved_chunks=retrieved_chunks,
                conversation_history=conversation_history
            )

            # Save conversation and messages.
            with transaction.atomic():

                if conversation is None:
                    conversation = Conversation.objects.create(
                        employee=request.user,
                        title=question[:200]
                    )

                Message.objects.create(
                    conversation=conversation,
                    role=Message.Role.EMPLOYEE,
                    content=question
                )

                Message.objects.create(
                    conversation=conversation,
                    role=Message.Role.AI,
                    content=answer
                )

                conversation.save(update_fields=["updated_at"])

            # Display complete conversation history.
            return render(
                request,
                "knowledge/ai_assistant.html",
                {
                    "question": question,
                    "answer": answer,
                    "sources": retrieved_chunks,
                    "conversation": conversation,
                    "conversation_id": str(conversation.id),
                    "chat_messages": conversation.messages.all(),
                }
            )

        except Exception:
            messages.error(
                request,
                "Unable to generate a response right now. Please try again."
            )

    return render(request, "knowledge/ai_assistant.html")



@login_required
@require_POST
def submit_conversation_feedback(request, conversation_id):

    if request.user.role != "EMPLOYEE":
        return HttpResponseForbidden(
            "Only employees can submit conversation feedback."
        )

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        employee=request.user,
        status=Conversation.Status.ACTIVE
    )

    feedback_value = request.POST.get("feedback", "").strip()

    valid_feedback = [
        ConversationFeedback.FeedbackType.HELPFUL,
        ConversationFeedback.FeedbackType.NOT_HELPFUL,
    ]

    if feedback_value not in valid_feedback:
        messages.error(request, "Invalid feedback selection.")
        return redirect("knowledge:ai_assistant")

    if ConversationFeedback.objects.filter(
        conversation=conversation
    ).exists():
        messages.info(request, "Feedback has already been submitted.")
    else:
        try:
            with transaction.atomic():

                ConversationFeedback.objects.create(
                    conversation=conversation,
                    employee=request.user,
                    feedback=feedback_value,
                    comments=request.POST.get("comments", "").strip()
                )

                if feedback_value == ConversationFeedback.FeedbackType.HELPFUL:
                    conversation.status = Conversation.Status.RESOLVED
                    conversation.save(
                        update_fields=["status", "updated_at"]
                    )

            if feedback_value == ConversationFeedback.FeedbackType.HELPFUL:
                messages.success(
                    request,
                    "Thank you! Your issue has been marked as resolved."
                )
            else:
                messages.success(
                    request,
                    "Thank you for your feedback. You can request human support."
                )

        except Exception:
            messages.error(
                request,
                "Unable to save your feedback. Please try again."
            )

    # Always return the conversation page.
    latest_employee_message = conversation.messages.filter(
        role=Message.Role.EMPLOYEE
    ).last()

    return render(
        request,
        "knowledge/ai_assistant.html",
        {
            "question": (
                latest_employee_message.content
                if latest_employee_message else ""
            ),
            "conversation": conversation,
            "conversation_id": str(conversation.id),
            "chat_messages": conversation.messages.all(),
            "feedback_submitted": ConversationFeedback.objects.filter(
                conversation=conversation
            ).exists(),
            "feedback_value": feedback_value,
            "show_escalation_prompt": (
                feedback_value ==
                ConversationFeedback.FeedbackType.NOT_HELPFUL
            ),
        }
    )
