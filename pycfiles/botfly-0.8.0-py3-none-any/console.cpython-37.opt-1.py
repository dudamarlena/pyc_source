# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /botfly/console.py
# Compiled at: 2019-11-10 21:45:46
# Size of source mod 2**32: 3020 bytes
"""
Input/Output objects.
"""
__all__ = [
 'ConsoleIO']
import sys, os, prompt_toolkit

class ConsoleIO:
    __doc__ = 'Read and write standard I/O from one object.\n\n    Implicitly pages output if too many lines are printed (like *more*).\n    '

    def __init__(self, pagerprompt=None):
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.mode = 'w'
        self.stderr = sys.stderr.buffer
        self.closed = 0
        self.softspace = 0
        self._ps = prompt_toolkit.shortcuts.PromptSession()
        if self.stdout.isatty():
            self.set_size()
        else:
            self.columns, self.rows = (80, 24)
        self.write = self.stdout.write
        self.writelines = self.stdout.writelines
        self.read = self.stdin.read
        self.readline = self.stdin.readline
        self.readlines = self.stdin.readlines
        self.flush = self.stdout.flush

    def set_size(self):
        self.columns, self.rows = os.get_terminal_size()

    def _winch_handler(self, sig, st):
        self.set_size()

    def input(self, prompt='> ', completer=None):
        return self._ps.prompt(prompt, completer=completer)

    def print(self, *args, **kwargs):
        kwargs.pop('file', None)
        args = tuple([prompt_toolkit.ANSI(str(i)) for i in args])
        (prompt_toolkit.shortcuts.print_formatted_text)(args, **kwargs, **{'file': self.stdout})

    def close(self):
        if not self.closed:
            self.stdout = None
            self.stdin = None
            del self.read
            del self.readlines
            del self.write
            del self.flush
            del self.writelines
            del self._oldhandler
            self.closed = 1

    def fileno(self):
        return self.stdin.fileno()

    def isatty(self):
        return self.stdin.isatty() and self.stdout.isatty()

    def error(self, text):
        self.stderr.write(text.encode('latin1') + b'\n')
        self.stderr.flush()


if __name__ == '__main__':
    io = ConsoleIO()
    if io.isatty():
        io.write('hello, type something\n')
        io.flush()
        print(io.readline())
        io.print('Test print ', end='')
        io.error('An error.\n')
    lines = []
    for i in range(200):
        lines.append('{}. Now is the time for all good men...'.format(i))

    lines.append('\n')
    text = '\n'.join(lines)
    io.write(text)
    io.write('------\n')
    for i in range(200):
        io.write('{}. Now is the time to write lines...\n'.format(i))