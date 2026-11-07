from django.conf import settings
from django.db import models


class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_owner_company_name",
            )
        ]

    def __str__(self):
        return self.name



class Opportunity(models.Model):

    class OpportunityType(models.TextChoices):
        INTERNSHIP = "INTERNSHIP", "Internship"
        FULL_TIME = "FULL_TIME", "Full-time"
        PART_TIME = "PART_TIME", "Part-time"
        GRADUATE_TRAINEE = "GRADUATE_TRAINEE", "Graduate Trainee"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="opportunities",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="opportunities",
    )
    title = models.CharField(max_length=200)
    opportunity_type = models.CharField(
        max_length=20,
        choices=OpportunityType.choices,
        default=OpportunityType.INTERNSHIP,
    )
    description = models.TextField(blank=True)
    application_url = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    is_remote = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"    