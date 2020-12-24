# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jobspider\baseclass\utils\store_data.py
# Compiled at: 2016-04-19 03:35:42
"""
store_data.py

the data needed sotred is in format:[{},{},{}],we can store them in Mysql ,json or Redis

"""
import json, os
from datetime import datetime, date
from ..database import Database

class Job_Data:

    def __init__(self, store_type='json'):
        self.store_type = store_type
        self.today = date.today().strftime('%Y-%m-%d')

    def store(self, data):
        if self.store_type == 'MySQL':
            self.store_to_mysql(data)
        elif self.store_type == 'json':
            self.store_to_json(data)
        elif self.store_type == 'excel':
            self.store_to_excel(data)
        elif self.store_type == 'redis':
            self.store_to_redis(data)

    def store_to_mysql(self, data):
        self.db = Database('Job')
        for item in data:
            item['create_day'] = self.today

        self.db.insert_dic_by_list('jobs', data)

    def store_to_json(self, data, filename=('-').join([date.today().strftime('%Y-%m-%d'), 'job.json'])):
        basepath = ('/').join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
        if os.name == 'nt':
            filepath = os.path.join(basepath, '%s' % filename)
            print 'json file is stored in %s' % filepath
        else:
            filepath = os.path.join('/tmp', filename)
            print 'json file is stored in %s ' % filepath
        for item in data:
            json_data = json.dumps(item)
            with file(filepath, 'a+') as (json_file):
                json_file.write(json_data)
                json_file.write('\n')

    def store_to_excel(self, data, filename='job.xlsx'):
        pass

    def store_to_redis(self, data, keyname='job'):
        pass