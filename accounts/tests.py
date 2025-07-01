from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewsTests(TestCase):

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Testpass123',
            'password2': 'Testpass123',
        })
        self.assertRedirects(response, reverse('mainapp:index'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_invalid(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': '',
            'email': 'invalid',
            'password1': '123',
            'password2': '456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hasła nie są takie same')

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_valid(self):
        User.objects.create_user(username='testuser', password='Testpass123')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'Testpass123',
        })
        self.assertRedirects(response, reverse('mainapp:index'))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'invalid',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Twoja nazwa użytkownika lub hasło są niepoprawne')
