# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from results import SEASON_MATCHES, SEASON_TEAMS, helpers


class IndexView(TemplateView):
    template_name = "index.html"


class LeagueView(TemplateView):
    template_name = "stats/league.html"

    def get_context_data(self, **kwargs):
        context = {'table': self.get_championship_table()}
        return context

    def get_championship_table(self):
        return self.set_championship_table

    @property
    def set_championship_table(self):
        table = helpers.get_championship(SEASON_TEAMS, SEASON_MATCHES)
        return [i for i in helpers.get_championship_table(table).values()]


class SearchView(View):
    template_name = "stats/templates/stats/search.html"

    @staticmethod
    def get(request):
        return HttpResponse(render(request, template_name='stats/search.html'))

    def post(self, request):
        team = self.request.POST.get('team_name')
        table = helpers.search(SEASON_TEAMS, team)
        context = {'table': table}
        return HttpResponse(render(request, template_name='stats/search.html', context=context))


class NextWeekendView(TemplateView):
    template_name = "stats/next_weekend.html"

    def get_context_data(self, **kwargs):
        t = helpers.next_weekend(SEASON_TEAMS, SEASON_MATCHES)
        table = [i for i in t.values()]
        context = {'table': table}
        return context


class ListAllView(TemplateView):
    template_name = "stats/list_all.html"

    def get_context_data(self, **kwargs):
        context = {'table': self.get_list_all()}
        return context

    def get_list_all(self):
        return self.set_list_all

    @property
    def set_list_all(self):
        table = helpers.all(SEASON_MATCHES)
        return [i for i in table]


class TeamStatsView(LeagueView, ListAllView, View):
    template_name = "stats/team_stats.html"

    def __init__(self):
        super(TeamStatsView, self).__init__()

    def get(self, request):
        return HttpResponse(render(request, template_name="stats/team_stats.html", context=None))

    def post(self, request):
        team = self.request.POST.get('name')
        championship = self.get_championship_table()
        tid = self.request.POST.get('tid')
        team_matches = self.get_list_all()
        table = helpers.get_team_matches(team_matches, tid)
        context = {'table_team': helpers.get_team_stats(championship, team),
                   'table_id': [i for i in table.values()]}
        return HttpResponse(render(request, template_name="stats/team_stats.html", context=context))