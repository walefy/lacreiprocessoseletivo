from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from professional.views import professional_general_controller
from examination import views


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
        self.valid_examination = {
            'date': '2024-04-09 15:00:00'
        }

    def create_professional(self):
        request = self.factory.post('/professional', self.valid_professional, format='json')
        return professional_general_controller(request)

    def crete_examination(self, professional_id):
        request = self.factory.post(f'/examinations/{professional_id}', self.valid_examination, format='json')
        return views.examination_with_professional_id_controller(request, professional_id)

    def test_create_examination(self):
        professional_id = self.create_professional().data.get('id')

        response = self.crete_examination(professional_id)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual(
            {'id': 1, 'date': '2024-04-09T15:00:00Z', 'professional': professional_id},
            response.data
        )

    def test_find_all_examinations_by_professional_id(self):
        professional_id = self.create_professional().data.get('id')
        examinations = []

        for count in range(1, 6):
            examination = self.crete_examination(professional_id).data
            examinations.append(examination)

        request = self.factory.get(f'/examinations/professional/{professional_id}', format='json')
        response = views.examination_with_professional_id_controller(request, professional_id)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual(examinations, response.data)

    def test_find_examination_by_id(self):
        professional_id = self.create_professional().data.get('id')
        examination = self.crete_examination(professional_id).data
        examination_id = examination.get('id')

        request = self.factory.get(f'/examinations/{examination_id}', format='json')
        response = views.examination_with_id_controller(request, examination_id)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {'id': examination_id, 'date': examination['date'], 'professional': professional_id},
            response.data
        )

    def test_update_examination_by_id(self):
        professional_id = self.create_professional().data.get('id')
        examination = self.crete_examination(professional_id).data
        examination_id = examination.get('id')

        update_payload = {
            'date': '2024-04-10 15:00:00'
        }

        request = self.factory.patch(f'/examinations/{examination_id}', update_payload, format='json')
        response = views.examination_with_id_controller(request, examination_id)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEquals(
            {'id': examination_id, 'date': examination['date'], 'professional': professional_id},
            response.data
        )
        self.assertDictEqual(
            {'id': examination_id, 'date': '2024-04-10T15:00:00Z', 'professional': professional_id},
            response.data
        )

    def test_list_all_examinations(self):
        professional_id = self.create_professional().data.get('id')
        examinations = []

        for count in range(1, 6):
            examination = self.crete_examination(professional_id).data
            examinations.append(examination)

        request = self.factory.get('/examinations', formart='json')
        response = views.examination_general_controller(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual(examinations, response.data)
