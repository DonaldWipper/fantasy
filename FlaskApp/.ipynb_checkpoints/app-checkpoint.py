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



def render(res):
    return render_template("log.html", res2 = res)  


@app.route("/make_subs", methods=['GET'])
def make_subs():
    tournament_id = request.args.get('tournament_id')
    res = sport_fantasy.make_subs(tournament_id)
    return render(res)

#sched.start()



 
@app.route("/", methods=['GET'])
def main():
    res = sport_fantasy.make_subs() 
    print(res)
    return render(res)
        

if __name__ == "__main__":
    app.run(debug = True)
