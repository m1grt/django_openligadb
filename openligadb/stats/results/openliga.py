# -*- coding: utf-8 -*-
import urllib.request
import json


class LigaApi(object):
    """
    Simple wrapper for openligadb Api.
    """

    def __init__(self):
        self.URL = 'https://www.openligadb.de/api'
        self.SEASON_TEAMS = self.get_data()
        self.SEASON_MATCHES = self.get_match_data_by_league_season()

    def get_data(self):
        """
        return all teams participating in current league season
        """
        data = json.load(
            urllib.request.urlopen(self.URL + '/getavailableteams/bl1/2017')
        )
        return [r for r in data]

    def get_match_data_by_league_season(self):
        """
        return all matche/games for current league season
        """
        data = json.load(
            urllib.request.urlopen(self.URL + '/getmatchdata/bl1/2017')
        )
        return [md for md in data]
