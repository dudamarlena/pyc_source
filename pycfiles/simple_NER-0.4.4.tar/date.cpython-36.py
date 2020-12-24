# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/date.py
# Compiled at: 2019-12-12 21:21:32
# Size of source mod 2**32: 39216 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
import re
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from lingua_franca.lang.parse_en import _convert_words_to_numbers_en, is_numeric, extractnumber_en
from lingua_franca.format import nice_duration, nice_date

def _annotate_datetime_en(string, dateNow=None, default_time=None):
    """ Convert a human date reference into an exact datetime

    Convert things like
        "today"
        "tomorrow afternoon"
        "next Tuesday at 4pm"
        "August 3rd"
    into a datetime.  If a reference date is not provided, the current
    local time is used.  Also returns the words used to define the date

    For example, the string
       "what is Tuesday's weather forecast"
    returns the date for the forthcoming Tuesday relative to the reference
    date and the string
       "Tuesday".

    Args:
        string (str): string containing date words
        dateNow (datetime): A reference date/time for "tommorrow", etc
        default_time (time): Time to set if no time was found in the string

    Returns:
        [datetime, str]: An array containing the datetime and the
                         text consumed in the parsing, or None if no
                         date or time related text was found.
    """
    dateNow = dateNow or datetime.now()

    def clean_string(s):
        s = s.lower().replace('?', '').replace('.', '').replace(',', '').replace(' the ', ' ').replace(' a ', ' ').replace(' an ', ' ').replace("o' clock", "o'clock").replace('o clock', "o'clock").replace("o ' clock", "o'clock").replace("o 'clock", "o'clock").replace('oclock', "o'clock").replace('couple', '2').replace('centuries', 'century').replace('decades', 'decade').replace('millenniums', 'millennium')
        wordList = s.split()
        for idx, word in enumerate(wordList):
            word = word.replace("'s", '')
            ordinals = [
             'rd', 'st', 'nd', 'th']
            if word:
                if word[0].isdigit():
                    for ordinal in ordinals:
                        if ordinal in word and 'second' not in word:
                            word = word.replace(ordinal, '')

            wordList[idx] = word

        return wordList

    def date_found():
        return found or datestr != '' or yearOffset != 0 or monthOffset != 0 or dayOffset is True or hrOffset != 0 or hrAbs or minOffset != 0 or minAbs or secOffset != 0

    if string == '' or not dateNow:
        return
    found = False
    daySpecified = False
    dayOffset = False
    monthOffset = 0
    yearOffset = 0
    today = dateNow.strftime('%w')
    currentYear = dateNow.strftime('%Y')
    fromFlag = False
    datestr = ''
    hasYear = False
    timeQualifier = ''
    timeQualifiersAM = [
     'morning']
    timeQualifiersPM = ['afternoon', 'evening', 'night', 'tonight']
    timeQualifiersList = set(timeQualifiersAM + timeQualifiersPM)
    markers = ['at', 'in', 'on', 'by', 'this', 'around', 'for', 'of', 'within']
    days = ['monday', 'tuesday', 'wednesday',
     'thursday', 'friday', 'saturday', 'sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june',
     'july', 'august', 'september', 'october', 'november',
     'december']
    recur_markers = days + [d + 's' for d in days] + ['weekend', 'weekday',
     'weekends', 'weekdays']
    monthsShort = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug',
     'sept', 'oct', 'nov', 'dec']
    year_multiples = ['decade', 'century', 'millennium']
    day_multiples = ['weeks', 'months', 'years']
    words = clean_string(string)
    consumed = []
    for idx, word in enumerate(words):
        if word == '':
            continue
        else:
            wordPrevPrev = words[(idx - 2)] if idx > 1 else ''
            wordPrev = words[(idx - 1)] if idx > 0 else ''
            wordNext = words[(idx + 1)] if idx + 1 < len(words) else ''
            wordNextNext = words[(idx + 2)] if idx + 2 < len(words) else ''
            word = word.rstrip('s')
            start = idx
            used = 0
            if word == 'now':
                if not datestr:
                    resultStr = ' '.join(words[idx + 1:])
                    resultStr = ' '.join(resultStr.split())
                    extractedDate = dateNow.replace(microsecond=0)
                    return [
                     extractedDate, word, resultStr]
            if wordNext in year_multiples:
                multiplier = None
                if is_numeric(word):
                    multiplier = extractnumber_en(word)
                multiplier = multiplier or 1
                multiplier = int(multiplier)
                used += 2
                if wordNext == 'decade':
                    yearOffset = multiplier * 10
                else:
                    if wordNext == 'century':
                        yearOffset = multiplier * 100
                    else:
                        if wordNext == 'millennium':
                            yearOffset = multiplier * 1000
            elif word == '2' and wordNext == 'of' and wordNextNext in year_multiples:
                multiplier = 2
                used += 3
                if wordNextNext == 'decade':
                    yearOffset = multiplier * 10
                else:
                    if wordNextNext == 'century':
                        yearOffset = multiplier * 100
                    else:
                        if wordNextNext == 'millennium':
                            yearOffset = multiplier * 1000
            elif word == '2' and wordNext == 'of' and wordNextNext in day_multiples:
                multiplier = 2
                used += 3
                if wordNextNext == 'years':
                    yearOffset = multiplier
                else:
                    if wordNextNext == 'months':
                        monthOffset = multiplier
                    else:
                        if wordNextNext == 'weeks':
                            dayOffset = multiplier * 7
            else:
                if word in timeQualifiersList:
                    timeQualifier = word
                else:
                    if word == 'today' and not fromFlag:
                        dayOffset = 0
                        used += 1
        if word == 'tomorrow':
            if not fromFlag:
                dayOffset = 1
                used += 1
            if word == 'day' and wordNext == 'after' and wordNextNext == 'tomorrow' and not fromFlag and not wordPrev[0].isdigit():
                dayOffset = 2
                used = 3
                if wordPrev == 'the':
                    start -= 1
                    used += 1
                elif word == 'day' and wordPrev:
                    if wordPrev[0].isdigit():
                        dayOffset += int(wordPrev)
                        start -= 1
                        used = 2
                elif word == 'week' and not fromFlag:
                    if wordPrev[0].isdigit():
                        dayOffset += int(wordPrev) * 7
                        start -= 1
                        used = 2
                    else:
                        if wordPrev == 'next':
                            dayOffset = 7
                            start -= 1
                            used = 2
                        else:
                            if wordPrev == 'last':
                                dayOffset = -7
                                start -= 1
                                used = 2
                elif word == 'month' and not fromFlag:
                    if wordPrev[0].isdigit():
                        monthOffset = int(wordPrev)
                        start -= 1
                        used = 2
                    else:
                        if wordPrev == 'next':
                            monthOffset = 1
                            start -= 1
                            used = 2
                        else:
                            if wordPrev == 'last':
                                monthOffset = -1
                                start -= 1
                                used = 2
                elif word == 'year' and not fromFlag:
                    if wordPrev[0].isdigit():
                        yearOffset = int(wordPrev)
                        start -= 1
                        used = 2
                    else:
                        if wordPrev == 'next':
                            yearOffset = 1
                            start -= 1
                            used = 2
                        else:
                            if wordPrev == 'last':
                                yearOffset = -1
                                start -= 1
                                used = 2
                elif word in days and not fromFlag:
                    d = days.index(word)
                    dayOffset = d + 1 - int(today)
                    used = 1
                    if dayOffset < 0:
                        dayOffset += 7
                    if wordPrev == 'next':
                        dayOffset += 7
                        used += 1
                        start -= 1
                    else:
                        if wordPrev == 'last':
                            dayOffset -= 7
                            used += 1
                            start -= 1
                elif word in months or word in monthsShort and not fromFlag:
                    try:
                        m = months.index(word)
                    except ValueError:
                        m = monthsShort.index(word)

                    used += 1
                    datestr = months[m]
                    if wordPrev:
                        if wordPrev[0].isdigit() or wordPrev == 'of' and wordPrevPrev[0].isdigit():
                            if wordPrev == 'of' and wordPrevPrev[0].isdigit():
                                datestr += ' ' + words[(idx - 2)]
                                used += 1
                                start -= 1
                            else:
                                datestr += ' ' + wordPrev
                        else:
                            start -= 1
                            used += 1
                            if wordNext:
                                if wordNext[0].isdigit():
                                    datestr += ' ' + wordNext
                                    used += 1
                                    hasYear = True
                            hasYear = False
                    elif wordNext:
                        if wordNext[0].isdigit():
                            datestr += ' ' + wordNext
                            used += 1
                            if wordNextNext:
                                if wordNextNext[0].isdigit():
                                    datestr += ' ' + wordNextNext
                                    used += 1
                                    hasYear = True
                            else:
                                hasYear = False
            else:
                validFollowups = days + months + monthsShort
                validFollowups.append('today')
                validFollowups.append('tomorrow')
                validFollowups.append('next')
                validFollowups.append('last')
                validFollowups.append('now')
                if word == 'from' or word == 'after':
                    if wordNext in validFollowups:
                        used = 2
                        fromFlag = True
                        if wordNext == 'tomorrow':
                            dayOffset += 1
                        else:
                            if wordNext in days:
                                d = days.index(wordNext)
                                tmpOffset = d + 1 - int(today)
                                used = 2
                                if tmpOffset < 0:
                                    tmpOffset += 7
                                dayOffset += tmpOffset
                            elif wordNextNext:
                                if wordNextNext in days:
                                    d = days.index(wordNextNext)
                                    tmpOffset = d + 1 - int(today)
                                    used = 3
                                    if wordNext == 'next':
                                        tmpOffset += 7
                                        used += 1
                                        start -= 1
                                    else:
                                        if wordNext == 'last':
                                            tmpOffset -= 7
                                            used += 1
                                            start -= 1
                                        dayOffset += tmpOffset
            if used > 0:
                if start - 1 > 0:
                    if words[(start - 1)] == 'this':
                        start -= 1
                        used += 1
                for i in range(0, used):
                    consumed += [words[(i + start)]]
                    words[i + start] = ''

                if start - 1 >= 0:
                    if words[(start - 1)] in markers:
                        words[start - 1] = ''
                found = True
                daySpecified = True

    hrOffset = 0
    minOffset = 0
    secOffset = 0
    hrAbs = None
    minAbs = None
    military = False
    for idx, word in enumerate(words):
        if word == '':
            continue
        else:
            wordPrevPrev = words[(idx - 2)] if idx > 1 else ''
            wordPrev = words[(idx - 1)] if idx > 0 else ''
            wordNext = words[(idx + 1)] if idx + 1 < len(words) else ''
            wordNextNext = words[(idx + 2)] if idx + 2 < len(words) else ''
            used = 0
            if word == 'noon':
                hrAbs = 12
                used += 1
            else:
                if word == 'midnight':
                    hrAbs = 0
                    used += 1
                else:
                    if word == 'morning':
                        if hrAbs is None:
                            hrAbs = 8
                        used += 1
                    else:
                        if word == 'afternoon':
                            if hrAbs is None:
                                hrAbs = 15
                            used += 1
                        else:
                            if word == 'evening':
                                if hrAbs is None:
                                    hrAbs = 19
                                used += 1
                            elif word == '2' and wordNext == 'of' and wordNextNext in ('hours',
                                                                                       'minutes',
                                                                                       'seconds'):
                                used += 3
                                if wordNextNext == 'hours':
                                    hrOffset = 2
                                else:
                                    if wordNextNext == 'minutes':
                                        minOffset = 2
                                    else:
                                        if wordNextNext == 'seconds':
                                            secOffset = 2
                            else:
                                if word == 'hour' and (wordPrev in markers or wordPrevPrev in markers):
                                    if wordPrev == 'half':
                                        minOffset = 30
                                    else:
                                        if wordPrev == 'quarter':
                                            minOffset = 15
                                        else:
                                            if wordPrevPrev == 'quarter':
                                                minOffset = 15
                                                if idx > 2:
                                                    if words[(idx - 3)] in markers:
                                                        words[idx - 3] = ''
                                                        if words[(idx - 3)] == 'this':
                                                            daySpecified = True
                                                words[idx - 2] = ''
                                            else:
                                                if wordPrev == 'within':
                                                    hrOffset = 1
                                                else:
                                                    hrOffset = 1
                                    if wordPrevPrev in markers:
                                        words[idx - 2] = ''
                                        if wordPrevPrev == 'this':
                                            daySpecified = True
                                    words[idx - 1] = ''
                                    used += 1
                                    hrAbs = -1
                                    minAbs = -1
        if word == 'minute':
            if wordPrev == 'in':
                minOffset = 1
                words[idx - 1] = ''
                used += 1
            elif word == 'second' and wordPrev == 'in':
                secOffset = 1
                words[idx - 1] = ''
                used += 1
            else:
                if word[0].isdigit():
                    isTime = True
                    strHH = ''
                    strMM = ''
                    remainder = ''
                    wordNextNextNext = words[(idx + 3)] if idx + 3 < len(words) else ''
                    if wordNext == 'tonight' or wordNextNext == 'tonight' or wordPrev == 'tonight' or wordPrevPrev == 'tonight' or wordNextNextNext == 'tonight':
                        remainder = 'pm'
                        used += 1
                        if wordPrev == 'tonight':
                            words[idx - 1] = ''
                        if wordPrevPrev == 'tonight':
                            words[idx - 2] = ''
                        if wordNextNext == 'tonight':
                            used += 1
                        if wordNextNextNext == 'tonight':
                            used += 1
                    if ':' in word:
                        stage = 0
                        length = len(word)
                        for i in range(length):
                            if stage == 0:
                                if word[i].isdigit():
                                    strHH += word[i]
                                else:
                                    if word[i] == ':':
                                        stage = 1
                                    else:
                                        stage = 2
                                        i -= 1
                            elif stage == 1:
                                if word[i].isdigit():
                                    strMM += word[i]
                                else:
                                    stage = 2
                                    i -= 1
                            elif stage == 2:
                                remainder = word[i:].replace('.', '')
                                break

                        if remainder == '':
                            nextWord = wordNext.replace('.', '')
                            if nextWord == 'am' or nextWord == 'pm':
                                remainder = nextWord
                                used += 1
                            elif wordNext == 'in':
                                if wordNextNext == 'the':
                                    if words[(idx + 3)] == 'morning':
                                        remainder = 'am'
                                        used += 3
                                else:
                                    if wordNext == 'in':
                                        if wordNextNext == 'the':
                                            if words[(idx + 3)] == 'afternoon':
                                                remainder = 'pm'
                                                used += 3
                                        else:
                                            if wordNext == 'in':
                                                if wordNextNext == 'the':
                                                    if words[(idx + 3)] == 'evening':
                                                        remainder = 'pm'
                                                        used += 3
                                            if wordNext == 'in':
                                                if wordNextNext == 'morning':
                                                    remainder = 'am'
                                                    used += 2
                                            if wordNext == 'in':
                                                if wordNextNext == 'afternoon':
                                                    remainder = 'pm'
                                                    used += 2
                                        if wordNext == 'in' and wordNextNext == 'evening':
                                            remainder = 'pm'
                                            used += 2
                                    else:
                                        if wordNext == 'this' and wordNextNext == 'morning':
                                            remainder = 'am'
                                            used = 2
                                            daySpecified = True
                                    if wordNext == 'this' and wordNextNext == 'afternoon':
                                        remainder = 'pm'
                                        used = 2
                                        daySpecified = True
                                if wordNext == 'this':
                                    if wordNextNext == 'evening':
                                        remainder = 'pm'
                                        used = 2
                                        daySpecified = True
                                    if wordNext == 'at':
                                        if wordNextNext == 'night':
                                            if strHH:
                                                if int(strHH) > 5:
                                                    remainder = 'pm'
                                            else:
                                                remainder = 'am'
                                            used += 2
                                        if timeQualifier != '':
                                            military = True
                                            if strHH and int(strHH) <= 12 and timeQualifier in timeQualifiersPM:
                                                strHH += str(int(strHH) + 12)
                    else:
                        length = len(word)
                        strNum = ''
                        remainder = ''
                        for i in range(length):
                            if word[i].isdigit():
                                strNum += word[i]
                            else:
                                remainder += word[i]

                        if remainder == '':
                            remainder = wordNext.replace('.', '').lstrip().rstrip()
                        if remainder == 'pm' or wordNext == 'pm' or remainder == 'p.m.' or wordNext == 'p.m.':
                            strHH = strNum
                            remainder = 'pm'
                            used = 1
                        else:
                            if remainder == 'am' or wordNext == 'am' or remainder == 'a.m.' or wordNext == 'a.m.':
                                strHH = strNum
                                remainder = 'am'
                                used = 1
                            else:
                                if remainder in recur_markers or wordNext in recur_markers or wordNextNext in recur_markers:
                                    strHH = strNum
                                    used = 1
                                else:
                                    if int(strNum) > 100 and (wordPrev == 'o' or wordPrev == 'oh'):
                                        strHH = str(int(strNum) // 100)
                                        strMM = str(int(strNum) % 100)
                                        military = True
                                        if wordNext == 'hours':
                                            used += 1
                                    else:
                                        if wordNext == 'hours' or wordNext == 'hour' or remainder == 'hours' or remainder == 'hour':
                                            if word[0] != '0':
                                                if int(strNum) < 100 or int(strNum) > 2400:
                                                    hrOffset = int(strNum)
                                                    used = 2
                                                    isTime = False
                                                    hrAbs = -1
                                                    minAbs = -1
                                        if wordNext == 'minutes' or wordNext == 'minute' or remainder == 'minutes' or remainder == 'minute':
                                            minOffset = int(strNum)
                                            used = 2
                                            isTime = False
                                            hrAbs = -1
                                            minAbs = -1
                                        else:
                                            if wordNext == 'seconds' or wordNext == 'second' or remainder == 'seconds' or remainder == 'second':
                                                secOffset = int(strNum)
                                                used = 2
                                                isTime = False
                                                hrAbs = -1
                                                minAbs = -1
                                            else:
                                                if int(strNum) > 100:
                                                    strHH = str(int(strNum) // 100)
                                                    strMM = str(int(strNum) % 100)
                                                    military = True
                                                    if wordNext == 'hours' or wordNext == 'hour' or remainder == 'hours' or remainder == 'hour':
                                                        used += 1
                                                else:
                                                    if wordNext:
                                                        if wordNext[0].isdigit():
                                                            strHH = strNum
                                                            strMM = wordNext
                                                            military = True
                                                            used += 1
                                                            if wordNextNext == 'hours' or wordNextNext == 'hour' or remainder == 'hours' or remainder == 'hour':
                                                                used += 1
                                                        else:
                                                            if wordNext == '' or wordNext == "o'clock" or wordNext == 'in' and (wordNextNext == 'the' or wordNextNext == timeQualifier) or wordNext == 'tonight' or wordNextNext == 'tonight':
                                                                strHH = strNum
                                                                strMM = '00'
                                                                if wordNext == "o'clock":
                                                                    used += 1
                                                                if wordNext == 'in' or wordNextNext == 'in':
                                                                    used += 1 if wordNext == 'in' else 2
                                                                    wordNextNextNext = words[(idx + 3)] if idx + 3 < len(words) else ''
                                                                    if wordNextNext:
                                                                        if wordNextNext in timeQualifier or wordNextNextNext in timeQualifier:
                                                                            if wordNextNext in timeQualifiersPM or wordNextNextNext in timeQualifiersPM:
                                                                                remainder = 'pm'
                                                                                used += 1
                                                                            if wordNextNext in timeQualifiersAM or wordNextNextNext in timeQualifiersAM:
                                                                                remainder = 'am'
                                                                                used += 1
                                                                if timeQualifier != '':
                                                                    if timeQualifier in timeQualifiersPM:
                                                                        remainder = 'pm'
                                                                        used += 1
                                                                    else:
                                                                        if timeQualifier in timeQualifiersAM:
                                                                            remainder = 'am'
                                                                            used += 1
                                                                        else:
                                                                            used += 1
                                                                            military = True
                                                            else:
                                                                isTime = False
                                                        HH = int(strHH) if strHH else 0
                                                        MM = int(strMM) if strMM else 0
                                                        HH = HH + 12 if (remainder == 'pm' and HH < 12) else HH
                                                        HH = HH - 12 if (remainder == 'am' and HH >= 12) else HH
                                                        if not military:
                                                            if remainder not in ('am',
                                                                                 'pm',
                                                                                 'hours',
                                                                                 'minutes',
                                                                                 'second',
                                                                                 'seconds',
                                                                                 'hour',
                                                                                 'minute'):
                                                                if not daySpecified or dayOffset < 1:
                                                                    if not dateNow.hour < HH:
                                                                        if dateNow.hour == HH and dateNow.minute < MM:
                                                                            pass
                                                                        else:
                                                                            if dateNow.hour < HH + 12:
                                                                                HH += 12
                                                                            else:
                                                                                dayOffset += 1
                                                    else:
                                                        if timeQualifier in timeQualifiersPM:
                                                            if HH < 12:
                                                                HH += 12
                                                        if HH > 24 or MM > 59:
                                                            isTime = False
                                                            used = 0
                                                    if isTime:
                                                        hrAbs = HH
                                                        minAbs = MM
                                                        used += 1
            if used > 0:
                for i in range(used):
                    if idx + i >= len(words):
                        break
                    consumed += [words[(idx + i)]]
                    words[idx + i] = ''

                if wordPrev == 'o' or wordPrev == 'oh':
                    words[words.index(wordPrev)] = ''
                if wordPrev == 'early':
                    hrOffset = -1
                    words[idx - 1] = ''
                    idx -= 1
                else:
                    if wordPrev == 'late':
                        hrOffset = 1
                        words[idx - 1] = ''
                        idx -= 1
                if idx > 0:
                    if wordPrev in markers:
                        words[idx - 1] = ''
                        if wordPrev == 'this':
                            daySpecified = True
                if idx > 1:
                    if wordPrevPrev in markers:
                        words[idx - 2] = ''
                        if wordPrevPrev == 'this':
                            daySpecified = True
                idx += used - 1
                found = True

    if not date_found:
        return
    if dayOffset is False:
        dayOffset = 0
    extractedDate = dateNow.replace(microsecond=0)
    if datestr != '':
        if '-' in datestr:
            datestr = datestr.split('-')[0]
        try:
            temp = datetime.strptime(datestr, '%B %d')
        except ValueError:
            try:
                temp = datetime.strptime(datestr, '%B %d %Y')
            except ValueError:
                try:
                    temp = datetime.strptime(datestr, '%B %Y')
                except ValueError:
                    temp = datetime.strptime(datestr, '%B')

        extractedDate = extractedDate.replace(hour=0, minute=0, second=0)
        if not hasYear:
            temp = temp.replace(year=(extractedDate.year), tzinfo=(extractedDate.tzinfo))
            if extractedDate < temp:
                extractedDate = extractedDate.replace(year=(int(currentYear)),
                  month=(int(temp.strftime('%m'))),
                  day=(int(temp.strftime('%d'))),
                  tzinfo=(extractedDate.tzinfo))
            else:
                extractedDate = extractedDate.replace(year=(int(currentYear) + 1),
                  month=(int(temp.strftime('%m'))),
                  day=(int(temp.strftime('%d'))),
                  tzinfo=(extractedDate.tzinfo))
        else:
            extractedDate = extractedDate.replace(year=(int(temp.strftime('%Y'))),
              month=(int(temp.strftime('%m'))),
              day=(int(temp.strftime('%d'))),
              tzinfo=(extractedDate.tzinfo))
    else:
        if hrOffset == 0:
            if minOffset == 0:
                if secOffset == 0:
                    extractedDate = extractedDate.replace(hour=0, minute=0, second=0)
                else:
                    if yearOffset != 0:
                        extractedDate = extractedDate + relativedelta(years=yearOffset)
                    if monthOffset != 0:
                        extractedDate = extractedDate + relativedelta(months=monthOffset)
                if dayOffset != 0:
                    extractedDate = extractedDate + relativedelta(days=dayOffset)
            else:
                if hrAbs != -1:
                    if minAbs != -1:
                        if hrAbs is None:
                            if minAbs is None:
                                if default_time is not None:
                                    hrAbs, minAbs = default_time.hour, default_time.minute
                        else:
                            hrAbs = hrAbs or 0
                            minAbs = minAbs or 0
                        extractedDate = extractedDate + relativedelta(hours=hrAbs, minutes=minAbs)
                        if hrAbs != 0 or minAbs != 0:
                            if datestr == '':
                                if not daySpecified:
                                    if dateNow > extractedDate:
                                        extractedDate = extractedDate + relativedelta(days=1)
            if hrOffset != 0:
                extractedDate = extractedDate + relativedelta(hours=hrOffset)
        else:
            if minOffset != 0:
                extractedDate = extractedDate + relativedelta(minutes=minOffset)
            if secOffset != 0:
                extractedDate = extractedDate + relativedelta(seconds=secOffset)
        for idx, word in enumerate(words):
            if words[idx] == 'and' and words[(idx - 1)] == '' and words[(idx + 1)] == '':
                words[idx] = ''

        resultStr = ' '.join(consumed)
        resultStr = ' '.join(resultStr.split())
        remStr = ' '.join(words)
        return [
         extractedDate, resultStr, remStr]


def _annotate_duration_en(text):
    """
    Convert an english phrase into a number of seconds

    Convert things like:
        "10 minute"
        "2 and a half hours"
        "3 days 8 hours 10 minutes and 49 seconds"
    into an int, representing the total number of seconds.

    The words used in the duration will be returned.

    As an example, "set a timer for 5 minutes" would return
    (300, "5 minutes").

    Reverse of extract_duration_en

    Args:
        text (str): string containing a duration

    Returns:
        (timedelta, str):
                    A tuple containing the duration and the text
                    consumed in the parsing. The first value will
                    be None if no duration is found.
    """
    if not text:
        return
    else:
        time_units = {'microseconds':None, 
         'milliseconds':None, 
         'seconds':None, 
         'minutes':None, 
         'hours':None, 
         'days':None, 
         'weeks':None}
        time_units2 = {'years':None, 
         'months':None, 
         'weeks':None, 
         'decades':None}
        pattern = '(?P<value>\\d+(?:\\.?\\d+)?)\\s+{unit}s?'
        norm_text = _convert_words_to_numbers_en(text)
        t = norm_text
        duration_text = text
        start = -1
        end = -1
        for unit in time_units:
            unit_pattern = pattern.format(unit=(unit[:-1]))
            matches = re.findall(unit_pattern, t)
            value = sum(map(float, matches))
            time_units[unit] = value
            t = re.sub(unit_pattern, '', t)
            if matches:
                n_start = norm_text.find(str(int(value)))
                if start < 0 or n_start < start:
                    start = n_start
                n_end = text.rfind(unit) + len(unit)
                if n_end > end:
                    end = n_end

        for unit in time_units2:
            unit_pattern = pattern.format(unit=(unit[:-1]))
            matches = re.findall(unit_pattern, t)
            value = sum(map(float, matches))
            t = re.sub(unit_pattern, '', t)
            if matches:
                if time_units['days'] is None:
                    time_units['days'] = 0
                if unit == 'years':
                    time_units['days'] += value * 365
                else:
                    if unit == 'months':
                        time_units['days'] += value * 30
                    else:
                        if unit == 'weeks':
                            time_units['days'] += value * 7
                        else:
                            if unit == 'decades':
                                time_units['days'] += value * 3650
                n_start = norm_text.find(str(int(value)))
                if start < 0 or n_start < start:
                    start = n_start
                n_end = text.rfind(unit) + len(unit)
                if n_end > end:
                    end = n_end

        if start > -1:
            if end > start:
                duration_text = duration_text[start:end]
            else:
                duration_text = duration_text[start:]
        duration = timedelta(**time_units) if any(time_units.values()) else None
        return (
         duration, duration_text.strip())


class DateTimeNER(NERWrapper):

    def __init__(self, anchor_date=None):
        super().__init__()
        self.anchor_date = anchor_date or datetime.now()
        self.add_detector(self.annotate_datetime)
        self.add_detector(self.annotate_duration)

    def annotate_duration(self, text):
        delta, value = _annotate_duration_en(text)
        if delta:
            data = {'days':delta.days,  'seconds':delta.seconds, 
             'microseconds':delta.microseconds, 
             'total_seconds':delta.total_seconds(), 
             'spoken':nice_duration(delta)}
            yield Entity(value, 'duration', source_text=text, data=data)

    def annotate_datetime(self, text):
        date, value, rem = _annotate_datetime_en(text, self.anchor_date)
        while value:
            try:
                data = {'timestamp':date.timestamp(), 
                 'isoformat':date.isoformat(), 
                 'weekday':date.isoweekday(), 
                 'month':date.month, 
                 'day':date.day, 
                 'hour':date.hour, 
                 'minute':date.minute, 
                 'year':date.year, 
                 'spoken':nice_date(date, now=self.anchor_date)}
                yield Entity(value, 'relative_date', source_text=text, data=data)
            except OverflowError:
                yield Entity(value, 'date', source_text=text, data={'spoken': value})

            if not rem:
                return
            date, value, rem = _annotate_datetime_en(rem, self.anchor_date)

    def annotate(self, text):
        from dateparser.search import search_dates
        matches = search_dates(text)
        for value, date in matches:
            data = {'timestamp':date.timestamp(),  'isoformat':date.isoformat(), 
             'weekday':date.isoweekday(), 
             'month':date.month, 
             'day':date.day, 
             'hour':date.hour, 
             'minute':date.minute, 
             'year':date.year}
            yield Entity(value, 'date', source_text=text, data=data)


if __name__ == '__main__':
    from pprint import pprint
    ner = DateTimeNER()
    for r in ner.extract_entities('What President served for five years , six months and 2 days ?'):
        pprint(r.as_json())

    for r in ner.extract_entities('my birthday is on december 5th'):
        pprint(r.as_json())

    for r in ner.extract_entities('starts in 5 minutes'):
        pprint(r.as_json())