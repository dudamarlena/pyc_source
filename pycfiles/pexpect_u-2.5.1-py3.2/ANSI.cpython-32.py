# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/ANSI.py
# Compiled at: 2011-11-02 15:34:07
"""This implements an ANSI (VT100) terminal emulator as a subclass of screen.

$Id: ANSI.py 525 2010-10-31 14:30:37Z noah $
"""
from . import screen
from . import FSM
import copy, string

def DoEmit(fsm):
    screen = fsm.memory[0]
    screen.write_ch(fsm.input_symbol)


def DoStartNumber(fsm):
    fsm.memory.append(fsm.input_symbol)


def DoBuildNumber(fsm):
    ns = fsm.memory.pop()
    ns = ns + fsm.input_symbol
    fsm.memory.append(ns)


def DoBackOne(fsm):
    screen = fsm.memory[0]
    screen.cursor_back()


def DoBack(fsm):
    count = int(fsm.memory.pop())
    screen = fsm.memory[0]
    screen.cursor_back(count)


def DoDownOne(fsm):
    screen = fsm.memory[0]
    screen.cursor_down()


def DoDown(fsm):
    count = int(fsm.memory.pop())
    screen = fsm.memory[0]
    screen.cursor_down(count)


def DoForwardOne(fsm):
    screen = fsm.memory[0]
    screen.cursor_forward()


def DoForward(fsm):
    count = int(fsm.memory.pop())
    screen = fsm.memory[0]
    screen.cursor_forward(count)


def DoUpReverse(fsm):
    screen = fsm.memory[0]
    screen.cursor_up_reverse()


def DoUpOne(fsm):
    screen = fsm.memory[0]
    screen.cursor_up()


def DoUp(fsm):
    count = int(fsm.memory.pop())
    screen = fsm.memory[0]
    screen.cursor_up(count)


def DoHome(fsm):
    c = int(fsm.memory.pop())
    r = int(fsm.memory.pop())
    screen = fsm.memory[0]
    screen.cursor_home(r, c)


def DoHomeOrigin(fsm):
    c = 1
    r = 1
    screen = fsm.memory[0]
    screen.cursor_home(r, c)


def DoEraseDown(fsm):
    screen = fsm.memory[0]
    screen.erase_down()


def DoErase(fsm):
    arg = int(fsm.memory.pop())
    screen = fsm.memory[0]
    if arg == 0:
        screen.erase_down()
    else:
        if arg == 1:
            screen.erase_up()
        elif arg == 2:
            screen.erase_screen()


def DoEraseEndOfLine(fsm):
    screen = fsm.memory[0]
    screen.erase_end_of_line()


def DoEraseLine(fsm):
    arg = int(fsm.memory.pop())
    screen = fsm.memory[0]
    if arg == 0:
        screen.erase_end_of_line()
    else:
        if arg == 1:
            screen.erase_start_of_line()
        elif arg == 2:
            screen.erase_line()


def DoEnableScroll(fsm):
    screen = fsm.memory[0]
    screen.scroll_screen()


def DoCursorSave(fsm):
    screen = fsm.memory[0]
    screen.cursor_save_attrs()


def DoCursorRestore(fsm):
    screen = fsm.memory[0]
    screen.cursor_restore_attrs()


def DoScrollRegion(fsm):
    screen = fsm.memory[0]
    r2 = int(fsm.memory.pop())
    r1 = int(fsm.memory.pop())
    screen.scroll_screen_rows(r1, r2)


def DoMode(fsm):
    screen = fsm.memory[0]
    mode = fsm.memory.pop()


def DoLog(fsm):
    screen = fsm.memory[0]
    fsm.memory = [screen]
    fout = open('log', 'a')
    fout.write(fsm.input_symbol + ',' + fsm.current_state + '\n')
    fout.close()


class term(screen.screen):
    """This class is an abstract, generic terminal.
    This does nothing. This is a placeholder that
    provides a common base class for other terminals
    such as an ANSI terminal. """

    def __init__(self, r=24, c=80):
        screen.screen.__init__(self, r, c)


