# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benwaters/sensu-auditor/lib/python2.7/site-packages/sensu_auditor/unhealthy.py
# Compiled at: 2016-09-05 06:45:07


class UnhealthyList(list):
    """
    """

    def get_by_name(self, name):
        """

        :param name:
        :return:
        """
        try:
            return [ index for index, x in enumerate(self) if x.check_name == name ][0]
        except ValueError:
            return

        return

    def names(self):
        """

        :return:
        """
        return [ x.check_name for x in self ]


class UnhealthyEntry(object):
    """

    """

    def __init__(self, check_name, start_time=None, end_time=None):
        self.check_name = check_name
        self.start_time = start_time
        self.end_time = end_time