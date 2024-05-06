from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
from users.views import LoginAPIView

LoginAPIView.throttle_classes = []

class LoginAPIViewTests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='IT')

        self.user = User.objects.create_user(username='test_user', email='test_email@gmail.com', password='test_password')
        self.user.groups.add(group)

    def test_correct_credentials(self):
        login_data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_credentials(self):
        login_data = {'username': 'test_user1', 'password': 'test_password1'}
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-list')
        group = Group.objects.create(name='IT')

        self.user = User.objects.create_user(username='test_user', email='test_email@gmail.com', password='test_password')
        self.user.groups.add(group)
        
        login_data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(reverse('login'), login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data.get('token', '')
        self.header_authentication = {'Authorization': f'Token {self.token}'}

        self.test_username = 'testusername'
        self.test_password = 'Test_password1'
        self.test_email = 'test_email2@gmail.com'


    def test_get_list_authenticated(self):
        response = self.client.get(self.url, headers=self.header_authentication)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_proper_response(self):
        expected_data = {
            'count': 1, 
            'next': None, 
            'previous': None, 
            'results': [{'username': 'test_user'}], 
            'total_pages': 1
        }

        response = self.client.get(self.url, headers=self.header_authentication)
        data = response.data
        uuid = data['results'][0].pop('uuid')
        self.assertEqual(len(uuid), 36)
        self.assertEqual(data, expected_data)


    def test_post_create_authenticated(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': self.test_password}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_create_unathenticated(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': self.test_password}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_password_no_uppercase_letter(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': 'test_password1'}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_password_no_lowercase_letter(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': 'TEST_PASSWORD1'}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_password_no_digit(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': 'Test_password'}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_password_more_than_32_characters(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': 'Test_password1aaaaaaaaaaaaaaaaaaa'}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_password_less_than_8_characters(self):
        data = {'username': self.test_username, 'email': self.test_email, 'password': 'Tpass1'}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_username_bad_character(self):
        data = {'username': 'Test_username1@', 'email': self.test_email, 'password': self.test_password}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_username_more_than_30_characters(self):
        data = {'username': 'Test_username1aaaaaaaaaaaaaaaaa', 'email': self.test_email, 'password': self.test_password}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_username_less_than_3_characters(self):
        data = {'username': 'T1', 'email': self.test_email, 'password': self.test_password}
        response = self.client.post(self.url, data=data, headers=self.header_authentication, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test_email@gmail.com', password='test_password')
        group = Group.objects.create(name='IT')
        self.user.groups.add(group)
        self.url = reverse('user-detail', kwargs={'uuid': self.user.uuid})
        
        login_data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(reverse('login'), login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data.get('token', '')
        self.header_authentication = {'Authorization': f'Token {self.token}'}

    def test_get_user_details(self):
        expected_data = {'username': 'test_user', 'email': 'test_email@gmail.com'}
        response = self.client.get(self.url, headers=self.header_authentication)
        data = response.data
        for key, value in expected_data.items():
            self.assertIn(key, data)
            self.assertEqual(data[key], value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_partial_update(self):
        data = {'username':'Test_username1'}
        response = self.client.patch(self.url, data=data, headers=self.header_authentication)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.username, data['username'])

    def test_delete_user(self):
        response = self.client.delete(self.url, headers=self.header_authentication)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(uuid=self.user.uuid)
        
class UserAccountViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test_email@gmail.com', password='test_password')
        self.url = reverse('user-me')
        self.client.force_authenticate(user=self.user)

    def test_get_response(self):
        expected_data = {'username': 'test_user', 'email': 'test_email@gmail.com'}
        response = self.client.get(self.url)
        data = response.data
        for key, value in expected_data.items():
            self.assertIn(key, data)
            self.assertEqual(data[key], value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class ChangePasswordViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('change-password')
        self.user = User.objects.create_user(username='test_user', email='test_email@gmail.com', password='test_password')

        self.test_password = 'Test_password1'
        self.client.force_authenticate(user=self.user)

    def test_post_correct_credentials(self):
        data = {'old_password': 'test_password', 'new_password': self.test_password}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        login_data = {'username': 'test_user', 'password': self.test_password}
        response = self.client.post(reverse('login'), login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_incorrect_old_password(self):
        data = {'old_password': 'incorrect_password', 'new_password': self.test_password}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_incorrect_new_password(self):
        data = {'old_password': 'test_password', 'new_password': 'new_password1'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
