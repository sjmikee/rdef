from __future__ import unicode_literals
from django.test import TestCase
from rdef_web.models import urls, whitelist, blacklist
import datetime
from django.conf import settings
from django.core import mail
from django.urls import reverse

from rdef_web import forms

from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY


# Create your tests here.


class UrlsTestCase(TestCase):
    def setUp(self):
        urls.objects.create(url="https://google.com", protocol="https")
        urls.objects.create(url="https://youtube.com", protocol="https")

    def test_urls(self):
        google = urls.objects.get(url="https://google.com")
        youtube = urls.objects.get(url="https://youtube.com")
        self.assertEqual(google.protocol, "https")
        self.assertEqual(youtube.protocol, "https")


class WhitelistTestCase(TestCase):
    def setUp(self):
        whitelist.objects.create(url="https://google.com", protocol="https")
        whitelist.objects.create(url="https://youtube.com", protocol="https")

    def test_urls(self):
        google = whitelist.objects.get(url="https://google.com")
        youtube = whitelist.objects.get(url="https://youtube.com")
        self.assertEqual(google.protocol, "https")
        self.assertEqual(youtube.protocol, "https")


class BlacklistTestCase(TestCase):
    def setUp(self):
        blacklist.objects.create(url="https://google.com", protocol="https")
        blacklist.objects.create(url="https://youtube.com", protocol="https")

    def test_urls(self):
        google = blacklist.objects.get(url="https://google.com")
        youtube = blacklist.objects.get(url="https://youtube.com")
        self.assertEqual(google.protocol, "https")
        self.assertEqual(youtube.protocol, "https")


class RegistrationViewTestCase(TestCase):

    def test_registration_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.get(reverse('rdef_web:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'rdef_web/registration.html')
        self.failUnless(isinstance(response.context['user_form'],
                                   forms.UserForm))

    def test_registration_view_post_failure(self):
        """
        A ``POST`` to the ``register`` view with invalid data does not
        create a user, and displays appropriate error messages.

        """
        response = self.client.post(reverse('rdef_web:user_register'),
                                    data={'username': 'bob',
                                          'email1': 'bobe@example.com',
                                          'email2': 'mark@example.com'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['user_form'].is_valid())
        self.assertEqual(len(mail.outbox), 0)

    def test_registration_complete_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        # register save registration_profile in the session
        response = self.client.post(reverse('rdef_web:user_register'),
                                    data={'username': 'alice',
                                          'password': '123123',
                                          'confirm_password': '123123',
                                          'email': 'a@b.com'})
        self.assertEqual(response.context['registered'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/registration.html')


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # login
        response = self.client.post(
            reverse('rdef_web:user_login'), self.credentials,  follow=True)
        self.assertTrue(response.context['user'].is_active)
