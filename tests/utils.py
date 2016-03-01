from __future__ import unicode_literals, print_function
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from rest_framework.test import APITestCase as BaseAPITestCase
from oauth2_provider.models import get_application_model, AccessToken


class TestCase(BaseAPITestCase):
    """
    This is the base test case providing common features for all tests
    """

    def setUp(self):
        """
        Create a superuser and standard user.
        Create an Oauth2 app for superuser.
        """
        self.superuser = get_user_model().objects.create_superuser('admin', password='admin', email='admin@example.com')
        self.user = get_user_model().objects.create_user('test', password='test', email='test@example.com')

        self.app = get_application_model().objects.create(
            name='app',
            client_type=get_application_model().CLIENT_CONFIDENTIAL,
            authorization_grant_type=get_application_model().GRANT_CLIENT_CREDENTIALS,
            user=self.superuser
        )

        self.token = AccessToken.objects.create(user=self.superuser,
                                                token='token_monster',
                                                application=self.app,
                                                expires=now() + timedelta(days=365))

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'token_monster',
        }

    def tearDown(self):
        """
        Clean up when tests end
        """
        self.superuser.delete()
        self.user.delete()
        self.app.delete()
        self.token.delete()
