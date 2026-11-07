
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!"
        )

    # 1. Registration Test
    def test_user_registration(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertRedirects(
            response,
            reverse("accounts:login")
        )

        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    # 2. Duplicate Username Test
    def test_duplicate_username_registration(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "testuser",
                "email": "another@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(response.context["form"].errors)

    # 3. Duplicate Email Test
    def test_duplicate_email_registration(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "anotheruser",
                "email": "test@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(response.context["form"].errors)

    # 4. Login Test
    def test_user_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "StrongPass123!",
            }
        )

        self.assertRedirects(
            response,
            reverse("applications:dashboard")
        )

    # 5. Logout Test
    def test_user_logout(self):
        self.client.login(
            username="testuser",
            password="StrongPass123!"
        )

        response = self.client.post(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            reverse("accounts:login")
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )

    # 6. Profile Access Protection Test
    def test_profile_requires_login(self):
        response = self.client.get(
            reverse("accounts:profile")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("accounts:login"),
            response.url
        )

    # 7. Profile Update Test
    def test_user_can_update_own_profile(self):
        self.client.login(
            username="testuser",
            password="StrongPass123!"
        )

        response = self.client.post(
            reverse("accounts:profile"),
            {
                "username": "updateduser",
                "email": "updated@example.com",
                "first_name": "Redwanul",
                "last_name": "Rimon",
            }
        )

        self.assertRedirects(
            response,
            reverse("accounts:profile")
        )

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.first_name, "Redwanul")
        self.assertEqual(self.user.last_name, "Rimon")

    # 8. Profile Ownership Test
    def test_user_cannot_update_another_users_profile(self):
        another_user = User.objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="StrongPass123!"
        )

        self.client.login(
            username="testuser",
            password="StrongPass123!"
        )

        self.client.post(
            reverse("accounts:profile"),
            {
                "username": "anotheruser",
                "email": "another@example.com",
                "first_name": "Changed",
                "last_name": "Name",
            }
        )

        another_user.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(another_user.username, "anotheruser")
        self.assertEqual(another_user.first_name, "")
        self.assertEqual(self.user.username, "testuser")
