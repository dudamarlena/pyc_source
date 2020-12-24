# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleconf/time2epoch2time.py
# Compiled at: 2020-01-24 07:29:17
# Size of source mod 2**32: 1843 bytes
import time, datetime

class epochtime:

    def date2epoch(date):
        hiredate = date
        pattern = '%d-%m-%Y'
        try:
            epoch = int(time.mktime(time.strptime(hiredate, pattern)))
            return epoch
        except ValueError:
            print('date format is not DD-MM-YYYY.moving to next item')
        except OverflowError:
            print('date format is before 1900.moving to next item')

    def epoch2date(epoch):
        try:
            ndate = datetime.date.fromtimestamp(epoch).strftime('%d-%m-%Y')
        except ValueError:
            print('epoch is wrong. moving to next item')
        except TypeError:
            print('encountered Type error as epoch returned was NULL')

        return ndate

    def epoch2dateeod(epoch):
        try:
            ndate = datetime.date.fromtimestamp(epoch).strftime('%Y-%m-%d')
        except ValueError:
            print('epoch is wrong. moving to next item')
            ndate = None
        except TypeError:
            print('encountered Type error as epoch returned was NULL')
            ndate = None

        return ndate

    def date2epocheod(date):
        hiredate = date
        pattern = '%Y-%m-%d'
        try:
            epoch = int(time.mktime(time.strptime(hiredate, pattern)))
            return epoch
        except ValueError:
            print('date format is not YYYY-MM-DD.moving to next item')
            ndate = None
        except OverflowError:
            print('date format is before 1900.moving to next item')
            ndate = None