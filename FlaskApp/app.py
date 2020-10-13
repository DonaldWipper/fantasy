import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from environs import Env

from flask import Flask, render_template, make_response
from flask import request, flash
import os
import logging
import sys

from cubes.server.utils import str_to_bool
from cubes.server.blueprint import slicer
import io
import configparser
import os.path

try:
    import FlaskApp.sport_fantasy as sport_fantasy
except:
    import sport_fantasy as sport_fantasy


# счатаем параметр
def read_config_local(config_path, path=""):
    env = Env()
    env.read_env()
    fin = open(config_path, "r")
    x = fin.read().format(
        DB_CONN_STR=env.str("DB_CONN_STR"),
        MODEL_PATH=path + "/" + env.str("MODEL_PATH"),
    )
    fin.close()
    buf = io.StringIO(x)
    config = configparser.ConfigParser()
    config.read_file(buf)
    return config


def create_server_(config=None, **_options):
    # Load extensions
    print(config)
    app = Flask(__name__)
    app.register_blueprint(slicer, config=config, url_prefix="/api", **_options)
    return app


# Set the configuration file
try:
    CONFIG_PATH = os.environ["SLICER_CONFIG"]
except KeyError:
    try:
        CONFIG_PATH = os.path.join(os.getcwd(), "slicer.ini")
        path = os.getcwd()
        config = read_config_local(CONFIG_PATH, path)

    except:
        CONFIG_PATH = os.path.join(os.getcwd() + "/FlaskApp/", "slicer.ini")
        path = os.getcwd() + "/FlaskApp/"
        config = read_config_local(CONFIG_PATH, path)

application = Flask(__name__)
application.config.from_object(__name__)
application.config["TEMPLATES_AUTO_RELOAD"] = True
application = create_server_(config)
debug = os.environ.get("SLICER_DEBUG")


def render(res, lineup={}):
    return render_template("log.html", res2=res, lineup=lineup)


#
# @application.route("/update_statistics", methods=["GET"])
# def update_statistics():
#     tournament_id = request.args.get("tournament_id")
#     sport_fantasy.update_plot_statictics()
#     res = sport_fantasy.make_transfers()
#     return render(res)


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
