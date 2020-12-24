# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pystamp/pystamp.py
# Compiled at: 2011-07-19 23:27:21
import re, calendar
from datetime import datetime

def format_like(obj, formatstr):
    translator = DateTimeTranslator(obj)
    return translator.format_like(formatstr)


class DateTimeTranslator(object):
    """
    DateTimeTranslator
    ------------------
    """
    MONTHNAME_REGEXP = '^(' + ('|').join(calendar.month_name[1:]) + ')$'
    ABBR_MONTHNAMES_REGEXP = '^(' + ('|').join(calendar.month_abbr[1:]) + ')$'
    DAYNAMES_REGEXP = '^(' + ('|').join(calendar.day_name) + ')$'
    ABBR_DAYNAMES_REGEXP = '^(' + ('|').join(calendar.day_abbr) + ')$'
    TIME_REGEXP = '(\\d{1,2})(:)(\\d{2})(\\s*)(:)?(\\d{2})?(\\s*)([ap]m)?'
    ONE_DIGIT_REGEXP = '^\\d{1}$'
    TWO_DIGIT_REGEXP = '^\\d{2}$'
    FOUR_DIGIT_REGEXP = '^\\d{4}$'
    MERIDIAN_LOWER_REGEXP = '^(a|p)m$'
    TWO_DIGIT_DATE_SUCCESSION = {'%m': '%d', 
       '%b': '%d', 
       '%B': '%d', 
       '%d': '%y', 
       '%e': '%y'}
    TWO_DIGIT_TIME_SUCCESSION = {'%H': '%M', 
       '%I': '%M', 
       '%M': '%S'}

    def __init__(self, target=datetime.utcnow()):
        self.target = target

    def format_like(self, example):
        return self.target.strftime(self.translate(example))

    def translate(self, example):
        before, time_example, after = DateTimeTranslator.extract_time(example)
        before_words = re.split('(\\W+)', before)
        words = []
        previous_directive = None
        for token in self.convert_directives(before_words):
            tmp = self.convert_date_directive(token, previous_directive)
            if tmp:
                if tmp != token:
                    previous_directive = tmp
                words.append(tmp)

        if time_example:
            tokens = re.findall(DateTimeTranslator.TIME_REGEXP, time_example)[0]
            previous_directive = None
            for token in self.convert_directives(tokens):
                tmp = self.convert_time_directive(token, previous_directive)
                if tmp:
                    if tmp != token:
                        previous_directive = tmp
                    words.append(tmp)

        if after:
            words.append(self.translate(after))
        return ('').join(words)

    def convert_directives(self, tokens):
        for token in tokens:
            yield token

    def convert_time_directive(self, token, previous_directive):
        cls = DateTimeTranslator
        if re.match(cls.MERIDIAN_LOWER_REGEXP, token.lower()):
            return '%p'
        else:
            if re.match(cls.TWO_DIGIT_REGEXP, token):
                should_be = cls.TWO_DIGIT_TIME_SUCCESSION.get(previous_directive, None)
                if 24 > int(token) > 12:
                    if not should_be:
                        return '%H'
                    return should_be
                if not should_be:
                    return '%I'
                return should_be
            else:
                if re.match(cls.ONE_DIGIT_REGEXP, token):
                    return '%I'
                else:
                    return token

            return

    def convert_date_directive(self, token, previous_directive):
        cls = DateTimeTranslator
        if re.match(cls.MONTHNAME_REGEXP, token, re.I):
            return '%B'
        else:
            if re.match(cls.ABBR_MONTHNAMES_REGEXP, token, re.I):
                return '%b'
            if re.match(cls.DAYNAMES_REGEXP, token, re.I):
                return '%A'
            if re.match(cls.ABBR_DAYNAMES_REGEXP, token, re.I):
                return '%a'
            if re.match(cls.FOUR_DIGIT_REGEXP, token):
                return '%Y'
            if re.match(cls.TWO_DIGIT_REGEXP, token):
                should_be = cls.TWO_DIGIT_DATE_SUCCESSION.get(previous_directive, None)
                if 99 >= int(token) >= 32:
                    return '%y'
                if 31 >= int(token) >= 13:
                    return '%d'
                if should_be:
                    return should_be
                return '%m'
            else:
                if re.match(cls.ONE_DIGIT_REGEXP, token):
                    return '%e'
                else:
                    return token

            return

    @classmethod
    def extract_time(cls, example):
        """
        Extract any substring that looks like time (i.e 10:10 or 10:10 am) ::

            >>> DateTimeTranslator.extract_time("March 1, 2010 10:10")
            >>> ("March 1, 2010", "10:10")

        Please notice that we donot validate the time here, only capture the
        format
        :return a tuple contains (before, time_example, after)
        """
        matcher = re.search(cls.TIME_REGEXP, example)
        if matcher:
            matched_time = matcher.group().strip()
            return example.partition(matched_time)
        else:
            return (
             example, None, None)
            return