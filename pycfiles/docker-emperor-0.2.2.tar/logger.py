# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/logger.py
# Compiled at: 2018-07-23 02:33:54
HEADER = '\x1b[40;223m'
BLUE = '\x1b[40;38;5;39m'
GREEN = '\x1b[40;92m'
YELLOW = '\x1b[40;93m'
ERROR = '\x1b[40;38;5;9m'
UNDERLINE = '\x1b[4m'
ORANGE = '\x1b[40;38;5;214m'
BOLD = '\x1b[1m'
END = '\x1b[0m'

class Logger:

    def __init__(self, root):
        self.root = root

    def cmd(self, *value):
        self.log(color=HEADER, *value)

    def success(self, *value):
        self.log(color=GREEN, *value)

    def choice(self, *value):
        self.log(color=BLUE, *value)

    def info(self, *value):
        self.log(color=HEADER, *value)

    def ask(self, *value):
        self.log(color=YELLOW, *value)

    def comment(self, *value):
        self.log(color=HEADER, *value)

    def warning(self, *value):
        self.log(color=ORANGE, *value)

    def error(self, *value):
        self.log(color=ERROR, *value)

    def log(self, *value, **kwargs):
        color = kwargs.pop('color', YELLOW)
        value = ' ' + (' ').join([ str(v) for v in value ]) + ' '
        value = ('{}>{}{}').format(color, value, END)
        value = value.replace('<b>', BOLD).replace('</b>', END + color)
        print value.strip()


def cmd(*value):
    log(color=HEADER, *value)


def success(*value):
    log(color=GREEN, *value)


def choice(*value):
    log(color=BLUE, *value)


def info(*value):
    log(color=HEADER, *value)


def ask(*value):
    log(color=YELLOW, *value)


def comment(*value):
    log(color=HEADER, *value)


def warning(*value):
    log(color=ORANGE, *value)


def error(*value):
    log(color=ERROR, *value)


def log(*value, **kwargs):
    color = kwargs.pop('color', YELLOW)
    value = ' ' + (' ').join([ str(v) for v in value ]) + ' '
    value = ('{}>{}{}').format(color, value, END)
    value = value.replace('<b>', BOLD).replace('</b>', END + color)
    print value.strip()