# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgalan/projects/redongo/redongo/serializer_utils.py
# Compiled at: 2016-08-11 11:38:11
try:
    import ujson, json
except:
    import json

try:
    import cPickle as pickle
except:
    import pickle

class serializer:

    def __init__(self, serializer_type):
        if serializer_type == 'ujson':
            self.loads = ujson.loads
            self.dumps = ujson.dumps
        elif serializer_type == 'json':
            self.loads = json.loads
            self.dumps = json.dumps
        else:
            self.loads = pickle.loads
            self.dumps = pickle.dumps