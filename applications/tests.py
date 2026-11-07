from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
from internships.models import Company, Opportunity
from applications.models import Application
from applications.forms import ApplicationForm


class ApplicationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="testpassword123",
        )

        self.company = Company.objects.create(name="Tech Corp", owner=self.user)
        self.opportunity = Opportunity.objects.create(
            company=self.company,
            title="Software Engineer Intern",
            opportunity_type="INTERNSHIP",
            owner=self.user,
        )

        self.application = Application.objects.create(
            user=self.user,
            opportunity=self.opportunity,
            status="APPLIED",
            applied_date=timezone.now().date(),
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("applications:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_context_statistics(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("applications:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("stats", response.context)
        self.assertIn("total_applications", response.context["stats"])
        self.assertEqual(response.context["stats"]["total_applications"], 1)

    def test_application_list_requires_login(self):
        response = self.client.get(reverse("applications:list"))
        self.assertEqual(response.status_code, 302)

    def test_user_can_view_own_applications(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("applications:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Software Engineer Intern")

    def test_user_cannot_view_others_applications(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("applications:list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Software Engineer Intern")

    def test_user_can_create_application(self):
        self.client.force_login(self.user)
        opp2 = Opportunity.objects.create(
            company=self.company,
            title="Frontend Intern",
            opportunity_type="INTERNSHIP",
            owner=self.user,
        )
        response = self.client.post(
            reverse("applications:create"),
            {
                "opportunity": opp2.pk,
                "status": "APPLIED",
                "applied_date": timezone.now().date(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Application.objects.filter(opportunity=opp2, user=self.user).exists())

    def test_cannot_create_duplicate_application_for_same_opportunity(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("applications:create"),
            {
                "opportunity": self.opportunity.pk,
                "status": "APPLIED",
                "applied_date": timezone.now().date(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.filter(opportunity=self.opportunity, user=self.user).count(), 1)

    def test_future_applied_date_is_rejected(self):
        form = ApplicationForm(
            data={
                "opportunity": self.opportunity.pk,
                "status": "APPLIED",
                "applied_date": timezone.now().date() + timedelta(days=5),
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("applied_date", form.errors)

    def test_interview_date_before_applied_date_is_rejected(self):
        form = ApplicationForm(
            data={
                "opportunity": self.opportunity.pk,
                "status": "INTERVIEW",
                "applied_date": timezone.now().date(),
                "interview_date": timezone.now() - timedelta(days=2),
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("interview_date", form.errors)

    def test_user_cannot_create_application_with_others_opportunity(self):
        other_company = Company.objects.create(name="Other Corp", owner=self.other_user)
        other_opp = Opportunity.objects.create(
            company=other_company,
            title="DevOps Intern",
            opportunity_type="INTERNSHIP",
            owner=self.other_user,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("applications:create"),
            {
                "opportunity": other_opp.pk,
                "status": "APPLIED",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Application.objects.filter(opportunity=other_opp, user=self.user).exists())

    def test_user_cannot_edit_others_application(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("applications:edit", kwargs={"pk": self.application.pk}),
            {"status": "OFFER"},
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_others_application(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("applications:delete", kwargs={"pk": self.application.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Application.objects.filter(pk=self.application.pk).exists())

    def test_application_form_requires_user_argument(self):
        with self.assertRaises(ValueError):
            ApplicationForm()

    def test_application_delete_get_not_allowed(self):
        self.client.force_login(self.user)
       
        response = self.client.get(reverse("applications:delete", kwargs={"pk": self.application.pk}))
        self.assertEqual(response.status_code, 405) 
        self.assertTrue(Application.objects.filter(pk=self.application.pk).exists())

    def test_filter_by_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("applications:list") + "?status=APPLIED")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Software Engineer Intern")