from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from internships.models import Company, Opportunity


class InternshipTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password123"
        )
        self.company1 = Company.objects.create(
            name="Google", owner=self.user1
        )
        self.opportunity1 = Opportunity.objects.create(
            company=self.company1,
            title="Backend Intern",
            owner=self.user1,
        )

    def test_company_list_requires_login(self):
        response = self.client.get(reverse("internships:companies"))
        self.assertEqual(response.status_code, 302)

    def test_user_can_view_own_companies(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("internships:companies"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google")

    def test_user_cannot_view_others_companies(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse("internships:companies"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Google")

    def test_user_can_create_company(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("internships:company_create"),
            {"name": "Microsoft", "website": "https://microsoft.com", "location": "Remote"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(name="Microsoft", owner=self.user1).exists())

    def test_company_creation_validation(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse("internships:company_create"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")

    def test_user_cannot_edit_others_company(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("internships:company_edit", kwargs={"pk": self.company1.pk}),
            {"name": "Google Updated"},
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_others_company(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("internships:company_delete", kwargs={"pk": self.company1.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Company.objects.filter(pk=self.company1.pk).exists())

    def test_opportunity_list_requires_login(self):
        response = self.client.get(reverse("internships:list"))
        self.assertEqual(response.status_code, 302)

    def test_opportunity_list_isolated(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse("internships:list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Backend Intern")

    def test_user_can_create_opportunity(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("internships:create"),
            {
                "company": self.company1.pk,
                "title": "Frontend Intern",
                "opportunity_type": "INTERNSHIP",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Opportunity.objects.filter(title="Frontend Intern", owner=self.user1).exists()
        )

    def test_user_cannot_create_opportunity_with_others_company(self):
        company2 = Company.objects.create(name="Meta", owner=self.user2)
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("internships:create"),
            {
                "company": company2.pk,
                "title": "DevOps Intern",
                "opportunity_type": "INTERNSHIP",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Opportunity.objects.filter(title="DevOps Intern").exists())

    def test_user_cannot_edit_others_opportunity(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("internships:edit", kwargs={"pk": self.opportunity1.pk}),
            {"title": "Hacked Title"},
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_others_opportunity(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("internships:delete", kwargs={"pk": self.opportunity1.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Opportunity.objects.filter(pk=self.opportunity1.pk).exists())

    def test_opportunity_deletion_cascades_safely(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("internships:delete", kwargs={"pk": self.opportunity1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Opportunity.objects.filter(pk=self.opportunity1.pk).exists())