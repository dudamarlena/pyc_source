# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/client.py
# Compiled at: 2016-11-12 07:38:04
import logging, urllib2, gevent, gevent.monkey
gevent.monkey.patch_all()
from beeswarm.drones.client.baits import clientbase
from beeswarm.drones.client.models.session import BaitSession
from beeswarm.drones.client.models.dispatcher import BaitDispatcher
from beeswarm.shared.helpers import extract_keys, get_most_likely_ip
logger = logging.getLogger(__name__)

class Client(object):

    def __init__(self, work_dir, config):
        """
            Main class which runs Beeswarm in Client mode.

        :param work_dir: Working directory (usually the current working directory)
        :param config_arg: Beeswarm configuration dictionary.
        """
        self.run_flag = True
        self.config = config
        extract_keys(work_dir, config)
        BaitSession.client_id = self.config['general']['id']
        if self.config['general']['fetch_ip']:
            self.my_ip = urllib2.urlopen('http://api-sth01.exip.org/?call=ip').read()
            logger.info(('Fetched {0} as my external ip.').format(self.my_ip))
        else:
            self.my_ip = get_most_likely_ip()
        self.dispatcher_greenlets = []

    def start(self):
        """
            Starts sending client bait to the configured Honeypot.
        """
        logger.info('Starting client.')
        self.dispatcher_greenlets = []
        for _, entry in self.config['baits'].items():
            for b in clientbase.ClientBase.__subclasses__():
                bait_name = b.__name__.lower()
                if bait_name in entry:
                    bait_options = entry[bait_name]
                    dispatcher = BaitDispatcher(b, bait_options)
                    dispatcher.start()
                    self.dispatcher_greenlets.append(dispatcher)
                    logger.info(('Adding {0} bait').format(bait_name))
                    logger.debug(('Bait added with options: {0}').format(bait_options))

        gevent.joinall(self.dispatcher_greenlets)

    def stop(self):
        """
            Stop sending bait sessions.
        """
        for g in self.dispatcher_greenlets:
            g.kill()

        logger.info('All clients stopped')