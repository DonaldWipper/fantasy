from bs4 import BeautifulSoup
import requests
import re
import json


def read_params(fn):
    d = {}
    try:
        with open(fn, "r", encoding="utf-8") as file:
            d = json.load(file)
    except FileNotFoundError:
        print("Error. Can't find file " + fn)
        d = {}
    return d


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_digit(string):
    players_total = string.strip()
    if hasNumbers(players_total):
        number = re.search(r"\d+", players_total.strip()).group()
        players_total = int(number)


settings = read_params("settings.json")
headers = settings["headers"]
txt = requests.get("https://www.sports.ru/fantasy/", headers=headers).text
f = open("fantasy.html", "w")
f.write(txt)
f.close()
soup = BeautifulSoup(txt, features="lxml")
# tr = soup.find_all("tr")
# tournament = tr.findAll("div", {"class": "league"})
# team = tr.findAll("div", {"class": "overBox"})
# #get_digit(ids[0]["href"])
