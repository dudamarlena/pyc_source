# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\formatter.py
# Compiled at: 2011-12-15 09:37:26


def nop(string, *args, **kwargs):
    return string


class ConsoleFormatter(object):

    def __init__(self, color=False):
        if color:
            import termcolor
            self.formatter = termcolor.colored
            import colorama
            colorama.init()
        else:
            self.formatter = nop

    def color_for(self, priority):
        colors = {'A': 'red', 
           'B': 'yellow', 
           'C': 'magenta', 
           'D': 'cyan', 
           'E': 'green'}
        if priority in colors:
            return colors[priority]
        return 'white'

    def format_todo(self, todo):
        return self.formatter(('{} {}').format(todo.id, todo.todo), self.color_for(todo.priority()))

    def format(self, model):
        shown = len(model)
        total = model.total()
        formatted = []
        for todo in model:
            formatted.append(self.format_todo(todo))

        suffix = '' if shown == 1 else 's'
        final = ('\n').join(formatted) + ('\n--\nTODO: {} of {} task{} shown\n').format(shown, total, suffix)
        return final.encode('utf-8')