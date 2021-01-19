#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 18:22:08 2021

@author: yannicklehr
"""

import pandas as pd
import glob
from textblob import TextBlob
from instabot import Bot


bot = Bot()
bot.login(username="",password="")

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