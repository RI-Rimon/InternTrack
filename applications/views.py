from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ApplicationForm
from .models import Application


@login_required
def dashboard(request):
    user_apps = Application.objects.filter(user=request.user)

    stats = user_apps.aggregate(
        total_applications=Count("id"),
        saved_count=Count("id", filter=Q(status="SAVED")),
        applied_count=Count("id", filter=Q(status="APPLIED")),
        assessment_count=Count("id", filter=Q(status="ASSESSMENT")),
        interview_count=Count("id", filter=Q(status="INTERVIEW")),
        offer_count=Count("id", filter=Q(status="OFFER")),
        rejected_count=Count("id", filter=Q(status="REJECTED")),
    )

    upcoming_interviews = (
        user_apps.filter(
            status="INTERVIEW",
            interview_date__isnull=False,
            interview_date__gte=timezone.now(),
        )
        .select_related("opportunity__company")
        .order_by("interview_date")[:5]
    )

    recent_applications = (
        user_apps.select_related("opportunity__company")
        .order_by("-updated_at")[:5]
    )

    context = {
        "stats": stats,
        "upcoming_interviews": upcoming_interviews,
        "recent_applications": recent_applications,
    }
    return render(request, "applications/dashboard.html", context)


@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user).select_related("opportunity__company")

    status_filter = request.GET.get("status")
    query = request.GET.get("q")

    if status_filter:
        applications = applications.filter(status=status_filter)

    if query:
        applications = applications.filter(
            Q(opportunity__title__icontains=query)
            | Q(opportunity__company__name__icontains=query)
            | Q(notes__icontains=query)
        )

    status_field = Application._meta.get_field("status")
    status_choices = status_field.choices

    context = {
        "applications": applications.order_by("-updated_at"),
        "status_choices": status_choices,
        "current_status": status_filter,
        "search_query": query,
    }
    return render(request, "applications/application_list.html", context)


@login_required
def application_create(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect("applications:list")
    else:
        form = ApplicationForm(user=request.user)

    return render(request, "applications/application_form.html", {"form": form})


@login_required
def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("applications:list")
    else:
        form = ApplicationForm(instance=application, user=request.user)

    return render(request, "applications/application_form.html", {"form": form, "application": application})


@login_required
@require_POST
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    application.delete()
    return redirect("applications:list")