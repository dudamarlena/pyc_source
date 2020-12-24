# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grbackup/grb_plugins/simple_output.py
# Compiled at: 2013-06-08 03:08:50
from collections import defaultdict
plugin_type = 'simple'
support_threads = False

def add_option_group(parser):
    return


class SimplePrint(object):

    def __init__(self, coding):
        self.coding = coding
        self._count_subs = 0
        self._count_topics = defaultdict(int)
        self._subscription = None
        self._starred = False
        return

    def put_subscription(self, subscription):
        if self._subscription != subscription:
            self._subscription = subscription
            title = subscription.get('title', '').encode(self.coding)
            url = subscription['id'].encode(self.coding)[5:]
            print ('feed: {0} ({1})').format(title, url)

    def put_all(self, subscription, topic):
        self.put_subscription(subscription)
        url = subscription['id'].encode(self.coding)[5:]
        self.put_topic(url, topic)

    def put_starred(self, topic):
        if not self._starred:
            self._starred = True
            print 'Starred:'
        title = topic.get('title', '').encode(self.coding)
        print title

    def put_topic(self, subscription_url, topic):
        url = ''
        if topic.get('alternate'):
            url = topic['alternate'][0]['href'].encode(self.coding)
        title = topic.get('title', '').encode(self.coding)
        message = ('{0} ({1})').format(title, url)
        print message


class writer(object):

    def __init__(self, opt):
        self._coding = opt.coding

    def __enter__(self):
        return SimplePrint(self._coding)

    def __exit__(self, *exc_info):
        pass