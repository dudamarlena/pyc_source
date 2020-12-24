# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/head_controller/curses_demo.py
# Compiled at: 2019-10-26 18:25:01
# Size of source mod 2**32: 2920 bytes
import sys, os, curses

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    while k != ord('q'):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        else:
            if k == curses.KEY_UP:
                cursor_y = cursor_y - 1
            else:
                if k == curses.KEY_RIGHT:
                    cursor_x = cursor_x + 1
                else:
                    if k == curses.KEY_LEFT:
                        cursor_x = cursor_x - 1
        cursor_x = max(0, cursor_x)
        cursor_x = min(width - 1, cursor_x)
        cursor_y = max(0, cursor_y)
        cursor_y = min(height - 1, cursor_y)
        title = 'Curses example'[:width - 1]
        subtitle = 'Written by Clay McLeod'[:width - 1]
        keystr = 'Last key pressed: {}'.format(k)[:width - 1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = 'No key press detected...'[:width - 1]
        start_x_title = int(width // 2 - len(title) // 2 - len(title) % 2)
        start_x_subtitle = int(width // 2 - len(subtitle) // 2 - len(subtitle) % 2)
        start_x_keystr = int(width // 2 - len(keystr) // 2 - len(keystr) % 2)
        start_y = int(height // 2 - 2)
        whstr = 'Width: {}, Height: {}'.format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(height - 1, len(statusbarstr), ' ' * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y, start_x_title, title)
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, width // 2 - 2, '----')
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)


if __name__ == '__main__':
    main()