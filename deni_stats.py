# shawn

from nba_api.stats.endpoints import (
    playercareerstats,
    playergamelog,
    leaguedashplayerstats,
    leaguedashteamstats,
    teamgamelogs
)
from nba_api.stats.static import players, teams
import json
from datetime import datetime
import time
import os
import pandas as pd

SEASON_START_DATE = "2025-10-20T00:00:00"

# Abbreviation to Team ID dict here

#         "Game": 8,
#         "Opponent": "GSW",
#         "Prev_5_Points": 32.2,
#         "Prev_5_FG%": 53.3,
#         "Prev_5_TS%":
#         "Prev_5_eFG%":
#         "Prev_5_USG%":
#         "PPG_Vs_Opp":
#         "Opp_Def_Rating": 109.6,
#         "Is_Home": 0,
#         "Is_B2B":
#         "Over_Under": 28.5,
#         "Label": 1

# Deni is player
player = [p for p in players.get_players() if p['full_name'] == 'Deni Avdija'][0]
deni_id = player['id']

"""
playergamelog Columns: 
['SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 'WL',
       'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
       'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE']

leaguedashteamstats Columns:
Index(['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'E_OFF_RATING',
       'OFF_RATING', 'E_DEF_RATING', 'DEF_RATING', 'E_NET_RATING',
       'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT',
       'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'E_PACE', 'PACE',
       'PACE_PER40', 'POSS', 'PIE', 'GP_RANK', 'W_RANK', 'L_RANK',
       'W_PCT_RANK', 'MIN_RANK', 'OFF_RATING_RANK', 'DEF_RATING_RANK',
       'NET_RATING_RANK', 'AST_PCT_RANK', 'AST_TO_RANK', 'AST_RATIO_RANK',
       'OREB_PCT_RANK', 'DREB_PCT_RANK', 'REB_PCT_RANK', 'TM_TOV_PCT_RANK',
       'EFG_PCT_RANK', 'TS_PCT_RANK', 'PACE_RANK', 'PIE_RANK'],
      dtype='object')

leaguedashplayerstats Columns:
Index(['PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION',
       'AGE', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
       'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
       'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS',
       'NBA_FANTASY_PTS', 'DD2', 'TD3', 'WNBA_FANTASY_PTS', 'GP_RANK',
       'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK',
       'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK',
       'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK',
       'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK',
       'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK',
       'DD2_RANK', 'TD3_RANK', 'WNBA_FANTASY_PTS_RANK', 'TEAM_COUNT'],
      dtype='object')

teamgamelogs Columns:
Index(['SEASON_YEAR', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
       'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
       'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS',
       'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK',
       'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK',
       'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK',
       'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK',
       'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'AVAILABLE_FLAG'],
      dtype='object')

"""

# Get all player stats
p_seasonstats = leaguedashplayerstats.LeagueDashPlayerStats(season='2025-26').get_data_frames()[0]

# Deni's season stats
deni_season_stats = p_seasonstats[p_seasonstats['PLAYER_ID'] == deni_id].iloc[0]
deni_ppg = deni_season_stats['PTS'] / deni_season_stats['GP']

# Deni's game by game stats
p_gamelog_26 = playergamelog.PlayerGameLog(player_id=deni_id, season='2025-26').get_data_frames()[0]
p_gamelog_25 = playergamelog.PlayerGameLog(player_id=deni_id, season='2024-25').get_data_frames()[0]
p_gamelog = pd.concat([p_gamelog_26, p_gamelog_25], ignore_index=True)

# Blazers game by game stats
BLAZERS_ID = deni_season_stats['TEAM_ID']
t_gamelog_26 = teamgamelogs.TeamGameLogs(team_id_nullable=BLAZERS_ID, season_nullable='2025-26').get_data_frames()[0]
t_gamelog_25 = teamgamelogs.TeamGameLogs(team_id_nullable=BLAZERS_ID, season_nullable='2025-26').get_data_frames()[0]
t_gamelog = pd.concat([t_gamelog_26, t_gamelog_25], ignore_index=True)

# filter games that started in 2025-26 season
curr_season_t_logs = t_gamelog.loc[t_gamelog['GAME_DATE'] > SEASON_START_DATE]

# Sort games by most recent game, reverse list
# p_gamelog = p_gamelog.sort_values("GAME_DATE").reset_index(drop=True)
# curr_season_t_logs = curr_season_t_logs.sort_values("GAME_DATE").reset_index(drop=True)

dataset = []


for i in range((len(p_gamelog) - 5)):

    last5 = p_gamelog.iloc[i+1:i+6]

    # Player stats
    pts = last5['PTS'].sum()
    fga = last5['FGA'].sum()
    fgm = last5['FGM'].sum()
    fta = last5['FTA'].sum()
    fg3m = last5['FG3M'].sum()
    tov = last5['TOV'].sum()
    minutes = last5['MIN'].sum()

    # Matching 5 team games — simplest is same index slice
    team_last5 = t_gamelog.iloc[i+1:i+6]

    tfga = team_last5['FGA'].sum()
    tfta = team_last5['FTA'].sum()
    ttov = team_last5['TOV'].sum()

    Prev_5_Points = pts / 5
    Prev_5_FG = fgm / fga if fga > 0 else 0
    Prev_5_TS = pts / (2 * (fga + 0.44 * fta)) if (fga + 0.44 * fta) else 0
    Prev_5_eFG = (fgm + 0.5 * fg3m) / fga if fga > 0 else 0
    Prev_5_USG = ((fga + 0.44 * fta + tov) * 240) / (minutes * (tfga + 0.44 * tfta + ttov)) * 100 if (minutes * (tfga + 0.44 * tfta + ttov)) > 0 else 0

    game_entry = {
        "Game": int(len(p_gamelog) - i),
        "Opponent": p_gamelog.iloc[i]['MATCHUP'].split(" ")[-1],
        "Prev_5_Points": Prev_5_Points,
        "Prev_5_FG": Prev_5_FG,
        "Prev_5_TS": Prev_5_TS,
        "Prev_5_eFG": Prev_5_eFG,
        "Prev_5_USG": Prev_5_USG,
        "Is_Home": 1 if "vs" in p_gamelog.iloc[i]['MATCHUP'] else 0
    }

    dataset.append(game_entry)

with open("deni_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)

print("Saved", len(dataset), "games to deni_dataset.json")
