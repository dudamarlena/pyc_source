# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/log.py
# Compiled at: 2020-01-12 12:29:08
# Size of source mod 2**32: 2212 bytes


class Log(object):

    @property
    def log_clear_all(self):
        ret = self.command('log.cgi?action=clear')
        return ret.content.decode('utf-8')

    def log_show(self, start_time, end_time):
        ret = self.command('Log.backup?action=All&condition.StartTime={0}&condition.EndTime={1}'.format(start_time, end_time))
        return ret.content.decode('utf-8')

    def log_find_start(self, start_time, end_time):
        ret = self.command('log.cgi?action=startFind&condition.StartTime={0}&condition.EndTime={1}'.format(start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
        return ret.content.decode('utf-8')

    def log_find_next(self, token, count=100):
        ret = self.command('log.cgi?action=doFind&token={0}&count={1}'.format(token, count))
        return ret.content.decode('utf-8')

    def log_find_stop(self, token):
        ret = self.command('log.cgi?action=stopFind&token={0}'.format(token))
        return ret.content.decode('utf-8')

    def log_find(self, start_time, end_time):
        token = self.log_find_start(start_time, end_time).strip().split('=')[1]
        to_query = True
        while to_query:
            content = self.log_find_next(token)
            tag, count = (list(content.split('\r\n', 1)[0].split('=')) + [None])[:2]
            to_query = False
            if tag == 'found':
                if int(count) > 0:
                    to_query = True
            yield content

        self.log_find_stop(token)