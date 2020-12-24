# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/lib.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 2019 bytes
import time, datetime
hostname = None

def gethostname():
    global hostname
    if hostname is None:
        import platform
        hostname = platform.node()
        if '.' in hostname:
            hostname = hostname.split('.')[0]
    return hostname


def decode_time_float(istr):
    if istr is None:
        return
    else:
        try:
            tyme = float(istr)
        except ValueError:
            if '.' in istr:
                l = istr.split('.', 1)
            else:
                l = [
                 istr]
            try:
                d = time.strptime(l[0], '%Y-%m-%d %H:%M:%S')
                tyme = time.mktime(d)
            except ValueError:
                try:
                    d = time.strptime(l[0], '%Y-%m-%dT%H:%M:%S')
                    tyme = time.mktime(d)
                except ValueError:
                    return

            if len(l) > 1:
                a = l[1]
                frac = float(int(a)) / int('1' + '0' * len(a))
                tyme = tyme + frac

        return tyme


def decode_time_str(istr):
    if istr is None:
        return
    else:
        try:
            tyme = float(istr)
        except ValueError:
            return istr

        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tyme)) + '.' + '%03d' % (int(tyme - int(tyme)) * 1000)


def time_diff(max, min):
    max = decode_time_float(max)
    min = decode_time_float(min)
    if max is None:
        return
    else:
        if min is None:
            return
        return datetime.timedelta(seconds=(int(max - min)))