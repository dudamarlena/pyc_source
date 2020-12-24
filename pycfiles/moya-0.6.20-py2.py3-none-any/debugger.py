# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/debugger.py
# Compiled at: 2015-10-22 13:02:41
from __future__ import unicode_literals
from __future__ import absolute_import
import sys
from cmd import Cmd
try:
    import readline
    readline
except ImportError:
    pass

from .console import Cell
from .elements.help import help
from . import namespaces
from .tools import extract_namespace
from .compat import text_type

def winpdb():
    import rpdb2
    rpdb2.start_embedded_debugger(b'password')


_previous_command = None

class MoyaCmdDebugger(Cmd):
    prompt = b'moya>'
    command_help = [
     (' let foo="bar"', '\n            Set foo to "bar" in the context.\n            '),
     (' foo', '\n            Evaulate the \'foo\' in the current context and display the result. Any valid expression will also work, for example 1 + 1, "Hello," + "World!" etc.\n            '),
     (' foo?', "\n            Convert the value of 'foo' to text.\n\n            "),
     (' foo??', "\n            Convert the value of 'foo' to a Moya expression (if possible).\n\n            "),
     (' foo???', "\n            Covert the value of 'foo' to the internal (Python) representation.\n            "),
     (' $$', '\n            Show the current scope\n            '),
     ('t, stack [EXTRALINES]', '\n            Show the current call stack. If EXTRALINES is provided, it should be an integer indicating the number of lines of code to show in the stack trace.\n            '),
     ('s, step', '\n            Advance to next logic element.\n            '),
     ('o, over', '\n            Step over the next logic element.\n            '),
     ('u, out', '\n            Step out of the current call.\n            '),
     ('c, continue', '\n            Run until the next breakpoint, or to the end of the logic code.\n\n            '),
     ('help', '\n            Show this help information.\n            '),
     ('help TAG', '\n            Show help information for a given tag.\n            '),
     ('w, where [EXTRALINES]', '\n            Show the current position in moya code, if EXTRALINES it provided, it should be an integer indicating the number of additional lines either side of the current position to display.\n            '),
     ('watch', '\n            When followed by an expression, it will be added to the watch list (a table of expressions and their results). When given without an argument, the watch list will be reset.\n            '),
     ('winpdb PASSWORD', '\n            Launch WinPDB to debug the next Python call.\n            '),
     ('ctrl+D', '\n            Exit debugger and continue with moya code execution. Ignores all further breakpoints to the end of the request.\n\n            '),
     ('<ENTER>', '\n            Repeat last command.\n            '),
     ('v, view', '\n            Display the full view of the currently executing moya code.\n\n            '),
     ('e, eval', '\n            Evaluates an expression, or shows the current frame if no argument is given.\n            '),
     ('exit', 'Stop execution of Moya code and exit debugger.'),
     ('r, run', 'Exit debugger and continue with moya code execution. Ignores all further breakpoints in the session.')]

    def __init__(self, archive, console):
        self.console = console
        self.archive = archive
        Cmd.__init__(self)

    def default(self, line):
        global _previous_command
        if not isinstance(line, text_type):
            line = line.decode(sys.stdin.encoding)
        self.usercmd = line
        _previous_command = line

    def postcmd(self, stop, line):
        if stop is False:
            return False
        else:
            if _previous_command is None:
                return self.do_help()
            self.usercmd = _previous_command
            return True

    def do_help(self, line=b''):
        if line:
            ns, tag = extract_namespace(line)
            self.console.div(b'Help on <%s/>' % tag, fg=b'blue', bold=True)
            help(self.archive, self.console, b'{%s}%s' % (ns or namespaces.default, tag))
            return False
        self.console.div(b'Moya Debugger', fg=b'blue', bold=True)
        self.console.text(b"Moya's Debugger http://www.moyaproject.com/debugger/", fg=b'black', bold=True).nl()
        table = [(Cell(b'Command', bold=True), Cell(b'Description', bold=True))]
        command_help = sorted(self.command_help, key=lambda h: h[0])

        def format_desc(desc):
            lines = [ l.strip() for l in desc.splitlines() if l.strip() ]
            return (b'\n').join(lines)

        for i, (command, desc) in enumerate(command_help):
            table.append([Cell(command, bold=True, fg=b'green'),
             Cell(format_desc(desc))])

        self.console.table(table, header=True)
        return False