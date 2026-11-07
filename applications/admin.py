from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "opportunity",
        "status",
        "applied_date",
        "interview_date",
    )
    search_fields = (
        "user__username",
        "opportunity__title",
        "opportunity__company__name",
    )
    list_filter = ("status",)