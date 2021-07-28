# -*- coding: utf-8 -*-
import logging
import os

from django.test import Client, TestCase, override_settings

from job.models import Job
from proj import settings

logger = logging.getLogger(__name__)


class ApiTestCase(TestCase):
    file_path = settings.BASE_DIR / 'test.png'

    def setUp(self):
        self.client = Client()

    @classmethod
    def tearDownClass(cls):
        # очищаем media от файлов
        for f in os.listdir(settings.MEDIA_ROOT):
            os.remove(os.path.join(settings.MEDIA_ROOT, f))
        super().tearDownClass()

    def test_root_url(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_job_gaussian_noise(self):
        with open(self.file_path, mode='rb') as file:
            date = {'image_filter': 'GaussianNoise', 'severity': 2, 'file': file}
            response = self.client.post('/jobs/', date, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('status'), Job.DONE)
            self.assertEqual(response.json().get('image_filter'), 'GaussianNoise')

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_job_rotate(self):
        with open(self.file_path, mode='rb') as file:
            date = {'image_filter': 'Rotate', 'rotate': 90, 'file': file}
            response = self.client.post('/jobs/', date, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('status'), Job.DONE)
            self.assertEqual(response.json().get('image_filter'), 'Rotate')

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_job_add_saturation(self):
        with open(self.file_path, mode='rb') as file:
            date = {'image_filter': 'AddToHueAndSaturation',
                    'value_hue': 255, 'value_saturation': 255, 'per_channel': 'True',
                    'file': file}
            response = self.client.post('/jobs/', date, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('status'), Job.DONE)
            self.assertEqual(response.json().get('image_filter'), 'AddToHueAndSaturation')

    def test_get_job_status_not_dote(self):
        date = {'image_filter': 'AddToHueAndSaturation',
                'value_hue': 255, 'value_saturation': 255, 'per_channel': 'True',
                }
        job = Job.objects.create(**date)
        response = self.client.get('/jobs/{}/'.format(job.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), Job.PENDING)
        self.assertEqual(response.json().get('image_filter'), 'AddToHueAndSaturation')
        self.assertNotIn('file', response.json())

    def test_get_job_status_dote(self):
        date = {'image_filter': 'AddToHueAndSaturation',
                'value_hue': 255, 'value_saturation': 255, 'per_channel': 'True',

                }
        job = Job.objects.create(**date)
        job.status = Job.DONE
        job.save()
        response = self.client.get('/jobs/{}/'.format(job.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), Job.DONE)
        self.assertEqual(response.json().get('image_filter'), 'AddToHueAndSaturation')
        self.assertIn('file', response.json())
