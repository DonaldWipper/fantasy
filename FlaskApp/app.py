from flask import Flask, render_template, make_response
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import request, flash
import json
import requests
import pandas as pd
import csv
try:
    import FlaskApp.sport_fantasy as sport_fantasy
except:
    import sport_fantasy as sport_fantasy
from datetime import date
from datetime import datetime
from flask import jsonify


app = Flask(__name__)
app.config.from_object(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True



def render(res, lineup={}):
    return render_template("log.html", res2 = res, lineup=lineup)  



@app.route("/update_statistics", methods=['GET'])
def update_statistics():
    tournament_id = request.args.get('tournament_id')
    sport_fantasy.update_plot_statictics()
    res = sport_fantasy.make_transfers()
    return render(res)

@app.route("/make_substitutions", methods=['GET'])
def make_substitutions():
    tournament_id = request.args.get('tournament_id')
    sport_fantasy.make_substitutions(_tournament_id = tournament_id)
    lineup = sport_fantasy.get_myteam_json(_tournament_id = tournament_id)
    res = sport_fantasy.make_transfers()
    return render(res,lineup)


@app.route("/make_transfers", methods=['GET'])
def make_transfers():
    tournament_id = request.args.get('tournament_id')
    res = sport_fantasy.make_transfers(check=False,  _tournament_id = tournament_id)
    return render(res)


@app.route("/show_line_up", methods=['GET'])
def show_line_up():
    tournament_id = request.args.get('tournament_id')
    lineup = sport_fantasy.get_myteam_json(_tournament_id = tournament_id)
    res = sport_fantasy.make_transfers()
    return render(res,lineup)

#sched.start()



 
@app.route("/", methods=['GET'])
def main():
    res = sport_fantasy.make_transfers() 
    print(res)
    return render(res)
        

if __name__ == "__main__":
    app.run(debug = True)
