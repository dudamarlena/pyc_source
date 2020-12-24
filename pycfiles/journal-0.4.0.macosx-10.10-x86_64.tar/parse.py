# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mbehrens/.pyenv/versions/2.7.8/lib/python2.7/site-packages/journal/parse.py
# Compiled at: 2015-09-01 16:03:46
import time, datetime, re

class Parse(object):

    @staticmethod
    def day(date_string):
        today = datetime.date.today()
        date_string = date_string.strip().lower()
        if date_string == 'today' or date_string == 't':
            return datetime.date(today.year, today.month, today.day)
        else:
            if date_string == 'yesterday' or date_string == 'y':
                return datetime.date(today.year, today.month, today.day) - datetime.timedelta(days=1)
            if re.search('(\\d{1,3}|a) days? ago', date_string):
                return Parse.n_day(date_string)
            return Parse.date(date_string)

    @staticmethod
    def n_day(date_string):
        """
        date_string string in format "(number|a) day(s) ago"
        """
        today = datetime.date.today()
        match = re.match('(\\d{1,3}|a) days? ago', date_string)
        groups = match.groups()
        if groups:
            decrement = groups[0]
            if decrement == 'a':
                decrement = 1
            return today - datetime.timedelta(days=int(decrement))
        else:
            return

    @staticmethod
    def date(date_string):
        date_string = date_string.replace('/', ' ').replace('-', ' ').replace(',', ' ').replace('.', ' ')
        date_formats_with_year = [
         '%m %d %Y', '%Y %m %d', '%B %d %Y', '%b %d %Y',
         '%m %d %y', '%y %m %d', '%B %d %y', '%B %d %y']
        date_formats_without_year = [
         '%m %d', '%d %B', '%B %d',
         '%d %b', '%b %d']
        for format in date_formats_with_year:
            try:
                result = time.strptime(date_string, format)
                return datetime.date(result.tm_year, result.tm_mon, result.tm_mday)
            except ValueError:
                pass

        for format in date_formats_without_year:
            try:
                result = time.strptime(date_string, format)
                year = datetime.date.today().year
                return datetime.date(year, result.tm_mon, result.tm_mday)
            except ValueError:
                pass

        return