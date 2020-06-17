import json
import pandas as pd
from datetime import date

try:
    import FlaskApp.fantasy_logic as fantasy_logic
    import FlaskApp.sport_api as sport_api
except:
    import fantasy_logic as fantasy_logic
    import sport_api as sport_api


def read_params(fn):
    d = {}
    try:
        with open(fn, 'r', encoding="utf-8") as file:
            d = json.load(file)
    except FileNotFoundError:
        print("Error. Can't find file " + fn)
        d = {}
    return d


def update_plot_statictics(_tournament_id=None):
    try:
        settings = read_params("FlaskApp/settings.json")
        sports = sport_api.SportsApiMethods(settings)
    except:
        settings = read_params("settings.json")
        sports = sport_api.SportsApiMethods(settings)

    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tournaments"]
    for tour in tournaments:
        team_id = tournaments[tour]['team_id']
        tournament_id = tournaments[tour]['tournament_id']
        season_id = tournaments[tour]['season_id']
        f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports, tour)
        f.get_plot_statistics()


def make_substitutions(_tournament_id=None):
    try:
        settings = read_params("FlaskApp/settings.json")
        sports = sport_api.SportsApiMethods(settings)
    except:
        settings = read_params("settings.json")
        sports = sport_api.SportsApiMethods(settings)
    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tournaments"]
    tour = [tour for tour in tournaments if int(_tournament_id) == tournaments[tour]['tournament_id']][0]
    team_id = tournaments[tour]['team_id']
    tournament_id = tournaments[tour]['tournament_id']
    season_id = tournaments[tour]['season_id']
    f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports)
    team_df = f.getMyFantasyTeam()
    team_df['is_inner_games'] = 1
    team_df = team_df.sort_values(
        by=list(f.sort_best_rules.keys()),
        ascending=list(f.sort_best_rules.values()),
    ).fillna(0).reset_index()
    positions = team_df[team_df['row'] > '0'].groupby(['amplua'])['amplua'].count().to_dict()
    final = f.sendTransfers(team_df, positions)
    return final


def get_myteam_json(_tournament_id):
    try:
        settings = read_params("FlaskApp/settings.json")
        sports = sport_api.SportsApiMethods(settings)
    except:
        settings = read_params("settings.json")
        sports = sport_api.SportsApiMethods(settings)

    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tournaments"]
    tour = [tour for tour in tournaments if int(_tournament_id) == tournaments[tour]['tournament_id']][0]
    team_id = tournaments[tour]['team_id']
    tournament_id = tournaments[tour]['tournament_id']
    season_id = tournaments[tour]['season_id']
    f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports)
    team_df = f.getMyFantasyTeam()
    team_df['is_inner_games'] = 1
    team_df = team_df.sort_values(
        by=list(f.sort_best_rules.keys()),
        ascending=list(f.sort_best_rules.values()),
    ).fillna(0).reset_index()

    columns = ['id',
               'club_id',
               'tag_id',
               'now_id',
               'is_inner_games',
               'plusminus',
               'rebounds',
               'plusminus_place',
               'shtraf_time',
               'goals_place',
               'avg_conceded_goals',
               'goal_passes_place',
               'goal_and_pass_place',
               'shtraf_time_place']

    order_columns = ['name',
                     'avatar',
                     'club',
                     'img']
    columns_list = order_columns + [c for c in team_df.columns if c not in order_columns]
    team_df = team_df[columns_list].drop(columns=columns)
    team_df = team_df.loc[:, (team_df != 0).any(axis=0)]
    team_df = team_df.round({'avg_minutes': 2, 'avg_season': 2, 'avg_goals': 2, 'avg_goal_passes': 2})
    return team_df.to_dict('index')


def get_color_by_state(status):
    if status == 0:
        return 'yellow'
    elif status == 1:
        return 'green'
    elif status == 2:
        return 'orange'
    elif status == -1:
        return 'red'


def create_new_team(_tournament_id=None):
    try:
        settings = read_params("FlaskApp/settings.json")
        sports = sport_api.SportsApiMethods(settings)
    except:
        settings = read_params("settings.json")
        sports = sport_api.SportsApiMethods(settings)
    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tournaments"]
    print(tournaments)
    tour = [tour for tour in tournaments if tournaments[tour]['tournament_id'] == _tournament_id][0]
    team_id = tournaments[tour]['team_id']
    tournament_id = tournaments[tour]['tournament_id']
    season_id = tournaments[tour]['season_id']
    team_df = pd.DataFrame()
    positions_worst = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 3, 2, 2, 1]
    positions = {1: 1, 2: 3, 3: 4, 4: 2}
    teams_limit_send = {}
    players_ids = []
    sum_price = 100
    worst = [1]
    f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports)
    all_players_df = f.getAllFantasyPlayers()
    best_players = f.getBest(team=all_players_df,
                             positions=positions_worst,
                             sum_price=sum_price,
                             teamsLimit=teams_limit_send,
                             my_players=players_ids,
                             max_player_one_team=settings['fantasy_settings']["tournaments"][tour][
                                 'max_player_one_team'])

    df_transfers = f.getNewTeamAfterSubstitions(team_df, worst_players=worst, best_players=best_players)
    df_transfers = df_transfers.sort_values(
        by=list(f.sort_best_rules.keys()),
        ascending=list(f.sort_best_rules.values()),
    ).fillna(0).reset_index()
    final = f.sendTransfers(df_transfers, positions)
    if str(final).lower().find('ok') > -1:
        make_substitutions(_tournament_id=tournament_id)
    else:
        print('not ok')


