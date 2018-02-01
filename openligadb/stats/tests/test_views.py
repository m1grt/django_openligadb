import json

from django.test import TestCase, RequestFactory, Client
from test_plus.test import TestCase as TestPlus
from django.urls import reverse
from stats.views import LeagueView, SearchView
from stats import forms
from urllib import urlencode


class League(TestPlus):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_index_page(self):
        request = self.client.get(reverse('index'))
        self.assertEqual(request.status_code, 200)

    def test_lague_page_response(self):
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

class LeagueViewTest(League):

    def test_league_page_returned_data(self):
        request = self.client.get(reverse('league'))
        stats = ['points', 'draws', 'goals', 'wins']
        [self.assertTrue(stat, request.context) for stat in stats]

class SearchViewTest(League):

    def test_league_page_returned_data(self):
        response = self.client.get(reverse('search'), {'team_name': 'borussia d'})
        self.assertTrue(u'borussia dortmund', response.context['table'][0]['name'])