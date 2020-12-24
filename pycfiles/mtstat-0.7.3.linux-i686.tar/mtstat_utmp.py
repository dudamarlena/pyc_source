# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_utmp.py
# Compiled at: 2006-12-12 18:59:18


class mtstat_utmp(mtstat):

    def __init__(self):
        self.name = 'utmp'
        self.format = ('d', 3, 10)
        self.nick = ('ses', 'usr', 'adm')
        self.vars = ('sessions', 'users', 'root')
        self.init(self.vars, 1)

    def check(self):
        global utmp
        try:
            import utmp
            return True
        except:
            raise Exception, 'Module needs the python-utmp module.'

    def extract(self):
        for name in self.vars:
            self.val[name] = 0

        for u in utmp.UtmpRecord():
            if u.ut_type == utmp.USER_PROCESS:
                self.val['users'] = self.val['users'] + 1
                if u.ut_user == 'root':
                    self.val['root'] = self.val['root'] + 1
            self.val['sessions'] = self.val['sessions'] + 1