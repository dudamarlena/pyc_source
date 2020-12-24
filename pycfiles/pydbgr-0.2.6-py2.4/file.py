# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/file.py
# Compiled at: 2013-03-17 09:26:42
import columnize, inspect, pyficache, sys
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mmisc = import_relative('misc', '....', 'pydbgr')

class InfoFile(Mbase_subcmd.DebuggerSubcommand):
    """**info file** [*filename* [**all** | **lines** | **sha1** | **size**]]

Show information about the current file. If no filename is given and
the program is running then the current file associated with the
current stack entry is used. Sub options which can be shown about a file are:
  
 * **brkpts** Line numbers where there are statement boundaries. These
 lines can be used in breakpoint commands.

 * **sha1**     A SHA1 hash of the source text. This may be useful in comparing source code.

 * **size**     The number of lines in the file.
 
 * **all** All of the above information.
 """
    __module__ = __name__
    min_abbrev = 2
    need_stack = False
    short_help = 'Show information about an imported or loaded Python file'

    def run(self, args):
        """Get file information"""
        if len(args) == 0:
            if not self.proc.curframe:
                self.errmsg('No frame - no default file.')
                return False
            filename = self.proc.curframe.f_code.co_filename
        else:
            filename = args[0]
        m = filename + ' is'
        filename_cache = self.core.filename_cache
        if filename in filename_cache:
            m += ' cached in debugger'
            if filename_cache[filename] != filename:
                m += ' as:'
                m = Mmisc.wrapped_lines(m, filename_cache[filename] + '.', self.settings['width'])
            else:
                m += '.'
            self.msg(m)
        else:
            self.msg(m + ' not cached in debugger.')
        canonic_name = self.core.canonic(filename)
        self.msg(Mmisc.wrapped_lines('Canonic name:', canonic_name, self.settings['width']))
        for name in (canonic_name, filename):
            if name in sys.modules:
                for key in [ k for (k, v) in list(sys.modules.items()) if name == v ]:
                    self.msg('module: %s', key)

        for arg in args[1:]:
            processed_arg = False
            if arg in ['all', 'size']:
                if pyficache.size(canonic_name):
                    self.msg('File has %d lines.' % pyficache.size(canonic_name))
                processed_arg = True
            if arg in ['all', 'sha1']:
                self.msg('SHA1 is %s.' % pyficache.sha1(canonic_name))
                processed_arg = True
            if arg in ['all', 'brkpts']:
                lines = pyficache.trace_line_numbers(canonic_name)
                self.section('Possible breakpoint line numbers:')
                fmt_lines = columnize.columnize(lines, ljust=False, arrange_vertical=False, lineprefix='  ')
                self.msg(fmt_lines)
                processed_arg = True
            if not processed_arg:
                self.errmsg("Don't understand sub-option %s." % arg)


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoFile(i)
    sub.run([])
    cp.curframe = inspect.currentframe()
    sub.run(['file.py', 'foo'])
    for width in (200, 80):
        sub.settings['width'] = width
        sub.run(['file.py', 'lines'])
        print sub.run([])

    sub.run(['file.py', 'all'])