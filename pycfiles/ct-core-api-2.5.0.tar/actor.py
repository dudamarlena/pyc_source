# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/pubsub/actor.py
# Compiled at: 2016-02-10 05:18:56


class Actor(object):

    def data(self):
        return {'name': self.name, 
           'channels': [ c.name for c in self.channels ]}

    def join(self, channel):
        self.channels.add(channel)

    def leave(self, channel):
        if channel in self.channels:
            self.channels.remove(channel)