def make_transfers(check=True, _tournament_id=None):
    # settings = read_params("settings.json")
    try:
        settings = read_params("FlaskApp/settings.json")
        sports = sport_api.SportsApiMethods(settings)
    except:
        settings = read_params("settings.json")
        sports = sport_api.SportsApiMethods(settings)

    try:
        last_try_sub = pd.read_csv("FlaskApp/data.csv")
    except:
        last_try_sub = pd.read_csv("data.csv")
    columns = ["deadline", "status_result", "substitutions", "status"]
    for col in columns:
        if col not in last_try_sub.columns:
            last_try_sub[col] = ""
    x = list(zip(last_try_sub["deadline"], last_try_sub["status_result"], last_try_sub["substitutions"],
                 last_try_sub["status"]))
    key = last_try_sub["tournament_id"]

    dict_last_try = dict(zip(key, x))
    print(dict_last_try)

    deadline_dict = {}
    fantasy_info = sports.getFantasyInfo()
    for idx in range(len(fantasy_info)):
        deadline_dict[fantasy_info.at[idx, 'id']] = fantasy_info.at[idx, 'date']

    settings_fantasy = settings['fantasy_settings']
    tournaments = settings_fantasy["tournaments"]
    url_login = settings_fantasy['url_login']
    login = settings_fantasy['login']
    password = settings_fantasy['password']
    today_dd_mm = date.today().strftime("%d.%m")
    sports = sport_api.SportsApiMethods(settings,
                                        url_login,
                                        login,
                                        password)
    teams = []
    res = []
    print(deadline_dict)
    for tour in tournaments:
        team_id = tournaments[tour]['team_id']
        tournament_id = tournaments[tour]['tournament_id']
        season_id = tournaments[tour]['season_id']
        try:
            r = {"tournament_id": tournament_id, "tournament": tour, "deadline": deadline_dict[team_id]}
        except:
            continue

        if int(tournament_id) in dict_last_try and str(dict_last_try[int(tournament_id)][0]).zfill(5) == deadline_dict[
            team_id]:
            if dict_last_try[tournament_id][1] in [1]:
                # r["status"] = dict_last_try[tournament_id][1]
                r["status"] = dict_last_try[tournament_id][3]
                r["substitutions"] = dict_last_try[tournament_id][2]
                r["status_result"] = dict_last_try[tournament_id][1]
                r["color"] = get_color_by_state(r["status_result"])
                res.append(r)
                continue;

        if deadline_dict[team_id] != today_dd_mm:
            log = 'Турнир %s: %s' % (deadline_dict[team_id], "время для замен еще не пришло")
            print(log)
            r["status"] = "время для замен еще не пришло"
            r["status_result"] = 0
            r["color"] = get_color_by_state(r["status_result"])
            res.append(r)
            continue;
        else:
            log = 'Турнир %s: %s' % (deadline_dict[team_id], "произведены замены")
            print(log)
            r["status"] = "сегодня время замен"
            r["substitutions"] = ""
            r["status_result"] = 2
            r["color"] = get_color_by_state(r["status_result"])
            if check == True:
                res.append(r)
                continue
            elif _tournament_id != None and tournament_id != int(_tournament_id):
                res.append(r)
                continue

        f = fantasy_logic.sportsFantasyLogic(team_id, tournament_id, season_id, sports)
        team_df = f.getMyFantasyTeam().fillna(0)
        team_df['is_inner_games'] = 1
        teams.append(team_df)
        all_players_df = f.getAllFantasyPlayers()

        if len(team_df) > 10:
            worst = f.getWorst(team=team_df, top=settings['fantasy_settings']["tournaments"][tour]['number_subs'])
            positions_worst = list(worst['amplua'])
            positions = team_df[team_df['row'] > '0'].groupby(['amplua'])['amplua'].count().to_dict()
            clubs_ids = list(worst['club_id'])
            players_ids = list(team_df['id'])
            sum_price = 100 - team_df.sum()['price'] + float(worst[['price']].sum())
            teams_limit_send = f.playersInTeamLimit(team_df, club_ids=clubs_ids)
        else:
            team_df = pd.DataFrame()
            positions_worst = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 3, 2, 2, 1]
            positions = {1: 1, 2: 3, 3: 4, 4: 2}
            teams_limit_send = {}
            players_ids = []
            sum_price = 100
            worst = [1]
        best_players = f.getBest(team=all_players_df,
                                 positions=positions_worst,
                                 sum_price=sum_price,
                                 teamsLimit=teams_limit_send,
                                 my_players=players_ids,
                                 max_player_one_team=settings['fantasy_settings']["tournaments"][tour][
                                     'max_player_one_team'])

        df_transfers = f.getNewTeamAfterSubstitions(team_df, worst_players=worst, best_players=best_players)
        df_transfers = df_transfers.sort_values(
            by=list(f.sort_best_rules.keys()),
            ascending=list(f.sort_best_rules.values()),
        ).fillna(0).reset_index()
        final = f.sendTransfers(df_transfers, positions)
        r["status"] = final
        if str(final).lower().find('ok') > -1:
            make_substitutions(_tournament_id=tournament_id)
            r["status_result"] = 1
        else:
            r["status_result"] = -1
        r["color"] = get_color_by_state(r["status_result"])
        r["substitutions"] = str(list(worst['name'])) + " => " + str(list(best_players['name']))
        res.append(r)
    df = pd.DataFrame.from_dict(res)
    try:
        df.to_csv("FlaskApp/data.csv")
    except:
        df.to_csv("data.csv")
    print(res)
    return res
