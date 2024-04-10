from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from professional.views import professional_general_controller, professional_with_id_controller


class ProfessionalTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.valid_professional = {
            'full_name': 'walefy',
            'social_name': '',
            'profession': 'developer',
            'contact': 'gg@gg.com',
            'address': 'rua dos bobos'
        }

    def create_professional(self):
        request = self.factory.post('/professional', self.valid_professional, format='json')
        return professional_general_controller(request)

    def test_create_professional(self):
        view_response = self.create_professional()

        response_without_id = view_response.data.copy()
        response_without_id.pop('id')

        self.assertEqual(view_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(view_response.data.get('id'), int))
        self.assertEqual(view_response.data.get('full_name'), 'walefy')
        self.assertEqual(response_without_id, self.valid_professional)

    def test_delete_professional(self):
        professional_id = 1

        self.create_professional()

        delete_request = self.factory.delete(f'/professional/{professional_id}', format='json')
        response = professional_with_id_controller(delete_request, professional_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'professional deleted!'})

    def test_find_professional_by_id(self):
        professional_id = 1

        self.create_professional()

        request = self.factory.get(f'/professional/{professional_id}', format='json')
        response = professional_with_id_controller(request, professional_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'id': 1, **self.valid_professional}, response.data)

    def test_find_all_professionals(self):
        professionals = []
        expected_professionals = []

        for count in range(1, 6):
            professionals.append(self.create_professional().data)
            expected_professionals.append({'id': count, **self.valid_professional})

        request = self.factory.get('/professional', format='json')
        response = professional_general_controller(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(expected_professionals, professionals)
