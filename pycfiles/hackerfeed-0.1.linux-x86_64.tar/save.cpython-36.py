# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratyush/Projects/HackerFeed/venv/lib/python3.6/site-packages/hfeedlib/parsing/save.py
# Compiled at: 2017-06-28 14:00:57
# Size of source mod 2**32: 993 bytes
import os, json

class savedparser:

    def __init__(self, saved_path: str):
        if not os.path.isfile(saved_path):
            raise FileNotFoundError
        self.saved_path = saved_path

    def parse(self):
        with open(self.saved_path, 'r') as (save_file):
            articles = json.load(save_file)
        return articles

    def insert(self, article: dict):
        with open(self.saved_path) as (save_file):
            articles = json.load(save_file)
        ids_old = [a['id'] for a in articles]
        if article['id'] not in ids_old:
            articles = [
             article] + articles
        with open(self.saved_path, 'w') as (save_file):
            json.dump(articles, save_file)

    def remove(self, num: int=1):
        with open(self.saved_path) as (save_file):
            articles = json.load(save_file)
        articles = articles[:num - 1] + articles[num:]
        with open(self.saved_path, 'w') as (save_file):
            json.dump(articles, save_file)