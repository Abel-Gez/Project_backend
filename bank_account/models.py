from django.db import models
from django.conf import settings

# Branchs are preloaded rows used for dropdowns.
class Branch(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

# Profile linking an existing User to a branch + role flag.
class BranchManagerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='branch_profile')
    is_branch_manager = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL, related_name='managers')

    def __str__(self):
        return f"{self.user.username} - manager@{self.branch.name if self.branch else 'unassigned'}"

# Account application from your frontend form.
class AccountApplication(models.Model):
    ACCOUNT_TYPES = [
        ("wadia", "Wadia Account"),
        ("mudarabah", "Mudarabah Account"),
        ("qard", "Qard"),
        ("haji_saving", "Haji Saving Account"),
        ("foreign_currency", "Foreign Currency Account"),
    ]

    # Personal & required fields (from your HTML)
    full_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    nationality = models.CharField(max_length=120)
    fayda_number = models.CharField(max_length=120)
    national_id_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='applications')

    # workflow fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='pending')  # pending/approved/rejected
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='assigned_account_applications')  # optional staff processing

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.branch.name}) - {self.account_type}"
