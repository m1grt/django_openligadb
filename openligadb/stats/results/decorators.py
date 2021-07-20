# -*- coding: utf-8 -*-
import datetime
import re

from dateutil import parser


def all_matches(f):
    def wrapped(*args):
        """
        return list of all matches for current league season
        """
        all_matches = {}
        n = 0
        for m in args[0]:
            all_matches[n] = {
                'match': m['Team1']['TeamName']
                + ' vs '
                + m['Team2']['TeamName'],
                'date': m['MatchDateTime'],
                'status': m['MatchIsFinished'],
                'id1': m['Team1']['TeamId'],
                'id2': m['Team2']['TeamId'],
            }
            n += 1
        return sorted(
            [value for key, value in all_matches.items()],
            key=lambda k: k['date'],
            reverse=False,
        )

    return wrapped


def set_championship(f):
    def wrapped(*args):
        """
        return all stats for teams in the league.
        """
        chart = {}
        for team in args[0]:
            chart[team['TeamId']] = {
                'team_name': team['TeamName'],
                'points': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'goals': 0,
                'received_goals': 0,
            }

        to_be_played = []
        for m in args[1]:
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

        return (
            sorted(
                [value for key, value in chart.items()],
                key=lambda k: (
                    k['points'],
                    k['goals'] - k['received_goals'],
                    k['goals'],
                ),
                reverse=True,
            ),
            to_be_played,
        )

    return wrapped


def set_championship_table(f):
    def wrapped(*args):
        """
        calculating required point and return season current ranking.
        """
        club = args[0][0]
        results = {}
        rank = 1
        for i in range(len(club)):
            count_matches = (
                club[i]['wins'] + club[i]['losses'] + club[i]['draws']
            )
            goals = (
                str(club[i]['goals']) + ':' + str(club[i]['received_goals'])
            )
            gd = int(club[i]['goals']) - int(club[i]['received_goals'])

            results[rank] = {
                'position': rank,
                'team_name': club[i]['team_name'],
                'matches': count_matches,
                'wins': club[i]['wins'],
                'draws': club[i]['draws'],
                'losses': club[i]['losses'],
                'goals': goals,
                'goal_difference': gd,
                'points': club[i]['points'],
            }
            rank += 1
        return results

    return wrapped


def next(f):
    def wrapped(*args):
        """
        return next weekend match/games.
        """
        today = datetime.date.today()
        sat = today + datetime.timedelta((5 - today.weekday()) % 7)
        sun = today + datetime.timedelta((6 - today.weekday()) % 7)

        next_matches = {}
        n = 0
        for m in args[1]:
            match_day = parser.parse(m['MatchDateTime'])
            if (
                m['MatchID'] in args[1]
                and match_day.date() == sat
                or match_day.date() == sun
            ):
                next_matches[n] = {
                    'teams': m['Team1']['TeamName']
                    + ' vs '
                    + m['Team2']['TeamName'],
                    'date': str(match_day),
                }
                n += 1
        return next_matches

    return wrapped


def search_team(f):
    def wrapped(*args):
        """
        search for team, and return name with id
        """
        t = [i for i in args[0]]
        results = []
        for i in t:
            try:
                s = re.search(
                    u'{}'.format(args[1].lower()),
                    u'{}'.format(i['TeamName'].lower()),
                )
                results.append({'name': s.string, 'id': i['TeamId']})
            except:
                pass
        return results

    return wrapped


def set_team_matches(f):
    def wrapped(*args):
        """
        find all games for the team we searched
        """
        team_info = {}
        n = 0
        for i in args[0]:
            if int(args[1]) == int(i['id1']) or int(args[1]) == int(i['id2']):
                team_info[n] = {
                    'match': i['match'],
                    'date': i['date'],
                    'status': i['status'],
                }
                n += 1

        return team_info

    return wrapped


def set_team_stats(f):
    def wrapped(*args):
        """
        return team current position and stats in the ranking table.
        """
        return [
            ts for ts in args[0] if ts['team_name'].lower() == args[1].lower()
        ][0]

    return wrapped
