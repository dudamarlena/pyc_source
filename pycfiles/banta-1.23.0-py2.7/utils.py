# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\utils.py
# Compiled at: 2012-12-01 19:03:54
"""
Some utility stuff
"""
import datetime, time, csv, codecs, cStringIO

class Timer(object):

    def __init__(self, name='-', verbose=True):
        from timeit import default_timer
        self.verbose = verbose
        self.timer = default_timer
        self.name = name

    def __enter__(self):
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        self.elapsed_secs = self.timer() - self.start
        self.elapsed = self.elapsed_secs * 1000
        if self.verbose:
            print '[%s] Elapsed: %f ms' % (self.name, self.elapsed)


FORBIDDEN_CHARACTERS = ('\n', '\t', '\r')

def printable(text):
    for c in FORBIDDEN_CHARACTERS:
        text = text.replace(c, ' ')

    return text


def unitr(oldtr):

    def utr(u, *args):
        if isinstance(u, unicode):
            u = u.encode('utf-8')
        else:
            print 'not unicode:', u
        return oldtr(u, *args)

    return utr


def currentMonthDates():
    """Returns the dates for the current month as a tuple of datetime
        Return ( Start of month, Today, End of Month)"""
    today = datetime.date.today()
    month_start = today - datetime.timedelta(days=today.day - 1)
    year = today.year
    month = today.month + 1
    if month > 12:
        month = 1
        year += 1
    month_end = datetime.date(year, month, 1)
    return (month_start, today, month_end)


def dateTimeToInt(d):
    """Covenverts a datetime object to a integer.
                        Used in models.Bill as key and everywhere where is needed some comparison of those keys
        """
    return int(time.mktime(d.timetuple()))


def getTimesFromFilters(date_min, date_max):
    """Returns a touple of times from the date widgets.
                The data format is the same as the key in bill_list
                date_min and date_max are two QDateEdit with min and max dates respectively
        """
    dmin = date_min.date().toPython()
    dmax = date_max.date().toPython() + datetime.timedelta(days=1)
    tmin = dateTimeToInt(dmin)
    tmax = dateTimeToInt(dmax)
    return (tmin, tmax)


class UTF8Recoder:
    """
Iterator that reads an encoded stream and reencodes the input to UTF-8
"""

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('utf-8')


class UnicodeCSVReader:
    """
A CSV reader which will iterate over lines in the CSV file "f",
which is encoded in the given encoding.
"""

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [ unicode(s, 'utf-8') for s in row ]

    def __iter__(self):
        return self


class UnicodeCSVWriter:
    """
A CSV writer which will write rows to CSV file "f",
which is encoded in the given encoding.
"""

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([ s.encode('utf-8') for s in row ])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def resourcePath(relative):
    """This functions convert a relative virtual path to a system path for a resource built in into an exe by pyinstaller
        """
    import os
    return os.path.join(os.environ.get('_MEIPASS2', os.path.abspath('.')), relative)