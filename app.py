#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 19:31:59 2021

@author: yannicklehr
"""

import logging
#test logging
logging.basicConfig(filename='server.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("##---------## SERVER STARTED ##---------##")

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, send_file, redirect, url_for, request, render_template, Response
from datetime import date, datetime
import atexit

from os import listdir
from os.path import isfile, join

import json
import pandas as pd
from instabot import Bot

data = json.load(open('private/config.json'))

def checkIfVariableExists(var):
    try:
        var
    except NameError:
        return False
    else:
        return True

def login():
    myUsername = data['credentials'][0]['username']
    myPassword = data['credentials'][0]['password']

    if myUsername is None or myPassword is None:
        raise Exception('Username or Password not set, please check config file')
    
    bot.login(username=myUsername,password=myPassword)
    logging.info("## "+myUsername+" logged in")




lastRun = 'Not runned yet'

def getStats(overwrite=False):
    if not bot.api.is_logged_in:
        logging.info("------> TASK skipped")
        return False
    
    logging.info("## Background task started")
    print("Scheduler is alive!")
    today = date.today()
    lastRun = datetime.today()
    try:
        user_id = bot.get_user_id_from_username('Shareyk_')
    except Exception as e:
        bot.logger.error("{}".format(e))
        exit()
    
    if not isfile('stats/'+str(user_id)+'/'+today.strftime("%d-%m-%Y")+'.pkl') or overwrite:
        followerData = bot.api.get_total_followers_or_followings(user_id=user_id,which="followers")
        df = pd.DataFrame(followerData)
        logging.info("------> SAVED")
        df.to_pickle('stats/'+str(user_id)+'/'+today.strftime("%d-%m-%Y")+'.pkl')
    else:
        logging.info("------> File already there")


bot = Bot()
if not bot.api.is_logged_in:
    login()

runHour = int(data['runTime']['hour'])
runMin = int(data['runTime']['min'])

scheduler = BackgroundScheduler()
#scheduler.add_job(func=sensor, trigger="interval", seconds=5)
scheduler.add_job(getStats, 'cron', hour=runHour, minute=runMin)
scheduler.start()
logging.info("## BackgroundScheduler started")

atexit.register(lambda: scheduler.shutdown(wait=False))


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template("index.html",lastRun=str(lastRun))

@user.route('/manuelExecute')
@app.route('/manuelExecute/<overwrite>')
def manuelExecute(overwrite):
    if overwrite == 'overwrite':
        getStats(True)
    else:
        getStats()
    return render_template("index.html",lastRun=str(lastRun))

@app.route("/test")
def test():
    """ Function for test purposes. """
    return "Server is running! YEY. Last task run at: "+str(lastRun)+" Check the Logfile for more!"

if __name__ == "__main__":
    app.run()
  
    
  
###ALTERNATIVE!!!
"""
import atexit

# v2.x version - see https://stackoverflow.com/a/38501429/135978
# for the 3.x version
from apscheduler.scheduler import Scheduler
from flask import Flask

app = Flask(__name__)

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

@cron.interval_schedule(hours=1)
def job_function():
    # Do your work here


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == '__main__':
    app.run()
"""