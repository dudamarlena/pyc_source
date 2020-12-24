# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/utils/dateutils.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1817 bytes
import datetime, calendar

def calculate_age(birthday):
    today = datetime.date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def numer_of_days(start, end):
    delta = end - start
    return delta.days


def parse_date(date_string):
    if len(date_string) == 10:
        fmt = '%d/%m/%Y'
    else:
        fmt = '%d/%m/%Y %H:%M:%S'
    return datetime.datetime.strptime(date_string, fmt)


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def add_days(sourcedate, days):
    sourcedate = sourcedate or datetime.date.today()
    return sourcedate + datetime.timedelta(days=days)


def future(days):
    return datetime.date.today() + datetime.timedelta(days=days)


def past(days):
    return datetime.date.today() - datetime.timedelta(days=days)


def pretty_date(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    if diff.days > 365 or diff.days < 0:
        return d.strftime('%d %b %y')
    if 60 > diff.days > 30:
        return '1 mês atrás'
    if diff.days > 60:
        return '{} meses atrás'.format(diff.days / 30)
    if diff.days == 1:
        return '1 dia atrás'
    if diff.days > 1:
        return '{} dias atrás'.format(diff.days)
    if s <= 1:
        return 'agora'
    if s < 60:
        return '{} segundos atrás'.format(s)
    if s < 120:
        return '1 minuto atrás'
    if s < 3600:
        return '{} minutos atrás'.format(s / 60)
    else:
        if s < 7200:
            return '1 hora atrás'
        return '{} horas atrás'.format(s / 3600)