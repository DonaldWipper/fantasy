
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, render_template, make_response
from flask import request, flash
import os
import logging
import sys

try:
    import FlaskApp.sport_fantasy as sport_fantasy
except:
    import sport_fantasy as sport_fantasy



logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
logging.captureWarnings(True)


files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    logging.info(f)
# do something


application = Flask(__name__)
application.config.from_object(__name__)
application.config["TEMPLATES_AUTO_RELOAD"] = True


def render(res, lineup={}):
    return render_template("log.html", res2=res, lineup=lineup)


@application.route("/update_statistics", methods=["GET"])
def update_statistics():
    tournament_id = request.args.get("tournament_id")
    sport_fantasy.update_plot_statictics()
    res = sport_fantasy.make_transfers()
    return render(res)


@application.route("/make_substitutions", methods=["GET"])
def make_substitutions():
    tournament_id = request.args.get("tournament_id")
    sport_fantasy.make_substitutions(_tournament_id=tournament_id)
    lineup = sport_fantasy.get_myteam_json(_tournament_id=tournament_id)
    res = sport_fantasy.make_transfers()
    return render(res, lineup)


@application.route("/make_transfers", methods=["GET"])
def make_transfers():
    tournament_id = request.args.get("tournament_id")
    res = sport_fantasy.make_transfers(check=False, _tournament_id=tournament_id)
    return render(res)


@application.route("/show_line_up", methods=["GET"])
def show_line_up():
    tournament_id = request.args.get("tournament_id")
    lineup = sport_fantasy.get_myteam_json(_tournament_id=tournament_id)
    res = sport_fantasy.make_transfers()
    return render(res, lineup)


# sched.start()


@application.route("/", methods=["GET"])
def main():
    res = sport_fantasy.make_transfers()
    print(res)
    return render(res)


if __name__ == "__main__":
    application.run(debug=True)