class ANSI(term):
    """This class implements an ANSI (VT100) terminal.
    It is a stream filter that recognizes ANSI terminal
    escape sequences and maintains the state of a screen object. """

    def __init__(self, r=24, c=80):
        term.__init__(self, r, c)
        self.state = FSM.FSM('INIT', [self])
        self.state.set_default_transition(DoLog, 'INIT')
        self.state.add_transition_any('INIT', DoEmit, 'INIT')
        self.state.add_transition('\x1b', 'INIT', None, 'ESC')
        self.state.add_transition_any('ESC', DoLog, 'INIT')
        self.state.add_transition('(', 'ESC', None, 'G0SCS')
        self.state.add_transition(')', 'ESC', None, 'G1SCS')
        self.state.add_transition_list('AB012', 'G0SCS', None, 'INIT')
        self.state.add_transition_list('AB012', 'G1SCS', None, 'INIT')
        self.state.add_transition('7', 'ESC', DoCursorSave, 'INIT')
        self.state.add_transition('8', 'ESC', DoCursorRestore, 'INIT')
        self.state.add_transition('M', 'ESC', DoUpReverse, 'INIT')
        self.state.add_transition('>', 'ESC', DoUpReverse, 'INIT')
        self.state.add_transition('<', 'ESC', DoUpReverse, 'INIT')
        self.state.add_transition('=', 'ESC', None, 'INIT')
        self.state.add_transition('#', 'ESC', None, 'GRAPHICS_POUND')
        self.state.add_transition_any('GRAPHICS_POUND', None, 'INIT')
        self.state.add_transition('[', 'ESC', None, 'ELB')
        self.state.add_transition('H', 'ELB', DoHomeOrigin, 'INIT')
        self.state.add_transition('D', 'ELB', DoBackOne, 'INIT')
        self.state.add_transition('B', 'ELB', DoDownOne, 'INIT')
        self.state.add_transition('C', 'ELB', DoForwardOne, 'INIT')
        self.state.add_transition('A', 'ELB', DoUpOne, 'INIT')
        self.state.add_transition('J', 'ELB', DoEraseDown, 'INIT')
        self.state.add_transition('K', 'ELB', DoEraseEndOfLine, 'INIT')
        self.state.add_transition('r', 'ELB', DoEnableScroll, 'INIT')
        self.state.add_transition('m', 'ELB', None, 'INIT')
        self.state.add_transition('?', 'ELB', None, 'MODECRAP')
        self.state.add_transition_list(string.digits, 'ELB', DoStartNumber, 'NUMBER_1')
        self.state.add_transition_list(string.digits, 'NUMBER_1', DoBuildNumber, 'NUMBER_1')
        self.state.add_transition('D', 'NUMBER_1', DoBack, 'INIT')
        self.state.add_transition('B', 'NUMBER_1', DoDown, 'INIT')
        self.state.add_transition('C', 'NUMBER_1', DoForward, 'INIT')
        self.state.add_transition('A', 'NUMBER_1', DoUp, 'INIT')
        self.state.add_transition('J', 'NUMBER_1', DoErase, 'INIT')
        self.state.add_transition('K', 'NUMBER_1', DoEraseLine, 'INIT')
        self.state.add_transition('l', 'NUMBER_1', DoMode, 'INIT')
        self.state.add_transition('m', 'NUMBER_1', None, 'INIT')
        self.state.add_transition('q', 'NUMBER_1', None, 'INIT')
        self.state.add_transition_list(string.digits, 'MODECRAP', DoStartNumber, 'MODECRAP_NUM')
        self.state.add_transition_list(string.digits, 'MODECRAP_NUM', DoBuildNumber, 'MODECRAP_NUM')
        self.state.add_transition('l', 'MODECRAP_NUM', None, 'INIT')
        self.state.add_transition('h', 'MODECRAP_NUM', None, 'INIT')
        self.state.add_transition(';', 'NUMBER_1', None, 'SEMICOLON')
        self.state.add_transition_any('SEMICOLON', DoLog, 'INIT')
        self.state.add_transition_list(string.digits, 'SEMICOLON', DoStartNumber, 'NUMBER_2')
        self.state.add_transition_list(string.digits, 'NUMBER_2', DoBuildNumber, 'NUMBER_2')
        self.state.add_transition_any('NUMBER_2', DoLog, 'INIT')
        self.state.add_transition('H', 'NUMBER_2', DoHome, 'INIT')
        self.state.add_transition('f', 'NUMBER_2', DoHome, 'INIT')
        self.state.add_transition('r', 'NUMBER_2', DoScrollRegion, 'INIT')
        self.state.add_transition('m', 'NUMBER_2', None, 'INIT')
        self.state.add_transition('q', 'NUMBER_2', None, 'INIT')
        self.state.add_transition(';', 'NUMBER_2', None, 'SEMICOLON_X')
        self.state.add_transition_any('SEMICOLON_X', DoLog, 'INIT')
        self.state.add_transition_list(string.digits, 'SEMICOLON_X', None, 'NUMBER_X')
        self.state.add_transition_any('NUMBER_X', DoLog, 'INIT')
        self.state.add_transition('m', 'NUMBER_X', None, 'INIT')
        self.state.add_transition('q', 'NUMBER_X', None, 'INIT')
        self.state.add_transition(';', 'NUMBER_2', None, 'SEMICOLON_X')
        return

    def process(self, c):
        self.state.process(c)

    def process_list(self, l):
        self.write(l)

    def write(self, s):
        for c in s:
            self.process(c)

    def flush(self):
        pass

    def write_ch(self, ch):
        """This puts a character at the current cursor position. The cursor
        position is moved forward with wrap-around, but no scrolling is done if
        the cursor hits the lower-right corner of the screen. """
        ch = ch[0]
        if ch == '\r':
            self.cr()
            return
        if ch == '\n':
            self.crlf()
            return
        if ch == chr(screen.BS):
            self.cursor_back()
            return
        if ch not in string.printable:
            fout = open('log', 'a')
            fout.write('Nonprint: ' + str(ord(ch)) + '\n')
            fout.close()
            return
        self.put_abs(self.cur_r, self.cur_c, ch)
        old_r = self.cur_r
        old_c = self.cur_c
        self.cursor_forward()
        if old_c == self.cur_c:
            self.cursor_down()
            if old_r != self.cur_r:
                self.cursor_home(self.cur_r, 1)
            else:
                self.scroll_up()
                self.cursor_home(self.cur_r, 1)
                self.erase_line()