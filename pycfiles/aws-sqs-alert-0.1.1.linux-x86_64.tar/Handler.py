# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/AWSSQSAlert/handlers/Handler.py
# Compiled at: 2014-02-11 01:00:10
import logging

class Handler(object):
    """
    Handlers process queue messages into actionable alerts.
    """

    def __init__(self):
        """
        Create a new instance of the Handler class
        """
        self.events = []
        self.logger = logging.getLogger('autoscale-alert')

    def watches(self, event):
        """
        Returns true or false for whether than handler operates on that metric
        """
        raise Exception('Not Implemented')

    def alert(self, config, event, msg):
        """
        Processes an event into an alert
        """
        raise Exception('Not Implemented')