import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime
import time
import math
from threading import Thread

def separate_n(data, n):
    m = math.ceil(len(data) / n)
    chunk = [data[x : x + m] for x in range(0, len(data), m)]
    return chunk


class sportsFantasyLogic:
    def __init__(self, _team_id, _tournament_id, _season_id, _sport_api):
        self.apiMethods = _sport_api
        self.team_id = _team_id
        self.tournament_id = _tournament_id
        self.season_id = _season_id
        self.df_all_players = pd.DataFrame()  # general informations about players
        self.players_df = pd.DataFrame()  # additional information about players
        self.cur_player_updated = 0
        self.players_dict = {}
        self.num_threads = 20
        self.threads = []
        self.players_additional_fields = pd.DataFrame()
        self.sort_best_rules = {
            "is_injured": 1,
            "is_inner_games": 1,
            "avg_season": 0,
            "avg_goals": 0,
            "avg_minutes": 0,
            "matches": 0,
            "conceded_goals": 1,
        }

    def __getMyFantasyTeamInner(self):
        my_team = self.apiMethods.getMyTeamInfo(self.team_id)
        self.df_my_team = pd.DataFrame(data=my_team)
        return self.df_my_team

    def __setUpdateFields(self, team):
        fields_numeric = ["price", "amplua", "tour", "season"]
        for field in fields_numeric:
            if field in team:
                team[field] = team[field].apply(pd.to_numeric)
        team["id"] = team["id"].astype(int)
        team["amplua"] = team["amplua"].astype(int)
        fields_avg = ["minutes", "season", "goals", "conceded_goals"]
        for field in fields_avg:
            if field in team:
                team["avg_" + field] = team[field] / team["matches"]
        team = team.fillna(0)
        return team

    def __createRowAndOrders(self, team):
        team = team.reset_index(drop=True)
        i = 0
        for idx in range(len(team)):
            if i < 11:
                team.at[idx, "row"] = team.at[idx, "amplua"]
                team.at[idx, "order"] = 0
            else:
                team.at[idx, "order"] = i - 10
                team.at[idx, "row"] = 0
            i += 1
        team = team.fillna(0)
        return team

    def getMyFantasyTeam(self):
        self.__getMyFantasyTeamInner()
        if len(self.df_my_team) > 1:
            self.__setAdditionalsMyFantasyTeamMetrics()
            return self.df_my_team_all
        else:
            return self.df_my_team

    def getAllFantasyPlayers(self):
        self.__getAllPlayersTournamentInner()
        return self.df_all_players


    def __getAdditionalInfoApi(self, players, num_thread):
        for player_id in players:
            # if self.cur_player_updated  == 4:
            #    break;
            status = self.df_all_players[self.df_all_players["id"] == player_id].iloc[0][
                "status"
            ]
            tag = self.df_all_players[self.df_all_players["id"] == player_id].iloc[0][
                "tag_id"
            ]
            name = self.df_all_players[self.df_all_players["id"] == player_id].iloc[0][
                "name"
            ]
            # print('tag is %d, id is %s' % (tag, player_id))
            if tag != 0 and status == False:
                try:
                    res = self.apiMethods.getPlayerStatSeason(
                        tag, self.season_id, self.tournament_id
                    )
                except:
                    time.sleep(secs)
                player = pd.DataFrame(data=res, index=[0])
                if player.iloc[0]["matches"] == 0:
                    del player
                    res = self.apiMethods.getPlayerStatSeason(tag)
                    player = pd.DataFrame(data=res, index=[0])
                    player["is_inner_games"] = 0
                else:
                    player["is_inner_games"] = 1
                print(
                    "Updated player number %d, name %s, search inner %d, cur thread %d"
                    % (self.cur_player_updated, name, player["is_inner_games"], num_thread)
                )
                self.players_additional_fields = pd.concat(
                    [self.players_additional_fields, player]
                )
                # self.players_df = pd.concat([self.players_df, player])

                # del player
                self.df_all_players.loc[
                    self.df_all_players["id"] == player_id, "status"
                ] = True
                self.cur_player_updated += 1
            elif tag == 0:
                print("Updated player number %d, cur thread %d" % (self.cur_player_updated, num_thread))
                self.df_all_players.loc[
                    self.df_all_players["id"] == player_id, "status"
                ] = True
                self.cur_player_updated += 1    

    def __setAdditionalsMyFantasyTeamMetrics(self):
        players = list(self.df_my_team["tag_id"])
        players_df = pd.DataFrame()
        for tag in players:
            res = self.apiMethods.getPlayerStatSeason(
                tag, self.season_id, self.tournament_id
            )
            player = pd.DataFrame(data=res, index=[0])
            players_df = pd.concat([players_df, player])

        self.df_my_team_all = pd.merge(
            self.df_my_team, players_df, on="tag_id", suffixes=("", "_all"), how="left"
        )
        self.__setUpdateFields(self.df_my_team_all)
        return self.df_my_team_all

    # logic can recover after internet connection distruption
    def __getAllPlayersTournamentInner(self):
        month = int(datetime.datetime.now().strftime("%m"))

        if len(self.df_all_players) == 0:
            self.players_additional_fields = pd.DataFrame()
            self.df_all_players = self.apiMethods.getAllTeamInfo(self.tournament_id)
            self.df_all_players["status"] = False
            self.df_all_players = self.df_all_players.rename(
                index=str, columns={"points": "season"}
            )
            dic = self.apiMethods.getPlayersDict(
                self.season_id,
                self.tournament_id,
                month=month,
                list_ids=list(self.df_all_players["id"]),
            )
            self.df_all_players["tag_id"] = self.df_all_players["id"].apply(
                lambda x: dic[x] if x in dic else 0
            )
            print("finish to create team")

        players = list(
            self.df_all_players[self.df_all_players["status"] == False]["id"]
        )
        print("Count players in tournament %d " % len(players))
        if len(self.players_df) == 0:
            self.players_df = pd.DataFrame()


        players_chunk = separate_n(players, self.num_threads)
        for i in range(1, self.num_threads + 1):
            players_thread = players_chunk[i - 1]
            t = Thread(target=self.__getAdditionalInfoApi, args=(players_thread, i))
            self.threads.append(t)
            print("start thread number %d" % i)
            t.start()

        for i in range(0, self.num_threads):
            t.join()

        self.df_all_players = pd.merge(
            self.df_all_players,
            self.players_additional_fields,
            on="tag_id",
            suffixes=("", "_all"),
            how="left",
        ).reset_index(drop=True)

        self.df_all_players = self.__setUpdateFields(self.df_all_players)
        return self.df_all_players.reset_index(drop=True)

    def playersInTeamLimit(self, team, club_ids=None):
        teams_limit = (
            team[["id", "club_id"]].groupby(["club_id"]).count().to_dict()["id"]
        )
        print(teams_limit)
        if club_ids != None:
            for w in club_ids:
                teams_limit[w] = teams_limit[w] - 1
        return teams_limit

    def getWorst(self, team, top=None):
        ascending2 = [1 - v for v in self.sort_best_rules.values()]
        res = team.sort_values(
            by=list(self.sort_best_rules.keys()), ascending=ascending2
        )
        if top == None:
            top = len(team)
        return res[0:top].reset_index(drop=True)

    def __getSearchingListPlayers(self, positions):
        result_list = []
        for i in range(len(positions)):
            result_list.append({"total": 0, "cur": 0, "shift": 0, "pos": positions[i]})

        count_list = [0] * len(positions)
        count_dic = dict(zip(positions, count_list))
        i = 0
        for pos in positions:
            result_list[i]["pos"] = pos
            count_dic[pos] += 1
            result_list[i]["cur"] = count_dic[pos] - 1
            i += 1
        print(count_dic)
        for i in range(len(positions)):
            result_list[i]["shift"] = count_dic[result_list[i]["pos"]]
        return result_list

    def __NextPlayer(self, search_list, cur_position):
        next_pos = search_list[cur_position]["cur"] + search_list[cur_position]["shift"]
        if next_pos < search_list[cur_position]["total"]:
            search_list[cur_position]["cur"] = next_pos
            return True
        else:
            return False

    def __checkIfSearchFinish(self, res):
        finish = True
        for r in res:
            if r["cur"] + r["shift"] < r["total"]:
                return False
        return finish

    def __getDistanceToVector(self, from_vector, to_vector=None):
        length = len(from_vector)
        if to_vector == None:
            to_vector = [0] * length
        res = 0
        for i in range(length):
            res += (from_vector[i] - to_vector[i]) * (from_vector[i] - to_vector[i])
        return math.sqrt(res)

    def __getDFBySearchList(self, search_list, dfs_search):
        df_players = pd.DataFrame()
        i = 0
        for player in search_list:
            shift_df = player["cur"]
            df_plr = dfs_search[i][shift_df : shift_df + 1]
            df_players = pd.concat([df_players, df_plr])
            i += 1
        return df_players

    def __checkIfTeamLimitOk(self, df_players, teamsLimit, max_player_one_team):
        print(teamsLimit)
        teamsLimitTest = teamsLimit.copy()
        res = True
        for club_id in list(df_players["club_id"]):
            if club_id in teamsLimitTest:
                teamsLimitTest[club_id] += 1
            else:
                teamsLimitTest[club_id] = 1
            if teamsLimitTest[club_id] > max_player_one_team:
                return False
        return res

    def __checkIfNotInYourTeam(self, df_players, my_players):
        res = True
        for player_id in list(df_players["id"]):
            if player_id in my_players:
                return False
        return res

    def getDictionaryFromTeam(self, sort_team):
        transfers = {}
        transfers["order[]"] = []
        transfers["suidaval"] = "wKgBoVzjp4oxjlQEfGZzAg=="
        for i in range(len(sort_team)):
            key = sort_team[i : i + 1]["id"].to_string(index=False).replace(" ", "")
            order = int(sort_team[i : i + 1]["order"])
            is_captain = int(sort_team[i : i + 1]["isCaptain"])
            if order > 0:
                transfers["order[]"].append(int(key))
            if is_captain > 0:
                transfers["captain"] = int(key)
            key = int(key)
            value = int(sort_team[i : i + 1]["amplua"])
            transfers["players[%d]" % key] = value
        return transfers

    def sendTransfers(self, df_transfers):
        transfers = self.getDictionaryFromTeam(df_transfers)
        return self.apiMethods.sendTransfers(transfers, self.team_id)

    def __getDistinceFromAVGPlayer(self, df_players, avg_price):
        vector_from = list(df_players["price"])
        vector_to = [avg_price] * len(vector_from)
        return self.__getDistanceToVector(vector_from, vector_to)

    def __printDF(self, df_players, avg_distance, search_price, error):
        player_names = "/".join(list(df_players["name"]))
        player_prices = "/".join([str("%.1f" % i) for i in list(df_players["price"])])
        player_ampluas = "/".join([str(i) for i in list(df_players["amplua"])])
        player_avg_points = "/".join(
            [str("%.1f" % i) for i in list(df_players["avg_season"])]
        )
        print(
            "%s with prices % s, ampluas %s, total price %s, avg dist %.1f, search price %.1f, avg_points %s, status %s"
            % (
                player_names,
                player_prices,
                player_ampluas,
                str(df_players.sum()["price"]),
                avg_distance,
                search_price,
                player_avg_points,
                error,
            )
        )
        return df_players

    def getNewTeamConcat(self, team, worst_players, best_players):
        team_new = team.copy()
        if len(team_new) > 1:
            worst_ids = list(worst_players["id"])
            team_new = team_new.drop(
                team_new[team_new["id"].isin(worst_ids)].index
            )  # delete worst players
        team_new = (
            pd.concat([team_new, best_players])
            .sort_values(
                by=list(self.sort_best_rules.keys()),
                ascending=list(self.sort_best_rules.values()),
            )
            .reset_index(drop=True)
        )
        team_new = team_new.fillna(0)
        return team_new

    def getNewTeamAfterSubstitions(self, team, worst_players, best_players):
        team_new = self.getNewTeamConcat(team, worst_players, best_players)
        rows_orders = team_new[["id", "row"]].groupby(["row"]).count().to_dict()["id"]
        rows_orders_new = {}
        rows_orders_x = {}
        for r in rows_orders:
            rows_orders_new[int(r)] = 0
            rows_orders_x[int(r)] = rows_orders[r]
        order = 0
        for idx in range(len(team_new)):
            if idx == 0:
                team_new.at[idx, "isCaptain"] = 1
            else:
                team_new.at[idx, "isCaptain"] = 0
            cur_player = team_new[idx : idx + 1]
            amplua = int(cur_player["amplua"])
            if rows_orders_new[amplua] + 1 <= rows_orders_x[amplua]:
                team_new.at[idx, "row"] = int(cur_player["amplua"])
                rows_orders_new[amplua] = rows_orders_new[amplua] + 1
                team_new.at[idx, "order"] = 0
            else:
                team_new.at[idx, "row"] = 0
                order += 1
                team_new.at[idx, "order"] = order
        return team_new

    def getBest(
        self,
        team,
        top=None,
        positions=[],
        sum_price=None,
        teamsLimit=None,
        my_players=[],
        max_player_one_team=2,
    ):

        if positions != []:
            team = team[team["amplua"].isin(positions)]
            team = team[~team["id"].isin(my_players)]
            print("len of total df % d" % (len(team)))
            dfs_search = []  # list of df for each position
            count_players = 0
            search_list = self.__getSearchingListPlayers(positions)
            i = 0
            for amplua in positions:
                df = team[team["amplua"] == amplua].sort_values(
                    by=list(self.sort_best_rules.keys()),
                    ascending=list(self.sort_best_rules.values()),
                )
                print("len of df % d, amplua %d" % (len(df), amplua))
                search_list[i]["total"] = len(df)  # set total players for each position
                dfs_search.append(df)
                i += 1

        while self.__checkIfSearchFinish(search_list) != True:
            df_players = pd.DataFrame()
            for cur_position in range(len(search_list)):  # for each position
                df_position = dfs_search[cur_position]
                if self.__NextPlayer(search_list, cur_position):
                    df_players = self.__getDFBySearchList(search_list, dfs_search)
                    avg_distance = self.__getDistinceFromAVGPlayer(
                        df_players, sum_price * 1.0 / 3
                    )
                    price = float(df_players.sum()["price"])
                    if not self.__checkIfNotInYourTeam(df_players, my_players):
                        error = "error.player exists in your team"
                    elif not self.__checkIfTeamLimitOk(
                        df_players, teamsLimit, max_player_one_team
                    ):
                        error = "error.exceded your team limit"
                    else:
                        error = "ok"
                    res_df = self.__printDF(df_players, avg_distance, sum_price, error)
                    if (price <= sum_price) and (error == "ok"):
                        if "row" not in df.columns:
                            res_df = self.__createRowAndOrders(res_df)
                        return res_df
