
from django.urls import path
from . import views

app_name = "internships"

urlpatterns = [
    path("", views.opportunity_list, name="list"),
    path("create/", views.opportunity_create, name="create"),
    path("<int:pk>/edit/", views.opportunity_edit, name="edit"),
    path("<int:pk>/delete/", views.opportunity_delete, name="delete"),

    path("companies/", views.company_list, name="companies"),
    path("companies/create/", views.company_create, name="company_create"),
    path("companies/<int:pk>/edit/", views.company_edit, name="company_edit"),
    path("companies/<int:pk>/delete/", views.company_delete, name="company_delete"),
]
