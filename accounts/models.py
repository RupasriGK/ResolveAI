
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        IT_AGENT = "IT_AGENT", "IT Support Agent"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
