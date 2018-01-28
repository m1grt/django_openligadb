__all__ = ['openliga', 'decorators', 'helpers']
from openliga import LigaApi as Api

api = Api()

SEASON_TEAMS = api.get_data()
SEASON_MATCHES = api.get_match_data_by_league_season()
