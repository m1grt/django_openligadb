# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .results import openliga_wrapper

wrapper = openliga_wrapper.Wrapper()


def index(request):
    return render(request, 'index.html')


def bundesliga(request):
    t = wrapper.process_table_stats()
    table = [i for i in t.values()]
    context = {'table': table}
    return render(request, 'stats/bundesliga.html', context)


def follow(request):
    t = wrapper.next_weekend()
    table = [i for i in t.values()]
    context = {'table': table}
    return render(request, 'stats/follow.html', context)


def all_matches(request):
    table = wrapper.all_matches()
    context = {'table': table}
    return render(request, 'stats/allmatches.html', context)


def search(request):
    if request.method == 'POST':
        try:
            team = request.POST.get('team_name')
            table = wrapper.search_team(team)
            context = {'table': table}
            return render(request, 'stats/search.html', context)
        except:
            pass
    else:
        return render(
            request,
            'stats/search.html',
        )


def team_stats(request):
    if request.method == 'POST':
        try:
            team = request.POST.get('name')
            table_team = wrapper.get_team_stats(team)
            tid = request.POST.get('tid')
            table = wrapper.get_team_matches(int(tid))
            table_id = [i for i in table.values()]
            return render(request, 'stats/info.html', {
                'table_team': table_team,
                'table_id': table_id
            })
        except:
            pass
    else:
        return render(
            request,
            'stats/info.html',
        )
