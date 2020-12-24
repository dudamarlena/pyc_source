# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/tools/terminal.py
# Compiled at: 2018-10-12 04:37:05
# Size of source mod 2**32: 2022 bytes
import os, sys, time, random
from subprocess import Popen, PIPE
from django.utils import termcolors
TYPING_SPEED = 50

def simulate_command_type(commands, shell=False):
    for command in commands.split('&& '):
        if not command.startswith('source'):
            simulate_type(command, shell=shell)


def simulate_type(command, shell=False):
    sys.stdout.write('breno@localhost: ~$ ')
    for c in command:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / TYPING_SPEED)

    print('')


def bold(text):
    return termcolors.make_style(fg='black', opts=('bold', ))(text)


def info(text):
    return termcolors.make_style(fg='cyan')(text)


def error(text):
    return termcolors.make_style(fg='red', opts=('bold', ))(text)


class Terminal(object):

    def __init__(self, verbose=True, python='python'):
        self.proccess = None
        self.verbose = verbose
        self.python = python

    def execute(self, command, clear=True, base_dir=None):
        if clear:
            os.system('clear')
            simulate_type('', shell=True)
        else:
            if self.verbose:
                simulate_command_type(command, shell=True)
            if command.startswith('python'):
                command.replace('python', self.python)
            if base_dir:
                command = 'cd {} && {}'.format(base_dir, command)
            command = self.verbose or '{}  > /dev/null'.format(command)
        os.system(command)

    def show(self, visible=True):
        if os.path.exists('/usr/bin/osascript'):
            minimize_terminal_script = '\n                tell application "Terminal"\n                  set miniaturized of window 1 to {}\n                end tell\n            '.format(visible and 'false' or 'true')
            self.proccess = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            self.proccess.communicate(minimize_terminal_script.encode())

    def hide(self):
        self.show(False)