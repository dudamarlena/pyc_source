# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_functest/formatter.py
# Compiled at: 2011-01-13 01:48:00
import traceback
try:
    import pygments
    from pygments import highlight
    from pygments.lexers import PythonLexer, PythonTracebackLexer
    from pygments.formatters import TerminalFormatter
    from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token
    TERMINAL_COLORS = {Token: ('', ''), 
       Comment: ('lightgray', 'darkgray'), 
       Keyword: ('darkblue', 'turquoise'), 
       Keyword.Type: ('teal', 'blue'), 
       Operator.Word: ('purple', 'fuchsia'), 
       Name.Builtin: ('teal', 'turquoise'), 
       Name.Function: ('darkgreen', 'green'), 
       Name.Namespace: ('_teal_', '_turquoise_'), 
       Name.Class: ('_darkgreen_', '_green_'), 
       Name.Exception: ('teal', 'turquoise'), 
       Name.Decorator: ('darkgray', 'lightgray'), 
       Name.Variable: ('darkred', 'red'), 
       Name.Constant: ('darkred', 'red'), 
       Name.Attribute: ('teal', 'blue'), 
       Name.Tag: ('blue', 'turquoise'), 
       String: ('brown', 'brown'), 
       Number: ('darkblue', 'turquoise'), 
       Generic.Deleted: ('red', 'red'), 
       Generic.Inserted: ('darkgreen', 'green'), 
       Generic.Heading: ('**', '**'), 
       Generic.Subheading: ('*purple*', '*fuchsia*'), 
       Generic.Error: ('red', 'red'), 
       Error: ('_red_', '_red_')}
except ImportError:
    pygments = None

import global_settings
LINES_IN_TB = global_settings.LINES_IN_TB

def highlight_traceback(recent_traceback):
    if global_settings.bigtb is False:
        tb = traceback.format_exception(*recent_traceback)
        tb.pop(1)
        print highlight(('').join([ t.encode('ascii', 'ignore') for t in tb ]), PythonTracebackLexer(), TerminalFormatter(bg='dark', colorscheme=TERMINAL_COLORS))
        return
    else:
        tb = traceback.extract_tb(recent_traceback[(-1)])
        colored_traceback = 'Traceback:\n'
        for (filename, lineno, method_name, entry_name) in tb:
            if filename.find('functest') is -1:
                source_file_lines = open(filename, 'r').read().splitlines()
                colored_traceback += '  in %s at line %s in %s\n' % (method_name, lineno, filename)
                if lineno > LINES_IN_TB:
                    index_start = lineno - LINES_IN_TB
                else:
                    index_start = 0
                index_str_length = len(str(lineno))
                for i in range(LINES_IN_TB):
                    line = source_file_lines[(index_start + i)]
                    if len(str(index_start + i)) == index_str_length:
                        index_string = str(index_start + i + 1) + ' '
                    else:
                        index_string = '0' + str(index_start + i + 1) + ' '
                    if pygments is not None:
                        colored_traceback += index_string + highlight(line, PythonLexer(), TerminalFormatter(bg='dark', colorscheme=TERMINAL_COLORS))
                    else:
                        colored_traceback += index_string + line + '\n'

        print colored_traceback
        return