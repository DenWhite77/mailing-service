from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    def test_home_page_status(self):
        # Проверяем, что главная страница открывается
        response = self.client.get(reverse('mailing:home'))
        self.assertEqual(response.status_code, 200)
