from django.db import models

# Gender choices
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class Vacancy(models.Model):
    """
    Represents a job post/position that HR can manage.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[('full-time','Full-time'), ('part-time','Part-time'), ('contract','Contract')],
        default='full-time'
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.location}"


class VacancyApplication(models.Model):
    # Link to Vacancy
    vacancy = models.ForeignKey(
        Vacancy, 
        on_delete=models.CASCADE, 
        related_name='applications',
        null=True,  # for existing records without a vacancy yet
        blank=True
    )

    # Mandatory fields
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    residence = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    position_applied = models.CharField(max_length=255)
    location_applied = models.CharField(max_length=255)
    file_attachment = models.FileField(upload_to='uploads/')

    # Optional fields
    email = models.EmailField(blank=True, null=True)
    additional_mobile_number = models.CharField(max_length=20, blank=True, null=True)
    current_employment_status = models.CharField(max_length=20, blank=True, null=True)
    current_employer = models.CharField(max_length=255, blank=True, null=True)
    current_role = models.CharField(max_length=255, blank=True, null=True)
    current_basic_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    education_details = models.JSONField(blank=True, null=True)
    previous_employers = models.JSONField(blank=True, null=True)
    roles_previous_employers = models.JSONField(blank=True, null=True)
    length_service_previous = models.JSONField(blank=True, null=True)
    total_banking_experience = models.PositiveIntegerField(blank=True, null=True)
    total_non_banking_experience = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.position_applied}"
