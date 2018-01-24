# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^bundesliga/', views.bundesliga, name='bundesliga'),
    url(r'^search/', views.search, name='search'),
    url(r'^follow/', views.follow, name='follow'),
    url(r'^allmatches/', views.all_matches, name='allmatches'),
    url(r'^team_stats/', views.team_stats, name='stats'),
]