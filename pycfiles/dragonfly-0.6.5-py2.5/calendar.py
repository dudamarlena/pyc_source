# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\language\en\calendar.py
# Compiled at: 2009-03-26 12:39:16
"""
This file implements date and time elements for the English language.

"""
from datetime import date, time, timedelta
from ...grammar.elements import Alternative, Compound, Choice
from ...grammar.number import Integer, IntegerRef
month_names = {'January': 1, 
   'February': 2, 
   'March': 3, 
   'April': 4, 
   'May': 5, 
   'June': 6, 
   'July': 7, 
   'August': 8, 
   'September': 9, 
   'October': 10, 
   'November': 11, 
   'December': 12}
day_names = {'Monday': 0, 
   'Tuesday': 1, 
   'Wednesday': 2, 
   'Thursday': 3, 
   'Friday': 4, 
   'Saturday': 5, 
   'Sunday': 6}

class Month(Choice):

    def __init__(self, name):
        Choice.__init__(self, name=name, choices=month_names)


class Day(Choice):

    def __init__(self, name):
        Choice.__init__(self, name=name, choices=day_names)


class Year(Alternative):
    alts = [
     IntegerRef('year', 2000, 2100),
     Compound(spec='<century> <year>', extras=[
      Integer('century', 20, 21),
      IntegerRef('year', 10, 100)], value_func=lambda n, e: e['century'] * 100 + e['year']),
     Compound(spec='<century> <year>', extras=[
      Integer('century', 19, 20),
      IntegerRef('year', 1, 100)], value_func=lambda n, e: e['century'] * 100 + e['year'])]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)


class AbsoluteDate(Compound):
    spec = '(<day> <month> | <month> <day>) [<year>]'
    extras = [IntegerRef('day', 1, 32), Month('month'), Year('year')]

    def __init__(self, name):
        Compound.__init__(self, name=name, spec=self.spec, extras=self.extras)

    def value(self, node):
        month = node.get_child_by_name('month').value()
        day = node.get_child_by_name('day').value()
        year_node = node.get_child_by_name('year')
        if year_node is None:
            year = date.today().year
        else:
            year = year_node.value()
        return date(year, month, day)


class RelativeDate(Alternative):

    class _DayOffset(Choice):

        def __init__(self):
            choices = {'<n> days ago': -1, 
               'yesterday': -1, 
               'today': 0, 
               'tomorrow': +1, 
               'in <n> days': +1}
            extras = [
             IntegerRef('n', 1, 100)]
            Choice.__init__(self, name=None, choices=choices, extras=extras)
            return

        def value(self, node):
            value = Choice.value(self, node)
            n = node.get_child_by_name('n')
            print 'November:', n
            if n is not None:
                value = value * n.value()
            return date.today() + timedelta(days=value)

    class _WeekdayOffset(Choice):

        def __init__(self):
            choices = {'(last | past) <day>': 'last day', 
               '(next | this) <day>': 'next day', 
               'last week <day>': 'last week', 
               'next week <day>': 'next week'}
            extras = [
             Day('day')]
            Choice.__init__(self, name=None, choices=choices, extras=extras)
            return

        def value(self, node):
            value = Choice.value(self, node)
            day = node.get_child_by_name('day').value()
            now = date.today().weekday()
            print value, day, now
            if value == 'last day':
                if day < now:
                    day_offset = -now + day
                else:
                    day_offset = -7 - now + day
            elif value == 'next day':
                if day < now:
                    day_offset = 7 - now + day
                else:
                    day_offset = day - now
            elif value == 'last week':
                day_offset = -now - 7 + day
            elif value == 'next week':
                day_offset = -now + 7 + day
            return date.today() + timedelta(days=day_offset)

    alts = [
     _DayOffset(),
     _WeekdayOffset()]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)


class Date(Alternative):
    alts = [
     AbsoluteDate(None),
     RelativeDate(None)]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)


class MilitaryTime(Compound):
    spec = '<hour> (hundred | (oh | zero) <min_1_10> | <min_10_60>)'
    extras = [
     Integer('hour', 0, 25),
     IntegerRef('min_1_10', 1, 10),
     IntegerRef('min_10_60', 10, 60)]

    def __init__(self, name):
        Compound.__init__(self, name=name, spec=self.spec, extras=self.extras)

    def value(self, node):
        hour = node.get_child_by_name('hour').value()
        if node.has_child_with_name('min_1_10'):
            minute = node.get_child_by_name('min_1_10').value()
        elif node.has_child_with_name('min_10_60'):
            minute = node.get_child_by_name('min_10_60').value()
        else:
            minute = 0
        return time(hour, minute)


class Time(Alternative):
    alts = [
     MilitaryTime(None)]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)