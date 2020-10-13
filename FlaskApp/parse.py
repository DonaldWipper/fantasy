from bs4 import BeautifulSoup
import requests
import re
import datetime
import json
import pandas as pd
from SQLWorker import SQLWorker
from environs import Env
from sport_api import SportsApiMethods


def read_params(fn):
    d = {}
    try:
        with open(fn, "r", encoding="utf-8") as file:
            d = json.load(file)
    except FileNotFoundError:
        print("Error. Can't find file " + fn)
        d = {}
    return d





def get_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_digit(string):
    players_total = string.strip()
    if get_numbers(players_total):
        number = re.search(r"\d+", players_total.strip()).group()
        players_total = int(number)
        return players_total


all_tournaments = []


class ParserClass:
    def __init__(self):
        env = Env()
        env.read_env()
        self.sql_worker = SQLWorker(db_string=env.str("DB_CONN_STR"))
        try:
            self.settings = read_params("FlaskApp/settings.json")
            self.sports = SportsApiMethods(self.settings)
        except:
            self.settings = read_params("settings.json")
            self.sports = SportsApiMethods(self.settings)

        self.headers = self.settings["headers"]

    def get_tour_points(self, key):
        players_stat = self.settings["sql"]["players_stat"]
        team_id = self.settings["fantasy_settings"]["tournaments"][key]["team_id"]
        tours_stats = self.sports.getMyTeamInfoAllTours(team_id=team_id).reset_index()
        if len(tours_stats) == 0:
            return
        all_tournaments.append(tours_stats)
        tours_stats["points"] = tours_stats.apply(
            lambda x: str(x["points"]).replace("-", "0"), axis=1
        )
        # tours_stats = tours_stats[tours_stats["row"] != "0"]
        tours_stats["points"] = tours_stats["points"].astype(int)
        tours_stats = tours_stats.where(pd.notnull(tours_stats), None)
        tours_stats["team_id"] = team_id
        self.sql_worker.insert_duplicate_df(tours_stats, table_name=players_stat)
        return 'OK'

    def save_deadlines_data(self):
        deadlines_table = self.settings["sql"]["deadlines"]
        url_menu = self.settings["sport_api"]["url_fantasy_menu"]
        r = requests.get(url_menu, headers=self.headers).json()
        main_df = pd.DataFrame(data=r["data"]["items"])
        txt = requests.get(
            self.settings["sport_api"]["url_fantasy"], headers=self.headers
        ).text
        soup = BeautifulSoup(txt, features="lxml")
        tournaments = soup.findAll("div", {"class": "league"})
        teams = soup.findAll("div", {"class": "overBox"})
        data_tournaments = []
        data_teams = []
        for item in tournaments:
            tour_info = {}
            x = item.text.strip().replace("\n", "").split("\r")
            x[1] = get_digit(x[1])
            x[2] = get_digit(x[2])
            tour_info["tournament_name"] = x[0]
            tour_info["players_total"] = x[1]
            tour_info["leagues_count"] = x[2]
            tour_info["tournament_id"] = get_digit(
                item.findAll("h4")[0].find_all("a", href=True)[0]["href"]
            )
            tour_info["tournament_url"] = item.findAll("h4")[0].find_all(
                "a", href=True
            )[0]["href"]
            data_tournaments.append(tour_info)

        for item in teams:
            team_info = {}
            x = item.text.strip().replace("\n", "").split("\r")
            x[1] = get_digit(x[1])
            x[2] = get_digit(x[2])
            team_info["team_name"] = x[0]
            team_info["points"] = x[1]
            team_info["place"] = x[2]
            team_info["deadline_time"] = x[3].split("|")[1]
            team_info["team_id"] = get_digit(item.find_all("a", href=True)[0]["href"])
            data_teams.append(team_info)
        tours_df = pd.DataFrame(data=data_tournaments)
        items_df = pd.DataFrame(data=data_teams)
        res_df = pd.concat([tours_df, items_df], axis=1, sort=False)
        rr = main_df.merge(res_df, left_on="id", right_on="team_id")
        rr["deadline_datetime"] = (
            str(datetime.datetime.now().year)
            + " "
            + rr["date"]
            + " "
            + rr["deadline_time"]
        )
        rr["deadline"] = rr.apply(
            lambda x: datetime.datetime.strptime(
                str(datetime.datetime.now().year)
                + " "
                + x["date"]
                + " "
                + x["deadline_time"],
                "%Y %d.%m %H:%M",
            ),
            axis=1,
        )
        rr["deadline_ts"] = rr.apply(lambda x: x["deadline"].timestamp(), axis=1)
        dict_columns_rename = {
            "link": "team_link",
        }

        rr = rr.rename(columns=dict_columns_rename)
        table_columns = self.sql_worker.get_columns(deadlines_table)
        insert_columns = [column for column in rr.columns if column in table_columns]
        xx = rr[insert_columns]
        xx.loc[:, "deadline"] = xx.loc[:, "deadline"].astype(str)
        xx = xx.where(pd.notnull(xx), None)
        self.sql_worker.insert_duplicate_df(table_name=deadlines_table, df=xx)


def run():
    parser = ParserClass()
    print("load deadlines")
    parser.save_deadlines_data()
    print("load players stat")
    tournaments = parser.settings["fantasy_settings"]["tournaments"]
    for tour in tournaments:
        print(tour)
        print(parser.get_tour_points(key=tour))


# print(tr.findAll("div", {"class": "league"}))
# tournament = tr.findAll("div", {"class": "league"})
# team = tr.findAll("div", {"class": "overBox"})
# #get_digit(ids[0]["href"])
# soup = BeautifulSoup(txt)
# res = soup.find_all("tr")
# tournament = tr.findAll("div", {"class": "league"})
# team = tr.findAll("div", {"class": "overBox"})
# get_digit(ids[0]["href"])
