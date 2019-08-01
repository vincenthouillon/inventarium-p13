from django.test import TestCase, SimpleTestCase
from .models import User, Residence
from django.urls import resolve, reverse
from .views import homepage, residence, equipment, room, residence_add


class TestUrls(SimpleTestCase):
    def test_homepage_resolves(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_residence_resolves(self):
        url = reverse('residence', args=['1'])
        self.assertEquals(resolve(url).func, residence)

    def test_residence_add_resolves(self):
        url = reverse('residence_add')
        self.assertEquals(resolve(url).func, residence_add)

    def test_room_resolves(self):
        url = reverse('room', args=['1'])
        self.assertEquals(resolve(url).func, room)

    def test_equipment_resolves(self):
        url = reverse('equipment', args=['1'])
        self.assertEquals(resolve(url).func, equipment)


class NotAuthentificationTestCase(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEquals(response.status_code, 200)

    def test_signin(self):
        response = self.client.get('/signin/')
        self.assertEquals(response.status_code, 200)


class AuthentificationPageTestCase(TestCase):

    def setUp(self):
        url = ('/dashboard/')

        self.post = {
            'username': 'UserTest',
            'email': 'usertest@inventarium.fr',
            'password': hash("1234abcd")
        }

        self.response = self.client.post(url, self.post)
        self.user = User.objects.create_user(**self.post)

    def test_access_dashboard(self):
        self.client.login(**self.post)
        response = self.client.get('/dashboard/')
        self.assertEquals(response.status_code, 200)

    def test_access_profile(self):
        self.client.login(**self.post)
        response = self.client.get('/profile/')
        self.assertEquals(response.status_code, 200)


class DatabaseResidenceTestCase(TestCase):
    def setUp(self):

        self.post = {
            'username': 'UserTest',
            'email': 'usertest@inventarium.fr',
            'password': hash("1234abcd")
        }

        self.user = User.objects.create_user(**self.post)

        Residence.objects.create(
            name='Lorem',
            adress='',
            zip_code='',
            city='',
            user=self.user
        )

    def test_residence_name(self):
        residence = Residence.objects.get(id=1)
        residence_name = f'{residence.name}'
        self.assertEquals(residence_name, 'Lorem')
