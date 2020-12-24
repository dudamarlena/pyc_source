# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/NEMbox/storage.py
# Compiled at: 2020-03-16 06:22:23
# Size of source mod 2**32: 3118 bytes
"""
Class to stores everything into a json file.
"""
from __future__ import print_function, unicode_literals, division, absolute_import
import json
from future.builtins import open
from .const import Constant
from .singleton import Singleton
from .utils import utf8_data_to_file

class Storage(Singleton):

    def __init__(self):
        """
        Database stores every info.

        version int
        # if value in file is unequal to value defined in this class.
        # An database update will be applied.
        user dict:
            username str
            key str
        collections list:
            collection_info(dict):
                collection_name str
                collection_type str
                collection_describe str
                collection_songs list:
                    song_id(int)
        songs dict:
            song_id(int) dict:
                song_id int
                artist str
                song_name str
                mp3_url str
                album_name str
                album_id str
                quality str
                lyric str
                tlyric str
        player_info dict:
            player_list list[dict]
            playing_order list[int]
            playing_mode int
            playing_offset int

        :return:
        """
        if hasattr(self, '_init'):
            return
        self._init = True
        self.database = {'user':{'username':'', 
          'password':'', 
          'user_id':'', 
          'nickname':''}, 
         'collections':[],  'songs':{},  'player_info':{'player_list':[],  'player_list_type':'', 
          'player_list_title':'', 
          'playing_order':[],  'playing_mode':0, 
          'idx':0, 
          'ridx':0, 
          'playing_volume':60}}
        self.storage_path = Constant.storage_path
        self.cookie_path = Constant.cookie_path

    def login(self, username, password, userid, nickname):
        self.database['user'] = dict(username=username,
          password=password,
          user_id=userid,
          nickname=nickname)

    def logout(self):
        self.database['user'] = {'username':'', 
         'password':'', 
         'user_id':'', 
         'nickname':''}

    def load(self):
        try:
            with open(self.storage_path, 'r') as (f):
                for k, v in json.load(f).items():
                    if isinstance(self.database[k], dict):
                        self.database[k].update(v)
                    else:
                        self.database[k] = v

        except (OSError, KeyError, ValueError) as e:
            try:
                pass
            finally:
                e = None
                del e

        self.save()

    def save(self):
        with open(self.storage_path, 'w') as (f):
            data = json.dumps(self.database)
            utf8_data_to_file(f, data)