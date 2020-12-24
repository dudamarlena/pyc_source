# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /elicit/widgets.py
# Compiled at: 2018-08-13 00:06:39
# Size of source mod 2**32: 3358 bytes
"""
Simple forms and user inputs using curses module.
"""
import sys, signal, curses, curses.ascii, curses.textpad, locale
from shutil import get_terminal_size
locale.setlocale(locale.LC_ALL, '')
LANG, ENCODING = locale.getlocale()
COLUMNS = LINES = None

def _reset_size(sig, tr):
    global COLUMNS
    global LINES
    COLUMNS, LINES = get_terminal_size()


_reset_size(signal.SIGWINCH, None)
signal.signal(signal.SIGWINCH, _reset_size)

def choose(somelist, defidx=0, prompt='choose', lines=LINES, columns=COLUMNS):
    return curses.wrapper(_choose, somelist, defidx, prompt, lines, columns)


def _choose(stdscr, somelist, defidx, prompt, lines, columns):
    oldcur = curses.curs_set(0)
    pad = curses.newpad(len(somelist) + 1, columns - 2)
    for line in somelist:
        pad.addstr(str(line))

    pminrow = defidx
    pmincol = 0
    sminrow = (lines - 3) // 2
    smincol = 1
    smaxrow = lines - 3
    smaxcol = columns - 2
    topwin = stdscr.subwin(sminrow, columns - 2, 2, 1)
    stdscr.clear()
    stdscr.addstr('{} (Press Enter to select)'.format(prompt))
    curses.textpad.rectangle(stdscr, 1, 0, lines - 2, columns - 1)
    stdscr.refresh()
    pad.chgat(pminrow, 0, smaxcol - 1, curses.A_REVERSE)
    pad.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
    J, K = [b'jk'[i] for i in range(2)]
    esc = False
    while True:
        ch = stdscr.getch()
        if ch in (curses.KEY_DOWN, J):
            pminrow = min(len(somelist) - 1, max(0, pminrow + 1))
        else:
            if ch in (curses.KEY_UP, K):
                pminrow = max(0, min(len(somelist), pminrow - 1))
            else:
                if ch == curses.ascii.NL:
                    break
                else:
                    if ch == curses.ascii.ESC:
                        esc = True
                        break
                    if pminrow > 0:
                        topwin.clear()
                    pad.chgat(pminrow + 1, 0, smaxcol - 1, curses.A_NORMAL)
                    pad.chgat(pminrow, 0, smaxcol - 1, curses.A_REVERSE)
                    pad.noutrefresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
                    curses.doupdate()

    curses.curs_set(oldcur)
    if esc:
        return
    return somelist[pminrow]


def _test(argv):
    with open('/etc/protocols') as (fo):
        lines = fo.readlines()
    print(choose(lines, defidx=3, prompt='Pick a service'))


if __name__ == '__main__':
    _test(sys.argv)