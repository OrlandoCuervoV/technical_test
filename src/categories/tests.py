import requests
from access.tests import TechTestCase
from .models import Category


class setUp():

    def setup_category(self):
        """
        create category
        """
        self.category = Category.objects.create(code="Jui" , description="The best juices in the world", title="Juices")
        self.url_category = self.get_url_server() + "api/api/categories/" + str(self.category.id) + "/"


class UserLoginTokenTestCase(TechTestCase):

    def setUp(self):
        self.setupUser()

    def test_authentication_without_password(self):
        """
        Test to verify the login without password
        """
        url = self.get_url_server() + "rest-auth/login/"
        response = requests.post(url, {"email": "snowman/n"})
        self.assertEqual(400, response.status_code)

    def test_authentication_wrong_password(self):
        """
        Test to verify the login with wrong password
        """
        url = self.get_url_server() + "rest-auth/login/"
        data = {"email": self.email, "password": "I/know"}
        response = requests.post(url, json=data)
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        """
        Test to verify the login with valid data
        """
        url = self.get_url_server() + "rest-auth/login/"
        data = {"email": self.email, "password": self.password}
        response = requests.post(url, json=data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in response.json())


class CategoryTestCase(TechTestCase, setUp):

    def setUp(self):
        self.setupUser()
        self.setupToken()

    def test_register_category(self):
        """
        Test to verify the create a category
        """
        url = self.get_url_server() + "api/categories/"
        data = {"code": "Fru", "description": "The best fruits in the world", "title":"Fruits"}
        response = requests.post(url, auth=self.auth,json=data)
        self.assertEqual(201, response.status_code)

    def test_update_category(self):
        """
        Test to verify the update a category
        """
        self.setup_category()
        url = self.get_url_server() + "api/categories/" + str(self.category.id) + "/"
        data = {"id": self.category.id, "code": "Juic", "description": "The best juices in the world!!!", "title":"Juices"}
        response = requests.put(url, auth=self.auth, json=data)
        self.assertEqual(200, response.status_code)

    def test_patch_category(self):
        """
        Test to verify the patch a category
        """
        self.setup_category()
        url = self.get_url_server() + "api/categories/" + str(self.category.id) + "/"
        data = {"id": self.category.id, "status": "inactive"}
        response = requests.patch(url, auth=self.auth, json=data)
        self.assertEqual(200, response.status_code)


class CategoryQueryTestCase(TechTestCase, setUp):

    def setUp(self):
        self.setupUser()
        self.setupToken()
        self.setup_category()

    def test_query_all_categories(self):
        """
        Test to verify categories queries already created
        """
        url = self.get_url_server() + "api/categories/"
        header = {'Authorization': 'Bearer ' + str(self.token)}
        response = requests.get(url, headers=header)
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(len(data), 1)

