# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grbackup/grb_plugins/json_output.py
# Compiled at: 2013-06-08 03:08:50
import json, os, threading
plugin_type = 'json'
support_threads = True
description = 'save items into file\noutput scheme:   json:/path/to/file.json\noutput examples: json:/home/grbackup/grbackup.json\n                 json:/tmp/grbackup/grbackup.json\n'

def add_option_group(parser):
    return


class WriteJSON(object):

    def __init__(self, fd):
        self.fd = fd
        self.subscriptions = set()
        self.lock = threading.Lock()

    def put_subscription(self, subscription):
        if subscription['id'] not in self.subscriptions:
            self.subscriptions.add(subscription['id'])
            self.write({'type': 'subscription', 'value': subscription})

    def put_all(self, subscription, topic):
        self.put_subscription(subscription)
        subscription_url = subscription['id'][5:]
        self.put_topic(subscription_url, topic)

    def put_starred(self, topic):
        self.write({'type': 'starred', 'value': topic})

    def put_topic(self, subscription_url, topic):
        self.write({'type': 'topic', 'subscription': subscription_url, 
           'value': topic})

    def write(self, json_obj):
        with self.lock:
            if self.fd.tell() == 0:
                self.fd.write('[')
            else:
                self.fd.seek(-1, os.SEEK_END)
                self.fd.truncate()
                self.fd.write(',\n')
            self.fd.write(json.dumps(json_obj))
            self.fd.write(']')


class writer(object):

    def __init__(self, opt):
        self._output = opt.output[opt.output.index(':') + 1:]
        self._fd = open(self._output, 'w')

    def __enter__(self):
        return WriteJSON(self._fd)

    def __exit__(self, *exc_info):
        if self._fd:
            self._fd.close()