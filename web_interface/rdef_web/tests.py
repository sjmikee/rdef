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
        self.failIf(response.context['msg'] == 'SUCCESS')
        self.assertEqual(len(mail.outbox), 0)

    def test_registration_complete_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.post(reverse('rdef_web:user_register'),
                                    data={'username': 'alice',
                                          'password': '123123',
                                          'password_confirm': '123123',
                                          'email': 'a@b.com'})
        self.assertEqual(response.context['msg'], 'SUCCESS')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/reg_complited.html')


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post(
            reverse('rdef_web:user_login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)


class TablesTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        blacklist.objects.create(url="https://google.com", protocol="https")
        whitelist.objects.create(url="https://google.com", protocol="https")
        urls.objects.create(url="https://google.com", protocol="https")

    def test_urls(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(reverse('rdef_web:urls_table'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/urls_table.html')

    def test_urls_nologin(self):
        response = self.client.get(reverse('rdef_web:urls_table'))

        self.assertEqual(response.status_code, 302)

    def test_whitelist(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(reverse('rdef_web:whitelist_table'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/urls_table.html')

    def test_whitelist_nologin(self):
        response = self.client.get(reverse('rdef_web:whitelist_table'))

        self.assertEqual(response.status_code, 302)

    def test_whitelist_remove(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(
            reverse('rdef_web:WLitem_remove', args=('1')), data={'pk': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/urls_table.html')

    def test_whitelist_remove_nologin(self):
        response = self.client.get(
            reverse('rdef_web:WLitem_remove', args=('1')), data={'pk': '1'})

        self.assertEqual(response.status_code, 302)

    def test_blacklist(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(reverse('rdef_web:blacklist_table'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/urls_table.html')

    def test_blacklist_nologin(self):
        response = self.client.get(reverse('rdef_web:blacklist_table'))

        self.assertEqual(response.status_code, 302)

    def test_blacklist_remove(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(
            reverse('rdef_web:BLitem_remove', args=('1')), data={'pk': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/urls_table.html')

    def test_blacklist_remove_nologin(self):
        response = self.client.get(
            reverse('rdef_web:BLitem_remove', args=('1')), data={'pk': '1'})

        self.assertEqual(response.status_code, 302)

    def test_blacklist_move_to_whitelist(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(
            reverse('rdef_web:BLitem_move_to_WL', args=('1')), data={'pk': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/urls_table.html')

    def test_blacklist_move_to_whitelist_nologin(self):
        response = self.client.get(
            reverse('rdef_web:BLitem_move_to_WL', args=('1')), data={'pk': '1'})

        self.assertEqual(response.status_code, 302)


class ChartsTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_charts(self):
        self.client.login(username="testuser", password='secret')
        response = self.client.get(reverse('rdef_web:charts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdef_web/charts.html')

    def test_charts_nologin(self):
        response = self.client.get(reverse('rdef_web:charts'))

        self.assertEqual(response.status_code, 302)
