from django.contrib import admin
from .models import Company, Opportunity


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "created_at")
    search_fields = ("name", "location")
    list_filter = ("created_at",)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "opportunity_type",
        "owner",
        "deadline",
    )
    search_fields = ("title", "company__name")
    list_filter = ("opportunity_type", "is_remote")