#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 18:22:08 2021

@author: yannicklehr
"""
import json
import pandas as pd
from instabot import Bot


data = json.load(open('private/config.json'))

myUsername = data['credentials'][0]['username']
myPassword = data['credentials'][0]['password']

if myUsername is None or myPassword is None:
    raise Exception('Username or Password not set, please check config file')

bot = Bot()
bot.login(username=myUsername,password=myPassword)

try:
    user_id = bot.get_user_id_from_username('Shareyk_')
except Exception as e:
    bot.logger.error("{}".format(e))
    exit()
    
test = bot.api.get_total_followers_or_followings(user_id=user_id,which="followers")
df = pd.DataFrame(test)

from datetime import date

today = date.today()
df.to_pickle('stats/7150177709/'+today.strftime("%d-%m-%Y")+'.pkl')
#df = pd.read_pickle(file_name)

import logging
#test logging
logging.basicConfig(filename='mylog.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running Urban Planning")

logging.info("Halloe")