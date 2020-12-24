# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_wifi.py
# Compiled at: 2006-12-12 18:59:18
import iwlibs

class mtstat_wifi(mtstat):

    def __init__(self):
        global iwlibs
        self.name = 'wifi'
        self.format = ('d', 3, 33)
        self.vars = iwlibs.getNICnames()
        self.name = self.vars
        self.nick = ('lnk', 's/n')
        self.init(self.vars, 2)

    def check(self):
        global iwlibs
        try:
            import iwlibs
        except:
            raise Exception, 'Module needs the python-wifi module.'

        return True

    def extract(self):
        for name in self.vars:
            wifi = iwlibs.Wireless(name)
            (stat, qual, discard, missed_beacon) = wifi.getStatistics()
            if qual.quality == 0 and qual.signallevel == qual.noiselevel == -101:
                self.val[name] = (-1, -1)
            else:
                self.val[name][0] = qual.quality * 100 / 160
                self.val[name][1] = qual.signallevel * 100 / qual.noiselevel