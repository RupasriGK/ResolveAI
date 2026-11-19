
from django import forms
from .models import (
    KnowledgeCategory,
    KnowledgeArticle,
    KnowledgeDocument,
)


class KnowledgeCategoryForm(forms.ModelForm):
    class Meta:
        model = KnowledgeCategory
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter category name",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe this category",
                "rows": 3,
            }),
        }


class KnowledgeArticleForm(forms.ModelForm):
    class Meta:
        model = KnowledgeArticle
        fields = [
            "category",
            "title",
            "summary",
            "content",
            "status",
        ]

        widgets = {
            "category": forms.Select(attrs={
                "class": "form-control",
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter article title",
            }),
            "summary": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write a short summary",
                "rows": 3,
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write the complete troubleshooting guide",
                "rows": 10,
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
        }


class KnowledgeDocumentForm(forms.ModelForm):
    class Meta:
        model = KnowledgeDocument
        fields = ["title", "file"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter document title",
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.docx,.txt",
            }),
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if uploaded_file:
            allowed_extensions = [".pdf", ".docx", ".txt"]
            extension = "." + uploaded_file.name.rsplit(".", 1)[-1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, DOCX and TXT files are allowed."
                )

            if uploaded_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must not exceed 10 MB."
                )

        return uploaded_file
