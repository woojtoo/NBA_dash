import time

from nba_api.stats.endpoints import LeagueGameLog, CommonPlayerInfo, CommonTeamRoster, PlayerCareerStats
from nba_api.stats.static.teams import get_teams
from nba_api.stats.static.players import get_active_players
import pandas as pd
from requests.exceptions import ReadTimeout

# pd.set_option('display.max_columns', 30)
# pd.set_option('display.width', 1000)


def show_df(df: pd.DataFrame(), rows: int = 10) -> None:
    print(df.head(rows).to_markdown())
    print(f'rows: {len(df)}\n')


# season = LeagueGameLog(season=2021).get_data_frames()[0]
# season.to_csv('data/season_2021.csv', index=False)
season = pd.read_csv('data/season_2021.csv')
show_df(season)


# teams = pd.DataFrame(get_teams())
# teams.to_csv('data/teams.csv', index=False)
teams = pd.read_csv('data/teams.csv')
show_df(teams)

# rosters = pd.DataFrame()
# for team in teams['id'].values:
#     roster = CommonTeamRoster(team, timeout=60).get_data_frames()[0]  # [['TeamID', 'PLAYER_ID', 'BIRTH_DATE', 'POSITION', 'AGE']]
#     rosters = pd.concat([rosters, roster], ignore_index=True)
#     rosters.to_csv('data/rosters.csv', index=False)
rosters = pd.read_csv('data/rosters.csv')
show_df(rosters)

# players = pd.DataFrame(get_active_players())
# show_df(players)

players_stats = pd.read_csv('data/players_stats.csv')
# players_stats = pd.DataFrame(columns=['PLAYER_ID'])
for i, player in enumerate(rosters['PLAYER_ID'].values):
    if player not in players_stats['PLAYER_ID'].values:
        print(i)
        n_try = 1
        success = False
        while not success:
            try:
                print(f'try: {n_try}')
                stats = PlayerCareerStats(player, timeout=60).get_data_frames()[0]
                show_df(stats, 3)
                players_stats = pd.concat([players_stats, stats], ignore_index=True)
                players_stats.to_csv('data/players_stats.csv', index=False)
                success = True
            except ReadTimeout:
                n_try += 1
                time.sleep(2*60)
show_df(players_stats)
# show_df(all_players['PERSON_ID', 'DISPLAY_FIRST_LAST', 'COUNTRY', 'JERSEY', 'POSITION', 'SEASON_EXP', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER'])