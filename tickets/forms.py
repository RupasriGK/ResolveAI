
from django import forms
from .models import Ticket


class TicketCreateForm(forms.ModelForm):

    class Meta:
        model = Ticket

        fields = [
            "title",
            "description",
            "category",
            "priority",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter your issue title",
                "class": "form-control",
            }),

            "description": forms.Textarea(attrs={
                "placeholder": "Describe your technical issue in detail...",
                "class": "form-control",
                "rows": 5,
            }),

            "category": forms.TextInput(attrs={
                "placeholder": "Example: Hardware, Software, Network",
                "class": "form-control",
            }),

            "priority": forms.Select(attrs={
                "class": "form-control",
            }),
        }
