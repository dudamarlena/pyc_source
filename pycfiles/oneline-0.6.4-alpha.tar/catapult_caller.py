# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/oneline/modules/catapult_caller.py
# Compiled at: 2015-02-28 18:25:51
from oneline import ol
from bandwidth_sdk import Client
from bandwidth_sdk import Call
import bsonlib

class catapult_caller(ol.module):

    def start(self):
        print 'Starting the Catapult Module.'
        self.pipeline = ol.stream()
        self.config = ol.config()
        self.bandwidth_client = Client(self.config['bandwidth_user_id'], self.config['bandwidth_app_id'], self.config['bandwidth_app_secret'])

    def receiver(self, message):
        parsed_message = ol.parse_message(message)
        packet = parsed_message['packet']
        if packet['generic']['type'] == 'call':
            print 'Calling someone!'
            try:
                call = Call.create(self.config['bandwidth_number'], packet['generic']['data']['to'])
            except:
                pass

        if packet['generic']['type'] == 'list':
            calls = Call.list()
            calls_d = []
            for i in calls:
                call = {'from': getattr(i, 'from_'), 'to': i.to, 'state': i.state}
                calls_d.append(call)

            parsed_message['data'] = calls_d
        packed = ol.pack_message(parsed_message)
        self.pipeline.run(packed)

    def provider(self, message):
        parsed_message = ol.parse_message(message)
        self.pipeline.run(message)

    def end(self):
        print 'Closing Catapult module. See you soon!'