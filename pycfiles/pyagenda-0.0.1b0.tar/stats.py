# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_conf/stats.py
# Compiled at: 2015-12-21 16:57:02
import logging, os, urllib2, Pyro4, time
from datetime import datetime
from pyage.core.inject import Inject, InjectOptional
from pyage.core.statistics import Statistics
from pyage.core.workplace import WORKPLACE
logger = logging.getLogger(__name__)

class GlobalTimeStatistics(Statistics):

    @Inject('ns_hostname')
    @InjectOptional('notification_url')
    def __init__(self):
        super(GlobalTimeStatistics, self).__init__()
        self.fitness_output = open('fitness_pyage' + str(datetime.now()) + '.txt', 'a')
        self.fitness_output.write('# DIMS:' + os.environ['DIMS'] + os.environ['MACHINES'] + ' ' + str(datetime.now()) + '\n')
        self.start = time.time()

    def update(self, step_count, agents):
        try:
            best_fitness = max(a.get_fitness() for a in agents)
            logger.info(best_fitness)
            if step_count % 100 == 0:
                ns = Pyro4.locateNS(self.ns_hostname)
                best_fitness = max(Pyro4.Proxy(w).get_fitness() for w in ns.list(WORKPLACE).values())
                self.append(best_fitness, step_count)
        except:
            logging.exception('')

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(time.time() - self.start) + ';' + str(abs(best_fitness)) + '\n')

    def summarize(self, agents):
        try:
            if hasattr(self, 'notification_url'):
                url = self.notification_url + '?time=%s&agents=%s&conf=%s' % (
                 time.time() - self.start, os.environ['AGENTS'], os.environ['DIMS'])
                logger.info(url)
                urllib2.urlopen(url)
        except:
            logging.exception('')


class NotificationStats(Statistics):

    @Inject('notification_url')
    def __init__(self):
        super(NotificationStats, self).__init__()
        self.start = time.time()

    def update(self, step_count, agents):
        best_fitness = max(a.get_fitness() for a in agents)
        logger.info(best_fitness)

    def summarize(self, agents):
        try:
            if hasattr(self, 'notification_url'):
                url = self.notification_url + '?time=%s&agents=%s&conf=%s' % (
                 time.time() - self.start, os.environ['AGENTS'], os.environ['DIMS'])
                logger.info(url)
                urllib2.urlopen(url)
        except:
            logging.exception('')


class MigrationNotificationStatistics(Statistics):

    @Inject('notification_url', 'migration')
    def __init__(self):
        super(MigrationNotificationStatistics, self).__init__()
        self.start = time.time()

    def update(self, step_count, agents):
        best_fitness = max(a.get_fitness() for a in agents)
        logger.info(best_fitness)

    def summarize(self, agents):
        try:
            if hasattr(self, 'notification_url'):
                url = self.notification_url + '?time=%s&agents=%s&conf=%s&pr=%s' % (
                 time.time() - self.start, os.environ['AGENTS'], str(self.migration.counter), str(os.environ['PR']))
                logger.info(url)
                urllib2.urlopen(url)
        except:
            logging.exception('')