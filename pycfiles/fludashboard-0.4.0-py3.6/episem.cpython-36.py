# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /storage/Marcelo/codes/FluVigilanciaBR/fludashboard/fludashboard/libs/episem.py
# Compiled at: 2017-10-17 15:31:35
# Size of source mod 2**32: 2743 bytes
import numpy as np, datetime
__author__ = 'Marcelo Ferreira da Costa Gomes'

def extractweekday(x=datetime.datetime):
    w = x.isoweekday() % 7
    return w


def firstepiday(year=int):
    day = datetime.datetime.strptime('%s-01-01' % year, '%Y-%m-%d')
    day_week = extractweekday(day)
    if day_week < 4:
        day = day - datetime.timedelta(days=day_week)
    else:
        day = day + datetime.timedelta(days=(7 - day_week))
    return day


def lastepiday(year=int):
    day = datetime.datetime.strptime('%s-12-31' % year, '%Y-%m-%d')
    day_week = extractweekday(day)
    if day_week < 3:
        day = day - datetime.timedelta(days=(day_week + 1))
    else:
        day = day + datetime.timedelta(days=(6 - day_week))
    return day


def episem(x, sep='W', out='YW'):
    """
    Return Brazilian corresponding epidemiological week from x.

    :param x: Input date. Can be a string in the format %Y-%m-%d or datetime.datetime
    :param sep: Year and week separator.
    :param out: Output format. 'YW' returns sep.join(epiyear,epiweek).
     'Y' returns epiyear only. 'W' returns epiweek only.
    :return: str
    """

    def out_format(year, week, out):
        if out == 'YW':
            return '%sW%02d' % (year, week)
        else:
            if out == 'Y':
                return '%s' % year
            if out == 'W':
                return '%02d' % week

    if type(x) != datetime.datetime:
        if str(x) == '' or type(x) != str and np.isnan(x):
            return
        x = datetime.datetime.strptime(x, '%Y-%m-%d')
    epiyear = x.year
    epiend = lastepiday(epiyear)
    if x > epiend:
        epiyear += 1
        return out_format(epiyear, 1, out)
    else:
        epistart = firstepiday(epiyear)
        if x < epistart:
            epiyear -= 1
            epistart = firstepiday(epiyear)
        epiweek = int(((x - epistart) / 7).days) + 1
        return out_format(epiyear, epiweek, out)