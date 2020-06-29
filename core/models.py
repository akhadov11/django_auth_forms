from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Department(models.Model):
    """
        class representing Department model
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class User(AbstractBaseUser):
    """
        class representing custom User model
    """
    full_name = models.CharField("full name", max_length=255)
    phone = models.CharField("phone number", max_length=12)
    status = models.BooleanField(
        "is active",
        default=True,
        help_text="Designates whether this user should be treated as active. ",
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.full_name
