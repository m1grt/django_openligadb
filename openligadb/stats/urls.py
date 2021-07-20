# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    IndexView,
    LeagueView,
    ListAllView,
    SearchView,
    NextWeekendView,
    TeamStatsView,
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^league/', LeagueView.as_view(), name='league'),
    url(r'^search/', SearchView.as_view(), name='search'),
    url(r'^next_weekend/', NextWeekendView.as_view(), name='next_weekend'),
    url(r'^list_all/', ListAllView.as_view(), name='list_all'),
    url(r'^team_stats/', TeamStatsView.as_view(), name='team_stats'),
]
