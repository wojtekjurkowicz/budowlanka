from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.core.paginator import Page
from django.contrib.admin.sites import AdminSite

from .forms import AppointmentForm, CommentForm, ContactForm
from .models import Appointment, Realization, Comment, RealizationImage
from .admin import RealizationAdmin, AppointmentAdmin, CommentAdmin
from .views import CalendarView
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware


# Model tests
class TestModels(TestCase):
    def test_appointment_str_representation(self):
        """Test string representation of Appointment model"""
        aware_date = make_aware(datetime(2024, 5, 21))
        appointment = Appointment(description="Test Appointment", date=aware_date)
        self.assertEqual(str(appointment), "Test Appointment")

    def test_realization_str_representation(self):
        """Test string representation of Realization model"""
        aware_date = make_aware(datetime(2024, 5, 21))
        realization = Realization(title="Test", content="Test Realization", date=aware_date)
        self.assertEqual(str(realization), "Test")

    def test_comment_str_representation(self):
        """Test string representation of Comment model"""
        aware_date = make_aware(datetime(2024, 5, 21))
        comment = Comment(realization_id=1, author_id=1, content="Test Comment", date=aware_date)
        self.assertEqual(str(comment), "Test Comment")

    def test_realization_image_str(self):
        realization = Realization.objects.create(title="T", content="C")
        img = RealizationImage.objects.create(realization=realization, image="fake.jpg")
        self.assertEqual(str(img), "T Image")


# Forms tests
class TestForms(TestCase):
    def test_appointment_valid_form(self):
        """Test valid AppointmentForm"""
        form = AppointmentForm(data={'description': 'Test Description', 'date': "2024-05-21"})
        self.assertTrue(form.is_valid())

    def test_comment_valid_form(self):
        """Test valid CommentForm"""
        form = CommentForm(data={'content': 'Test Content', 'date': "2024-05-21"})
        self.assertTrue(form.is_valid())

    def test_contact_form_valid(self):
        form = ContactForm(
            data={'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com', 'message': 'Test Message'})
        self.assertTrue(form.is_valid())

    def test_appointment_invalid_form(self):
        form = AppointmentForm(data={'description': ''})  # brak daty i opisu
        self.assertFalse(form.is_valid())

    def test_comment_invalid_form(self):
        form = CommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())


# Views tests
class TestViews(TestCase):
    def setUp(self):
        """Setup before tests"""
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.list_url = reverse('mainapp:blog')
        self.appointment_url = reverse('mainapp:appointment')
        self.contact_url = reverse('mainapp:contact')

        # Create a test realization and comment
        self.realization = Realization.objects.create(title="Test Title", content="Test Content")
        self.detail_url = reverse('mainapp:detail', args=[self.realization.id])

    def test_blog_view(self):
        """Test blog view"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/blog.html')

    def test_detail_view(self):
        """Test detail view"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/detail.html')

    def test_appointment_view_get(self):
        """Test appointment view (GET)"""
        response = self.client.get(self.appointment_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/appointment.html')

    def test_appointment_view_post(self):
        """Test appointment view (POST)"""
        response = self.client.post(self.appointment_url, {
            'description': 'Test Appointment',
            'date': '2024-05-21T10:00:00Z'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post

    def test_contact_view(self):
        """Test contact view"""
        response = self.client.post(self.contact_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'message': 'Test message'
        })

        self.assertRedirects(response, reverse('mainapp:index'), fetch_redirect_response=False)

        response = self.client.get(reverse('mainapp:index'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'mainapp/index.html')

    def test_comment_creation(self):
        """Test comment creation"""
        response = self.client.post(self.detail_url, {'content': 'New Test Comment', 'date': '2024-05-21'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post
        self.assertEqual(Comment.objects.count(), 1)  # Ensure that the comment is created

    def test_contact_view_get(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/contact.html')


# Email sending tests
class TestEmail(TestCase):
    def setUp(self):
        """Setup before tests"""
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_appointment_email_sent(self):
        """Test if appointment confirmation email is sent"""
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('mainapp:appointment'), {
            'description': 'Testowa wizyta',
            'date': '2024-05-21T10:00:00Z'
        })

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Potwierdzenie wizyty')
        self.assertEqual(email.to, [self.user.email])
        self.assertIn('Testowa wizyta', email.body)


# Pagination tests
class TestPagination(TestCase):
    """Tests for pagination"""

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('mainapp:blog')
        for i in range(15):
            Realization.objects.create(title=f'Test Title {i}', content=f'Test Content {i}')

    def test_pagination_is_ten(self):
        """Test if pagination shows ten items per page"""
        response = self.client.get(reverse('mainapp:blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue(isinstance(response.context['page_obj'], Page))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_lists_all_realizations(self):
        """Test if all realizations are listed on the first page"""
        response = self.client.get(reverse('mainapp:blog') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_pagination_second_page(self):
        """Test if the second pagination page contains five items"""
        response = self.client.get(reverse('mainapp:blog') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_blog_view_no_entries(self):
        Realization.objects.all().delete()
        response = self.client.get(reverse('mainapp:blog'))
        self.assertEqual(response.status_code, 200)


class MockRequest:
    pass


# Admin PDF export tests
class AdminExportPDFTest(TestCase):
    """Tests for PDF export through admin panel"""

    def setUp(self):
        """Setup before tests"""
        self.site = AdminSite()

        self.realization_admin = RealizationAdmin(Realization, self.site)
        self.appointment_admin = AppointmentAdmin(Appointment, self.site)
        self.comment_admin = CommentAdmin(Comment, self.site)

        self.realization = Realization.objects.create(title="Test Title", content="Test Content")
        aware_date = make_aware(datetime(2024, 5, 21))
        self.appointment = Appointment.objects.create(description="Test Appointment", date=aware_date)
        self.comment = Comment.objects.create(realization=self.realization,
                                              author=User.objects.create(username='testuser'), content="Test Comment")

    def test_realization_export_to_pdf(self):
        """Test exporting realizations to PDF"""
        queryset = Realization.objects.all()
        request = MockRequest()
        response = self.realization_admin.export_to_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="database_report.pdf"', response['Content-Disposition'])

    def test_appointment_export_to_pdf(self):
        """Test exporting appointments to PDF"""
        queryset = Appointment.objects.all()
        request = MockRequest()
        response = self.appointment_admin.export_to_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="database_report.pdf"', response['Content-Disposition'])

    def test_comment_export_to_pdf(self):
        """Test exporting comments to PDF"""
        queryset = Comment.objects.all()
        request = MockRequest()
        response = self.comment_admin.export_to_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="database_report.pdf"', response['Content-Disposition'])


# ContactForm tests
class TestContactForm(TestCase):
    """Tests for ContactForm"""

    def test_contact_form_valid(self):
        """Test valid ContactForm"""
        form = ContactForm(
            data={'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com', 'message': 'Test Message'})
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        """Test invalid ContactForm"""
        form = ContactForm(data={'first_name': '', 'last_name': '', 'email': 'invalid', 'message': ''})
        self.assertFalse(form.is_valid())


class TestCalendarView(TestCase):
    def test_format_month_generates_html(self):
        # Tworzymy wizytę na maj 2024
        Appointment.objects.create(description="Wizyta testowa", date=timezone.datetime(2024, 5, 15, tzinfo=timezone.utc))

        calendar = CalendarView()
        html = calendar.formatmonth(2024, 5)
        self.assertIn('<table', html)
        self.assertIn('Zajęty termin', html)

