# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskillscore/time_interval.py
# Compiled at: 2017-08-03 08:36:25
""" A representation of a time interval. """

class TimeInterval:
    """ A representation of a time interval. """

    def __init__(self, start, end):
        """ Initialisation.

        :param start: the start of the time interval.
        :param end: the end of the time interval.
        """
        self.start = start
        self.end = end