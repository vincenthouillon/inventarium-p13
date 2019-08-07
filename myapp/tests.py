from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

import myapp.views as views

from .models import Category, Equipment, Residence, Room, CustomUser

PAGES_WITH_ARGS = [
    'equipment_add',
    'equipment_delete',
    'equipment_update',
    'equipment',
    'residence_delete',
    'residence_update',
    'residence',
    'room_add',
    'room_delete',
    'room_update',
    'room',
]

PAGES_WITHOUT_ARGS = [
    'about',
    'homepage',
    'index',
    'account',
    'account_update',
    'signup',
    'residence_add',
    'search',
    'signin',
    'signout',
    'terms',
    'user_delete',
]


class TestResolveUrls(SimpleTestCase):
    """Test if the urls answer."""

    def test_pages_with_args(self):
        """Test 11 urls."""
        for page in PAGES_WITH_ARGS:
            url = reverse(page, args=['1'])
            self.assertEquals(resolve(url).func, getattr(views, page))

    def test_pages_without_args(self):
        """Test 12 urls."""
        for page in PAGES_WITHOUT_ARGS:
            url = reverse(page)
            self.assertEquals(resolve(url).func, getattr(views, page))


class NotAuthentificationTestCase(TestCase):
    """Test pages that do not require authentication."""

    def test_homepage_response(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_about_response(self):
        response = self.client.get('/about/')
        self.assertEquals(response.status_code, 200)

    def test_signin_response(self):
        response = self.client.get('/signin/')
        self.assertEquals(response.status_code, 200)

    def test_signup_response(self):
        response = self.client.get('/signup/')
        self.assertEquals(response.status_code, 200)

    def test_terms_response(self):
        response = self.client.get('/signup/terms/')
        self.assertEquals(response.status_code, 200)


class AuthAndDatabaseTestCase(TestCase):
    """
    Test the operation of the database and pages requiring authentication.
    """

    def setUp(self):
        self.post = {
            'email': 'usertest@inventarium.fr',
            'password': hash("1234abcd")
        }

        self.user = CustomUser.objects.create_user(**self.post)
        self.client.login(**self.post)
        self.residence = Residence.objects.create(name='lorem', user=self.user)
        self.room = Room.objects.create(name='kitchen',
                                        residence=self.residence)
        self.category = Category.objects.create(name='test')
        self.equipment = Equipment.objects.create(
            name='tv', category=self.category, room=self.room)

    def test_homepage_response(self):
        self.client.login(**self.post)
        response = self.client.get('/homepage/')
        self.assertEquals(response.status_code, 200)

    def test_account_response(self):
        self.client.login(**self.post)
        response = self.client.get('/account/')
        self.assertEquals(response.status_code, 200)

    def test_residence_name(self):
        residence = Residence.objects.get(id=self.residence.id)
        residence_name = f'{residence.name}'
        self.assertEquals(residence_name, 'lorem')

    def test_room_name(self):
        room = Room.objects.get(id=self.room.id)
        room_name = f'{room.name}'
        self.assertEquals(room_name, 'kitchen')

    def test_equipment_name(self):
        equipment = Equipment.objects.get(id=self.equipment.id)
        equipment_name = f'{equipment.name}'
        self.assertEquals(equipment_name, 'tv')

    def test_page_residence_response(self):
        self.client.login(**self.post)
        residence = Residence.objects.get(id=self.residence.id)
        url = reverse('residence', args=[residence.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_page_room_response(self):
        self.client.login(**self.post)
        room = Room.objects.get(id=self.room.id)
        url = reverse('room', args=[room.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_page_equipment_response(self):
        self.client.login(**self.post)
        equipment = Equipment.objects.get(id=self.equipment.id)
        url = reverse('equipment', args=[equipment.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
