from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import User


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        department = request.POST.get("department", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        errors = []

        if not username or len(username) < 3 or len(username) > 150:
            errors.append("Username must be between 3 and 150 characters.")
        elif User.objects.filter(username__iexact=username).exists():
            errors.append("Username already exists.")

        try:
            validate_email(email)
        except ValidationError:
            errors.append("Enter a valid email address.")

        if email and User.objects.filter(email__iexact=email).exists():
            errors.append("An account with this email already exists.")

        allowed_departments = {"IT", "HR", "Finance", "Marketing", "Sales", "Operations", "Other"}
        if department not in allowed_departments:
            errors.append("Select a valid department.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        candidate = User(username=username, email=email, department=department)
        try:
            validate_password(password, candidate)
        except ValidationError as exc:
            errors.extend(exc.messages)

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "accounts/register.html", {
                "form_data": {
                    "username": username,
                    "email": email,
                    "department": department,
                }
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            department=department,
            role=User.Role.EMPLOYEE
        )

        messages.success(request, "Account created successfully. Please sign in.")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == User.Role.EMPLOYEE:
                return redirect("dashboard:employee_dashboard",user_uuid=request.user.id)
            if user.role == User.Role.IT_AGENT:
                return redirect("agent_dashboard")
            if user.role == User.Role.ADMIN:
                return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("login")


def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')