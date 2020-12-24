# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratyush/Projects/HackerFeed/venv/lib/python3.6/site-packages/hfeedlib/fetchlib.py
# Compiled at: 2017-06-28 14:19:44
# Size of source mod 2**32: 1956 bytes
import json, requests
from .utils import fetchItem, getArticlesPath
from .parsing.save import savedparser
BASE_URL = 'https://hacker-news.firebaseio.com/v0/'

def getNewArticles(number: int=5, save_flag: bool=False, single: bool=False, start_point: int=0):
    r = requests.get(BASE_URL + 'newstories.json')
    r = json.loads(r.content)
    articles = []
    if single:
        return fetchItem((r[(number - 1)]), save_flag=save_flag)
    else:
        id_list = r[start_point:start_point + number]
        id_list.reverse()
        for id in id_list:
            articles.append(fetchItem(id, save_flag=save_flag))

        articles.reverse()
        return articles


def getTopArticles(number: int=5, save_flag: bool=False, single: bool=False, start_point: int=0):
    r = requests.get(BASE_URL + 'topstories.json')
    r = json.loads(r.content)
    articles = []
    if single:
        return fetchItem((r[(number - 1)]), save_flag=save_flag)
    else:
        id_list = r[start_point:start_point + number]
        id_list.reverse()
        for id in id_list:
            articles.append(fetchItem(id, save_flag=save_flag))

        articles.reverse()
        return articles


def getBestArticles(number: int=5, save_flag: bool=False, single: bool=False, start_point: int=0):
    r = requests.get(BASE_URL + 'beststories.json')
    r = json.loads(r.content)
    articles = []
    if single:
        return fetchItem((r[(number - 1)]), save_flag=save_flag)
    else:
        id_list = r[start_point:start_point + number]
        id_list.reverse()
        for id in id_list:
            articles.append(fetchItem(id, save_flag=save_flag))

        articles.reverse()
        return articles


def getSavedArticles(number: int=5, display_all: bool=False):
    parser = savedparser(getArticlesPath())
    if display_all:
        return parser.parse()
    else:
        return parser.parse()[:number]