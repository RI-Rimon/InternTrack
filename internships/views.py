from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompanyForm, OpportunityForm
from .models import Company, Opportunity


@login_required
def company_list(request):
    companies = (
        Company.objects.filter(owner=request.user)
        .annotate(opportunity_count=Count("opportunities"))
        .order_by("name")
    )
    return render(request, "internships/company_list.html", {"companies": companies})


@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect("internships:companies")
    else:
        form = CompanyForm()

    return render(request, "internships/company_form.html", {"form": form})


@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect("internships:companies")
    else:
        form = CompanyForm(instance=company)

    return render(request, "internships/company_form.html", {"form": form, "company": company})


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == "POST":
        company.delete()
        return redirect("internships:companies")

    return render(request, "internships/company_confirm_delete.html", {"company": company})


@login_required
def opportunity_list(request):
    opportunities = (
        Opportunity.objects.filter(owner=request.user)
        .select_related("company")
        .order_by("-created_at")
    )
    return render(request, "internships/opportunity_list.html", {"opportunities": opportunities})


@login_required
def opportunity_create(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST, user=request.user)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.owner = request.user
            opportunity.save()
            return redirect("internships:list")
    else:
        form = OpportunityForm(user=request.user)

    return render(request, "internships/opportunity_form.html", {"form": form})


@login_required
def opportunity_edit(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, owner=request.user)

    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("internships:list")
    else:
        form = OpportunityForm(instance=opportunity, user=request.user)

    return render(request, "internships/opportunity_form.html", {"form": form, "opportunity": opportunity})


@login_required
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, owner=request.user)

    if request.method == "POST":
        opportunity.delete()
        return redirect("internships:list")

    return render(request, "internships/opportunity_confirm_delete.html", {"opportunity": opportunity})