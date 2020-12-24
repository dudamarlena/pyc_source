# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/log.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 926 bytes


class Log(object):

    @property
    def log_clear_all(self):
        ret = self.command('log.cgi?action=clear')
        return ret.content.decode('utf-8')

    def log_show(self, start_time, end_time):
        ret = self.command('Log.backup?action=All&condition.StartTime={0}&condition.EndTime={1}'.format(start_time, end_time))
        return ret.content.decode('utf-8')