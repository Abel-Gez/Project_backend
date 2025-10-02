# accounts/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class StaffUserManager(BaseUserManager):
    """
    Custom manager for StaffUser.
    """

    def create_user(self, username: str, email: str, role: str, password: str, **extra_fields):
        if not username:
            raise ValueError("The username field is required")
        if not email:
            raise ValueError("The email field is required")
        if not role:
            raise ValueError("The role field is required")
        if not password:
            raise ValueError("The password field is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)  # password is always required now
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: str, password: str, **extra_fields):
        """
        Create and return a superuser. Role is forced to ADMIN.
        """
        if not password:
            raise ValueError("Superuser must have a password")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        role = extra_fields.pop("role", None) or StaffUser.Role.ADMIN

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, role=role, password=password, **extra_fields)


class StaffUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for staff accounts.
    """

    class Role(models.TextChoices):
        MARKETING = "MARKETING", "Marketing"
        HR = "HR", "Human Resources"
        FINANCE = "FINANCE", "Finance"
        ADMIN = "ADMIN", "Admin"

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # required by Django admin
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

    objects = StaffUserManager()

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

    def get_full_name(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Staff User"
        verbose_name_plural = "Staff Users"
        ordering = ["username"]
