# -*- coding: utf-8 -*-
import urllib2
import json
import datetime
import re

from dateutil import parser


class Wrapper:
    def __init__(self):
        self.url = 'https://www.openligadb.de/api'
        self.matches = self.get_match_data_by_league_season()
        self.stats = self.championship_status()[0]
        self.to_be = self.championship_status()[1]
        self.teams = self.get_data()

    def get_data(self):
        data = json.load(urllib2.urlopen(self.url + '/getavailableteams/bl1/2017'))
        return [r for r in data]

    def get_match_data_by_league_season(self):
        """
        """
        data = json.load(urllib2.urlopen(self.url + '/getmatchdata/bl1/2017'))
        return [md for md in data]

    def process_table_stats(self):
        self.stats = self.championship_status()[0]
        results = {}

        rank = 1
        for club in self.stats:
            count_matches = club['wins'] + club['losses'] + club['draws']
            goals = str(club['goals']) + ':' + str(club['received_goals'])
            gd = int(club['goals']) - int(club['received_goals'])

            results[rank] = {'position': rank, 'team_name': club['team_name'], 'matches': count_matches,
                             'wins': club['wins'], 'draws': club['draws'], 'losses': club['losses'], 'goals': goals,
                             'goal_difference': gd, 'points': club['points']}

            rank += 1
        return results

    def championship_status(self):
        teams = self.get_data()
        chart = {}
        for team in teams:
            chart[team['TeamId']] = {'team_name': team['TeamName'], 'points': 0, 'wins': 0, 'losses': 0, 'draws': 0,
                                     'goals': 0, 'received_goals': 0}

        match_data = self.get_match_data_by_league_season()

        to_be_played = []
        for m in match_data:
            if not m['MatchIsFinished']:
                to_be_played.append(m['MatchID'])
                continue

            t1 = m['Team1']['TeamId']
            goals_t1 = int(m['MatchResults'][-1]['PointsTeam1'])

            t2 = m['Team2']['TeamId']
            goals_t2 = int(m['MatchResults'][-1]['PointsTeam2'])

            data_t1 = chart[t1]
            data_t2 = chart[t2]

            data_t1['goals'] += goals_t1
            data_t2['goals'] += goals_t2
            data_t1['received_goals'] += goals_t2
            data_t2['received_goals'] += goals_t1

            if goals_t1 > goals_t2:
                data_t1['points'] += 3
                data_t1['wins'] += 1
                data_t2['losses'] += 1
            elif goals_t1 < goals_t2:
                data_t2['points'] += 3
                data_t2['wins'] += 1
                data_t1['losses'] += 1
            else:
                data_t1['points'] += 1
                data_t2['points'] += 1
                data_t1['draws'] += 1
                data_t2['draws'] += 1

        return sorted([value for key, value in chart.items()],
                      key=lambda k: (k['points'],
                                     k['goals'] - k['received_goals'],
                                     k['goals']),
                      reverse=True), to_be_played, teams

    def next_weekend(self):
        today = datetime.date.today()
        sat = today + datetime.timedelta((5 - today.weekday()) % 7)
        sun = today + datetime.timedelta((6 - today.weekday()) % 7)

        next_matches = {}
        n = 0
        for m in self.matches:
            match_day = parser.parse(m['MatchDateTime'])
            if m['MatchID'] in self.to_be and match_day.date() == sat or match_day.date() == sun:
                next_matches[n] = {'teams': m['Team1']['TeamName'] + ' vs ' + m['Team2']['TeamName'],
                                   'date': str(match_day)}
                n += 1
        return next_matches

    def all_matches(self):
        all_matches = {}
        n = 0
        for m in self.matches:
            all_matches[n] = {'match': m['Team1']['TeamName'] + ' vs ' + m['Team2']['TeamName'],
                              'date': m['MatchDateTime'], 'status': m['MatchIsFinished'], 'id1': m['Team1']['TeamId'],
                              'id2': m['Team2']['TeamId']}
            n += 1
        return sorted([value for key, value in all_matches.items()],
                      key=lambda k: k['date'], reverse=False)

    def search_team(self, team):
        t = [i for i in self.get_data()]
        results = []
        for i in t:
            try:
                s = re.search(u'{}'.format(team.lower()), u'{}'.format(i['TeamName'].lower()))
                results.append({'name': s.string, 'id': i['TeamId']})
            except:
                pass
        return results

    def get_team_matches(self, tid):
        team_info = {}
        n = 0
        for i in self.all_matches():
            if tid in i.values():
                team_info[n] = {'match': i['match'], 'date': i['date'], 'status': i['status']}
                n += 1

        return team_info

    def get_team_stats(self, name):
        return [ts for ts in self.stats if ts['team_name'].lower() == name][0]