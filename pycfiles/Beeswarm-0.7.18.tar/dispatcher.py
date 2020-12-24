# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/models/dispatcher.py
# Compiled at: 2016-11-12 07:38:04
import logging, random, datetime, gevent
from gevent import Greenlet
logger = logging.getLogger(__name__)

class BaitDispatcher(Greenlet):
    """ Dispatches capabilities in a realistic fashion (with respect to timings) """

    def __init__(self, bait_type, bait_options):
        Greenlet.__init__(self)
        self.options = bait_options
        self.enabled = False
        self.bait_type = bait_type
        self.run_flag = True
        self.bait_session_running = False
        self.start_time = None
        self.end_time = None
        try:
            self.set_active_interval()
        except (ValueError, AttributeError, KeyError, IndexError) as err:
            logger.debug(('Caught exception: {0} ({1})').format(err, str(type(err))))

        self.activation_probability = self.options['activation_probability']
        self.sleep_interval = float(self.options['sleep_interval'])
        return

    def set_active_interval(self):
        interval_string = self.options['active_range']
        begin, end = interval_string.split('-')
        begin = begin.strip()
        end = end.strip()
        begin_hours, begin_min = begin.split(':')
        end_hours, end_min = end.split(':')
        self.start_time = datetime.time(int(begin_hours), int(begin_min))
        self.end_time = datetime.time(int(end_hours), int(end_min))

    def _run(self):
        while self.run_flag:
            while not self.time_in_range():
                gevent.sleep(5)

            while self.time_in_range():
                if self.activation_probability >= random.random() and not self.bait_session_running:
                    if not self.options['server']:
                        logging.debug('Discarding bait session because the honeypot has not announced the ip address yet')
                    else:
                        self.bait_session_running = True
                        bait = self.bait_type(self.options)
                        greenlet = gevent.spawn(bait.start)
                        greenlet.link(self._on_bait_session_ended)
                else:
                    logging.debug(('Not spawing {0} because a bait session of this type is already running.').format(self.bait_type))
                logging.debug(('Scheduling next {0} bait session in {1} second.').format(self.bait_type, self.sleep_interval))
                gevent.sleep(self.sleep_interval)

    def _on_bait_session_ended(self, greenlet):
        self.bait_session_running = False
        if greenlet.exception is not None:
            logger.warning(('Bait session of type {0} stopped with unhandled error: {1}').format(self.bait_type, greenlet.exception))
        return

    def time_in_range(self):
        """Return true if current time is in the active range"""
        curr = datetime.datetime.now().time()
        if self.start_time <= self.end_time:
            return self.start_time <= curr <= self.end_time
        else:
            return self.start_time <= curr or curr <= self.end_time