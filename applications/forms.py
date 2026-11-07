from django import forms
from django.utils import timezone
from .models import Application
from internships.models import Opportunity


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "opportunity",
            "status",
            "applied_date",
            "interview_date",
            "notes",
        ]
        widgets = {
            "opportunity": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "applied_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "interview_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Interview notes, questions, impressions..."}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        if user is None:
            raise ValueError("User is required for ApplicationForm")
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["opportunity"].queryset = Opportunity.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        opportunity = cleaned_data.get("opportunity")
        applied_date = cleaned_data.get("applied_date")
        interview_date = cleaned_data.get("interview_date")

       
        if opportunity and self.user:
            duplicate_qs = Application.objects.filter(user=self.user, opportunity=opportunity)
            if self.instance.pk:
                duplicate_qs = duplicate_qs.exclude(pk=self.instance.pk)
            if duplicate_qs.exists():
                self.add_error("opportunity", "You have already tracked an application for this opportunity.")

        
        if applied_date and applied_date > timezone.now().date():
            self.add_error("applied_date", "Applied date cannot be in the future.")

        
        if applied_date and interview_date:
            if interview_date.date() < applied_date:
                self.add_error(
                    "interview_date",
                    "Interview date cannot be earlier than the application date.",
                )

        return cleaned_data