from rest_framework.test import APILiveServerTestCase
import requests

from django.contrib.auth.models import User


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + str(self.token)
        return r


class TechTestCase(APILiveServerTestCase):
    def get_url_server(self):
        return self.live_server_url + "/"

    def setupUser(self):
        """
        create user
        """
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you/know/"
        self.is_active = True
        self.is_superuser = True
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def setupToken(self):
        """
        create token
        """
        url = self.get_url_server() + "rest-auth/login/"
        data = {"email": self.email, "password": self.password}
        response = requests.post(url, json=data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in response.json())
        self.token=response.json()['token']
        self.auth = TokenAuth(self.token)





