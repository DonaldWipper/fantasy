from sport_api import SportsApiMethods
import json


def read_params(fn):
    d = {}
    try:
        with open(fn, 'r', encoding="utf-8") as file:
            d = json.load(file)
    except FileNotFoundError:
        print("Error. Can't find file " + fn)
        d = {}
    return d


try:
    settings = read_params("FlaskApp/settings.json")
    sports = SportsApiMethods(settings)
except:
    settings = read_params("settings.json")
    sports = SportsApiMethods(settings)

print(sports.getStatSeasonsById(56))
