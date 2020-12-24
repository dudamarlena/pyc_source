# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyano/security.py
# Compiled at: 2010-11-08 17:36:16
import datetime
from config import conf
datetime_fmt = '%H%M%S%m%d%Y'

class SecurityError(Exception):
    pass


def get_history():
    history = {}
    try:
        with open(conf.hist_file, 'r') as (f):
            for line in f:
                times = line.strip('\n').split(':')
                ip = times.pop(0)
                history[ip] = [ datetime.datetime.strptime(t, datetime_fmt) for t in times ]

    except IOError:
        pass

    return history


def prune_history(hist):
    now = datetime.datetime.today()
    cutoff = now - datetime.timedelta(0, 0, 0, 0, conf.hist_window)
    to_del = []
    for (ip, times) in hist.iteritems():
        new_times = []
        for t in times:
            if t >= cutoff:
                new_times.append(t)

        if new_times:
            hist[ip] = new_times
        else:
            to_del.append(ip)

    for ip in to_del:
        del hist[ip]

    return hist


def write_history(hist):
    try:
        with open(conf.hist_file, 'w') as (f):
            for (ip, times) in hist.iteritems():
                f.write(ip)
                for t in times:
                    f.write(':' + t.strftime(datetime_fmt))

                f.write('\n')

    except IOError:
        pass


def check_hist(ip):
    hist = prune_history(get_history())
    if ip in hist:
        hist[ip].append(datetime.datetime.today())
        write_history(hist)
        if len(hist[ip]) > 2 * conf.hist_max_uses:
            ban(ip)
            raise SecurityError("Your ip has been banned from using this service. If you feel this is not warranted, please contact this service's operator")
        if len(hist[ip]) > conf.hist_max_uses:
            raise SecurityError('In order to prevent abuse of this service, you can only send a limited number of emails at a given time. Please try again later. If you persist in trying to use this interface too frequently, you will eventually get banned from this service.')
    else:
        hist[ip] = [
         datetime.datetime.today()]
        write_history(hist)


def check_banned(ip):
    banned = get_banned()
    if ip in banned:
        raise SecurityError("Your ip has been banned from using this service. If you feel this is not warranted, please contact this service's operator")


def ban(ip):
    banned = get_banned()
    banned.append(ip)
    write_banned(banned)


def get_banned():
    banned = []
    try:
        with open(conf.banned_file, 'r') as (f):
            banned = f.read().split('\n')
    except IOError:
        pass

    return banned


def write_banned(banned):
    with open(conf.banned_file, 'w') as (f):
        f.write(('\n').join(banned))


def check_ip(ip):
    check_banned(ip)
    check_hist(ip)