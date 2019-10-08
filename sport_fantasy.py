import requests
import json
import io
import numpy as np # linear algebra
import pandas as pd
import datetime
import math
import fantasy_logic
import sport_api
from urllib.parse import parse_qs
from datetime import date


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
    settings = read_params("settings.json")
    sports = sport_api.sportsApiMethods(settings)
    deadline_dict = {}
    fantasy_info = sports.getFantasyInfo()
    for idx in range(len(fantasy_info)):
        deadline_dict[fantasy_info.at[idx, 'id']] = fantasy_info.at[idx, 'date']
    url_settings = settings['sport_api']
    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tounaments"]
    url_login = settings_fantasy['url_login']
    login = settings_fantasy['login']
    password = settings_fantasy['password']
    today_dd_mm = date.today().strftime("%d.%m")
    sports = sport_api.sportsApiMethods(settings, 
                                    url_login, 
                                    login, 
                                    password) 
    teams = []
    res = []
    for tour in tournaments:
        team_id =  tournaments[tour] ['team_id']
        tournament_id =  tournaments[tour] ['tournament_id']
        season_id =  tournaments[tour] ['season_id']
        if deadline_dict[team_id] != today_dd_mm:
            log = 'Время замена для турнира %s %s еще не пришло. Сегодня %s' % (tour, deadline_dict[team_id], today_dd_mm) 
            print(log)    
            continue;
        else:
            log = 'Делаю замены для турнира %s' % (tour) 
            print(log)
        res.append(log) 
        f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports)
        team_df = f.getMyFantasyTeam()
        team_df['is_inner_games'] = 1
        teams.append(team_df)
        all_players_df =  f.getAllFantasyPlayers()
    
        if len(team_df) > 10:
            worst = f.getWorst(team = team_df, top = settings['fantasy_settings']["tounaments"][tour]['number_subs'])
            positions_worst = list(worst['amplua'])
            clubs_ids = list(worst['club_id'])
            players_ids = list(team['id'])
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
                                     max_player_one_team = settings['fantasy_settings']["tounaments"][tour]['max_player_one_team'])
    
        df_transfers = f.getNewTeamAfterSubstitions(team_df, worst_players = worst, best_players = best_players)
        f.sendTransfers(df_transfers)
    print(res)
    return res

