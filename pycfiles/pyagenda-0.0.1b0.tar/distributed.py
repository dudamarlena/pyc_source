# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/stats/distributed.py
# Compiled at: 2015-12-21 17:12:57
import logging, os, urllib2, Pyro4, time, sys
from pyage.core.inject import Inject, InjectOptional
from pyage.core.statistics import Statistics
from pyage.core.workplace import WORKPLACE
logger = logging.getLogger(__name__)

class GlobalStepStatistics(Statistics):

    @Inject('ns_hostname')
    @InjectOptional('notification_url')
    def __init__(self, output_file_name='fitness_pyage.txt'):
        super(GlobalStepStatistics, self).__init__()
        self.fitness_output = open(output_file_name, 'a')
        self.start = time.time()

    def update(self, step_count, agents):
        if step_count % 100 == 0:
            ns = Pyro4.locateNS(self.ns_hostname)
            best_fitness = max(Pyro4.Proxy(w).get_fitness() for w in ns.list(WORKPLACE).values())
            self.append(best_fitness, step_count)

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(step_count) + ';' + str(abs(best_fitness)) + '\n')

    def summarize(self, agents):
        try:
            if hasattr(self, 'notification_url'):
                url = self.notification_url + '?time=%s&agents=%s&conf=%s' % (
                 time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
                logger.info(url)
                urllib2.urlopen(url)
        except:
            logging.exception('')