# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/opt/.virtualenvs/djangoplus/lib/python3.7/site-packages/djangoplus/tools/editor.py
# Compiled at: 2018-09-05 08:12:08
# Size of source mod 2**32: 7281 bytes
import random, curses, time
from time import sleep
from djangoplus.tools.subtitle import Subtitle

class EditorSimulator(object):
    COMMENT_MARKUP = '{}{} '.format('#', ':')

    def __init__(self, file_path=None, slow=True):
        self.screen = None
        self.height = 0
        self.width = 0
        self.top = []
        self.center = []
        self.bottom = []
        self.steps = {}
        self.slow = slow
        if file_path:
            self.lines = open(file_path).readlines()
        else:
            self.lines = []
        self.initialize_curses()

    def initialize_curses(self):
        self.screen = curses.initscr()
        self.height, self.width = self.screen.getmaxyx()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.curs_set(0)
        self.top = []
        self.center = []
        self.bottom = []
        self.steps = {}

    def proccess_lines(self, start_step=None, end_step=None):
        i = 0
        for j, line in enumerate(self.lines):
            tokens = line.split(EditorSimulator.COMMENT_MARKUP)
            if len(tokens) > 1:
                step_number = float(tokens[1].strip().split()[0])
                if j:
                    self.lines[j - 1] = self.lines[(j - 1)].strip() or '{}{}{}'.format(self.lines[(j - 1)], EditorSimulator.COMMENT_MARKUP, step_number)

        for j, text in enumerate(self.lines):
            j += 1
            tokens = text.split(EditorSimulator.COMMENT_MARKUP)
            text = tokens[0].rstrip()
            if len(tokens) > 1:
                step = tokens[1].strip()
                step_number = float(step.split()[0])
                step_message = ' '.join(step.split()[1:]).strip()
                if start_step:
                    if step_number < start_step:
                        step_number = None
                        step_message = ''
                    else:
                        step_number = None
                        step_message = ''
                if step_number is None:
                    if i < self.height - 1:
                        self.center.append(text)
                        self.screen.addstr(i, 0, text[0:self.width - 1])
                        i += 1
                    else:
                        self.bottom.append(text)
            else:
                if step_number not in self.steps:
                    self.steps[step_number] = []
                for line in self.lines[:j]:
                    tokens = line.replace('\n', '').split(EditorSimulator.COMMENT_MARKUP)
                    if len(tokens) > 1 and float(tokens[1].strip().split()[0]) > step_number:
                        j -= 1

                self.steps[step_number].append([text, j, step_message])

        self.screen.refresh()

    def simulate(self, start_step=None, end_step=None, pause=False):
        if not self.screen:
            self.initialize_curses()
        self.proccess_lines(start_step, end_step)
        for step in sorted(self.steps.keys()):
            if end_step is not None:
                if step > float(end_step):
                    break
            for text, i, message in self.steps[step]:
                if message:
                    Subtitle.display(message, self.slow and 3 or 1)
                self.write(text, i)

        self.close(validate=(end_step is None), pause=pause)

    def scroll(self, i):
        time.sleep(random.random() * 10.0 / (self.slow and 400 or 50))
        first_visible_line = len(self.top)
        if i > first_visible_line:
            for j in range(first_visible_line, i):
                text = self.center.pop(0)
                self.top.append(text)
                self.screen.move(0, 0)
                self.screen.deleteln()
                if self.bottom:
                    text = self.bottom.pop(0)
                    self.center.append(text)
                    self.screen.addstr(len(self.center) - 1, 0, text)
                self.screen.refresh()
                time.sleep(0.1)

        else:
            if i < first_visible_line:
                self.screen.move(0, 0)
                for j in range(i, first_visible_line):
                    if self.top:
                        text = self.top.pop()
                        self.center.insert(0, text)
                        self.screen.insertln()
                        self.screen.addstr(0, 0, text)
                        if len(self.center) > self.height - 1:
                            text = self.center.pop()
                            self.bottom.insert(0, text)
                        self.screen.refresh()
                        time.sleep(0.1)

            self.screen.refresh()

    def write(self, text, i, start=0):
        middle = int(self.height / 2)
        if len(self.center) > middle and i > middle:
            shift = middle
            self.scroll(i - shift - 1)
        else:
            shift = i - 1
            self.scroll(i - shift - 1)
        self.screen.move(0 + shift, 0)
        curses.setsyx(0 + shift, 0)
        if start:
            self.center[0] = '{}{}{}'.format(self.center[0][:start], text, self.center[0][start:])
        else:
            self.screen.insdelln(1)
            self.center.insert(0 + shift, text)
            if len(self.center) == self.height:
                self.bottom.insert(0, self.center.pop())
        for j, c in enumerate(text):
            if j > 0:
                curses.curs_set(1)
            elif start:
                self.screen.insstr(0 + shift, start + j, c, curses.color_pair(1))
            else:
                self.screen.addstr(0 + shift, j, c, curses.color_pair(1))
            time.sleep(random.random() * 10.0 / (self.slow and 50 or 400))
            self.screen.refresh()
            curses.curs_set(0)

    def save(self, file_path):
        tmp = open(file_path, 'w')
        tmp.write(self.get_content())
        tmp.flush()
        tmp.close()

    def get_content(self):
        l = list()
        if self.top:
            l.append('\n'.join(self.top))
            l.append('\n')
        l.append('\n'.join(self.center))
        if self.bottom:
            l.append('\n')
            l.append('\n'.join(self.bottom))
        return ''.join(l)

    def validate(self):
        l = list()
        for line in self.lines:
            l.append(line.split(EditorSimulator.COMMENT_MARKUP)[0].rstrip())

        original_content = '\n'.join(l)
        content = self.get_content()
        if not original_content == content:
            open('/tmp/output0.txt', 'w').write(original_content)
            open('/tmp/output1.txt', 'w').write(content)
            raise Exception('Output content does not mach original content!!!')

    def close(self, pause=False, validate=False):
        if pause:
            self.screen.getch()
        if validate:
            self.validate()
        if self.screen:
            self.screen.clear()
            curses.endwin()
            sleep(1)
        self.screen = None