from django.test import TestCase, RequestFactory, Client
from django.urls import reverse


class League(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_index_page(self):
        request = self.client.get(reverse('index'))
        self.assertEqual(request.status_code, 200)

    def test_league_page(self):
        request = self.client.get(reverse('league'))
        self.assertEqual(request.status_code, 200)

    def test_search_page(self):
        request = self.client.get(reverse('search'))
        self.assertEqual(request.status_code, 200)

    def test_next_weekend_page(self):
        request = self.client.get(reverse('next_weekend'))
        self.assertEqual(request.status_code, 200)


    def test_team_stats_page(self):
        request = self.client.get(reverse('list_all'))
        self.assertEqual(request.status_code, 200)

    def test_list_all_page(self):
        request = self.client.get('team_stats')
        self.assertEqual(request.status_code, 404)