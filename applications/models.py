
from django.conf import settings
from django.db import models


class Application(models.Model):

    class Status(models.TextChoices):
        SAVED = "SAVED", "Saved"
        APPLIED = "APPLIED", "Applied"
        ASSESSMENT = "ASSESSMENT", "Assessment"
        INTERVIEW = "INTERVIEW", "Interview"
        OFFER = "OFFER", "Offer"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    opportunity = models.ForeignKey(
        "internships.Opportunity",
        on_delete=models.CASCADE,
        related_name="applications",
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.SAVED,
    )

    applied_date = models.DateField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "opportunity"],
                name="unique_user_opportunity_application",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"
