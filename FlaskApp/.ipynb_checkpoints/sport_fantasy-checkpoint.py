import requests
import json
import io
import numpy as np # linear algebra
import pandas as pd
import datetime
import math
#import fantasy_logic as fantasy_logic
#import sport_api as sport_api
from urllib.parse import parse_qs
from datetime import date


try:
    import FlaskApp.fantasy_logic as fantasy_logic
    import FlaskApp.sport_api as sport_api
except:
    import fantasy_logic as fantasy_logic
    import sport_api as sport_api
    
def read_params(fn): 
    d ={} 
    try:
        with open(fn, 'r',encoding="utf-8") as file: 
            d = json.load(file) 
    except FileNotFoundError:
        print ("Error. Can't find file " + fn)
        d = {}
    return d 

def make_subs():
    #settings = read_params("settings.json")
    try:
        settings = read_params("FlaskApp/settings.json")
    except:
        settings = read_params("settings.json")
    sports = sport_api.sportsApiMethods(settings)
    deadline_dict = {}
    fantasy_info = sports.getFantasyInfo()
    for idx in range(len(fantasy_info)):
        deadline_dict[fantasy_info.at[idx, 'id']] = fantasy_info.at[idx, 'date']
    url_settings = settings['sport_api']
    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tournaments"]
    url_login = settings_fantasy['url_login']
    login = settings_fantasy['login']
    password = settings_fantasy['password']
    today_dd_mm = date.today().strftime("%d.%m")
    sports = sport_api.sportsApiMethods(settings, 
                                    url_login, 
                                    login, 
                                    password) 
    teams = []
    res = {}
    for tour in tournaments:
        team_id =  tournaments[tour] ['team_id']
        tournament_id =  tournaments[tour] ['tournament_id']
        season_id =  tournaments[tour] ['season_id']
        
        if deadline_dict[team_id] != today_dd_mm and tournament_id != 246:
            log = 'Турнир %s: %s' % (deadline_dict[team_id], "время для замен еще не пришло") 
            print(log) 
            res[tour] = {"deadline":deadline_dict[team_id], "status":"время для замен еще не пришло"}  
            continue;
        else:
            log = 'Турнир %s: %s' % (deadline_dict[team_id], "произведены замены") 
            print(log)
            res[tour] = {"deadline":deadline_dict[team_id], "status":"произведены замены", "substitutions":""}  
        f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports)
        team_df = f.getMyFantasyTeam()
        team_df['is_inner_games'] = 1
        teams.append(team_df)
        all_players_df =  f.getAllFantasyPlayers()
    
        if len(team_df) > 10:
            worst = f.getWorst(team = team_df, top = settings['fantasy_settings']["tournaments"][tour]['number_subs'])
            positions_worst = list(worst['amplua'])
            clubs_ids = list(worst['club_id'])
            players_ids = list(team_df['id'])
            sum_price = float(worst[['price']].sum())
            teams_limit_send =  f.playersInTeamLimit(team_df, club_ids = clubs_ids)
        else:
            team_df = pd.DataFrame()
            positions_worst = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 3, 2, 2, 1]
            teams_limit_send = {}
            players_ids = []
            sum_price = 100
            worst = [1]
        best_players = f.getBest(team = all_players_df, 
                                     positions = positions_worst, 
                                     sum_price = sum_price, 
                                     teamsLimit = teams_limit_send, 
                                     my_players = players_ids, 
                                     max_player_one_team = settings['fantasy_settings']["tournaments"][tour]['max_player_one_team'])
    
        df_transfers = f.getNewTeamAfterSubstitions(team_df, worst_players = worst, best_players = best_players)
        final = f.sendTransfers(df_transfers)
        res[tour]["status"] = final 
        res[tour]["substitutions"] = str(list(worst['name'])) + " => " + str(list(best_players['name'])) 
        df = pd.DataFrame.from_dict(res, orient="index") 
        df.to_csv("FlaskApp/data.csv")
    print(res)
    return res

