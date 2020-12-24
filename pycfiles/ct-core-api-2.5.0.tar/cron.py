# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/web/dez_server/cron.py
# Compiled at: 2020-04-02 07:25:26
from datetime import datetime, timedelta
from rel import timeout
from cantools import config
from cantools.util import read
from ..util import do_respond
secsPerUnit = {'hours': 3600, 
   'minutes': 60, 
   'mins': 60, 
   'seconds': 1}

class Rule(object):

    def __init__(self, controller, url, rule, logger_getter):
        self.logger = logger_getter('Rule(%s -> %s)' % (rule, url))
        self.controller = controller
        self.url = url
        self.rule = rule
        self.exact = len(rule) == 5
        self.words = rule.split(' ')
        self.timer = timeout(None, self.trigger)
        self.parse()
        return

    def trigger(self):
        self.logger.info('trigger: %s (%s)' % (self.url, getattr(self, 'seconds', self.rule)))
        self.controller.trigger_handler(self.url, self.url[1:])
        return True

    def start(self):
        if self.rule != 'on start':
            self.logger.info('start (%s seconds)' % (self.seconds,))
            self.timer.add(self.seconds)
            if self.exact:
                self.timer.delay = 86400

    def parse(self):
        self.logger.info('parse')
        if self.exact:
            hours, mins = self.rule.split(':')
            n = datetime.now()
            t = datetime(n.year, n.month, n.day, int(hours), int(mins))
            self.seconds = (t - n).seconds
        elif self.rule == 'on start':
            self.logger.info('triggering start script')
            self.trigger()
        elif len(self.words) == 3 and self.words[0] == 'every':
            num = int(self.words[1])
            unit = self.words[2]
            self.seconds = num * secsPerUnit[unit]
        else:
            self.logger.error("can't parse: %s" % (self.rule,))


class Cron(object):

    def __init__(self, controller, logger_getter):
        self.logger_getter = logger_getter
        self.logger = logger_getter('Cron')
        self.controller = controller
        self.timers = {}
        self.parse()
        self.start()

    def parse(self):
        self.logger.info('parse')
        url = None
        for line in read('cron.yaml', True):
            if line.startswith('- description: '):
                self.logger.info('initializing %s' % (line[15:],))
            elif line.startswith('  url: '):
                url = line[7:].strip()
            elif url:
                self.timers[url] = Rule(self.controller, url, line[12:].strip(), self.logger_getter)
                url = None

        return

    def start(self):
        self.logger.info('start')
        for rule in list(self.timers.values()):
            rule.start()