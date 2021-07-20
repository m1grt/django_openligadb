# -*- coding: utf-8 -*-
from . import decorators


@decorators.all_matches
def all(*args):
    return


@decorators.set_championship
def get_championship(SEASON_TEAMS, SEASON_MATCHES):
    return


@decorators.set_championship_table
def get_championship_table(*args):
    return


@decorators.next
def next_weekend(SEASON_TEAMS, SEASON_MATCHES):
    return SEASON_MATCHES, get_championship(SEASON_TEAMS, SEASON_MATCHES)[1]


@decorators.search_team
def search(*args):
    return


@decorators.set_team_matches
def get_team_matches(*args):
    return


@decorators.set_team_stats
def get_team_stats(*args):
    return get_championship_table()
