# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/browseRF.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import curses, re, sys, subprocess
from pyfeld.dirBrowse import DirBrowse
returnString = None

class MainGui:

    def __init__(self):
        self.selected_index_stack = [
         0]
        self.returnString = b''
        self.play_in_room = None
        self.dir = DirBrowse()
        self.selected_index = 0
        self.selected_column = 0
        self.window = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        self.window.keypad(1)
        self.draw_ui()
        return

    def set_room(self, room):
        self.play_in_room = room

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def draw_ui(self):
        self.window.clear()
        self.window.addstr(0, 0, b'Path:  ' + self.dir.get_friendly_path_name(b'>'))
        self.screen_height, self.screen_width = self.window.getmaxyx()
        self.window.addstr(0, 0, b'')
        self.window.addstr(self.screen_height - 2, 0, b'Arrow keys: select device')
        self.window.addstr(self.screen_height - 1, 0, b'P)lay S)top H)elp Q)uit Return')
        self.show_dir()
        self.window.refresh()

    def show_dir(self):
        try:
            for i in range(0, self.dir.max_entries_on_level()):
                if i == self.selected_index:
                    col = curses.color_pair(1)
                else:
                    col = curses.color_pair(3)
                if self.dir.get_type(i) == b'D':
                    vis_string = b'> '
                else:
                    vis_string = b'  '
                vis_string += self.dir.get_friendly_name(i)
                self.window.addstr(i + 3, 0, vis_string, col)

        except:
            pass

    def enter_dir(self):
        self.dir.enter(self.selected_index)

    def leave_dir(self):
        self.dir.leave()

    def play(self):
        path = self.dir.get_path_for_index(self.selected_index).decode(b'utf-8')
        if self.play_in_room is None:
            command = b'pyfeld -z 0 play "' + path + b'"'
        else:
            command = b'pyfeld --zonewithroom "' + self.play_in_room + b'" play "' + path + b'"'
        self.window.addstr(1, 0, command)
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            self.window.addstr(0, 0, b'Launching pyfeld failed')
            return 0

        lines = list()
        while True:
            nextline = process.stdout.readline()
            if len(nextline) == 0 and process.poll() != None:
                break

        self.window.addstr(1, 0, str(lines))
        return lines

    def run_main_loop(self):
        self.draw_ui()
        while 1:
            c = self.window.getch()
            if curses.keyname(c) in ('h', 'H'):
                self.show_help()
            elif curses.keyname(c) in ('p', 'P'):
                self.play()
            else:
                if curses.keyname(c) in ('q', 'Q'):
                    return
                if c == 27:
                    self.returnString = self.dir.get_current_path()
                    return self.returnString
                if c == curses.KEY_ENTER or c == 10:
                    self.returnString = self.dir.get_current_path()
                    return self.returnString
                if c == curses.KEY_UP:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                    self.draw_ui()
                elif c == curses.KEY_DOWN:
                    if self.selected_index < self.dir.max_entries_on_level() - 1:
                        self.selected_index += 1
                    self.draw_ui()
                elif c == curses.KEY_LEFT:
                    self.leave_dir()
                    self.draw_ui()
                elif c == curses.KEY_RIGHT:
                    self.enter_dir()
                    self.draw_ui()
                elif c == curses.KEY_RESIZE:
                    self.draw_ui()

        return


def show_dir(dir_browser):
    for i in range(0, dir_browser.max_entries_on_level() - 1):
        print dir_browser.get_friendly_name(i)


def test_dir():
    dir_browser = DirBrowse()
    print dir_browser.path
    show_dir(dir_browser)
    dir_browser.enter(1)
    print dir_browser.path
    show_dir(dir_browser)
    dir_browser.enter(4)
    print dir_browser.path
    show_dir(dir_browser)
    dir_browser.leave()
    print dir_browser.path
    show_dir(dir_browser)


def run_main():
    global returnString
    argv = sys.argv[1:]
    if len(argv) == 1:
        if argv[0] == b'test':
            test_dir()
            return
        if argv[0] == b'--help':
            print b'Usage:'
            print b'--zonewithroom {room}'
            return
    with MainGui() as (gui):
        inroom = None
        if len(argv) >= 1:
            index = 0
            if argv[0] == b'--zonewithroom':
                gui.set_room(argv[1])
        returnString = gui.run_main_loop()
    return


if __name__ == b'__main__':
    run_main()
if returnString is not None:
    sys.stdout.write(returnString.decode(b'utf-8'))
    sys.stdout.write(b'\n')