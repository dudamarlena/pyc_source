# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/cf/user_rating.py
# Compiled at: 2019-07-09 05:11:54
# Size of source mod 2**32: 633 bytes
from cf.classes import *
from colorama import Fore, Back, Style
from cf.util import *
from datetime import datetime

def user_rating(user):
    user = user['result']
    n = len(user)
    ratings = []
    for i in range(n):
        ratings.append(RatingChange(user[i]))

    x = []
    y = []
    for i in range(n):
        a = ratings[i].ratingUpdateTimeSeconds
        a = datetime.fromtimestamp(a).strftime('%d%m%Y')
        x.append(a)
        y.append(ratings[i].newRating)

    print('\n\tRating Chart for user : ' + Fore.BLACK + Back.YELLOW + '{:10s}'.format(' ' + ratings[0].handle + ' ') + Style.RESET_ALL)
    plotterm(x, y)