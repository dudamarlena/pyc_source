# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgerber/anaconda3/lib/python3.4/site-packages/getTimer/getTimerDateTime.py
# Compiled at: 2016-02-12 14:25:52
# Size of source mod 2**32: 2231 bytes
import curses, datetime
from .getTimerDate import *
from .getTimerTime import *

def displayDateTime(scr, day, time, cursor, topString, bottomString):
    string = day.isoformat() + ' ' + time.isoformat()
    max_y, max_x = scr.getmaxyx()
    y = int(max_y / 2)
    x = int(max_x / 2) - 9
    scr.addstr(y - 2, x - int(len(topString) / 2) + 9, topString)
    scr.addstr(y, x, string[0:cursor])
    scr.addstr(y, x + cursor, string[cursor:cursor + 1], curses.A_REVERSE)
    scr.addstr(y, x + cursor + 1, string[cursor + 1:])
    scr.addstr(y + 2, x - int(len(bottomString) / 2) + 9, bottomString)
    scr.refresh()


def runDateTime(scr, rollover, topString, bottomString, dt=None):
    if rollover:
        if dt == None:
            d = date.today()
            t = time()
        else:
            d = date(dt.year, dt.month, dt.day)
            t = time(dt.hour, dt.minute, dt.second)
    elif dt == None:
        d = datetime.date.today()
        t = datetime.time()
    c = curses.KEY_MAX
    cursor = 3
    while c != 10:
        displayDateTime(scr, d, t, cursor, topString, bottomString)
        c = scr.getch()
        if c == curses.KEY_RIGHT and cursor < 18:
            cursor += 1
            if cursor in (4, 7, 10, 13, 16):
                cursor += 1
        elif c == curses.KEY_LEFT and cursor > 0:
            cursor -= 1
            if cursor in (4, 7, 10, 13, 16):
                cursor -= 1
        elif c == curses.KEY_UP:
            if cursor < 10:
                d = _alterDigitDay(cursor, d, 1)
            else:
                t = alterDigitTime(cursor - 11, t, 1)
        elif c == curses.KEY_DOWN:
            if cursor < 10:
                d = _alterDigitDay(cursor, d, -1)
            else:
                t = alterDigitTime(cursor - 11, t, -1)
        else:
            try:
                i = int(c) - 48
                if i >= 0:
                    if i < 10:
                        if cursor < 10:
                            d = updateDigitDay(cursor, d, i)
                        else:
                            t = updateDigitTime(cursor - 11, t, i)
            except ValueError:
                pass

    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)