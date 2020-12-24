# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/files.py
# Compiled at: 2015-06-03 07:13:28
import columnize, inspect, pyficache, sys, os
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan import misc as Mmisc
from trepan.lib import complete as Mcomplete
from trepan.lib.file import file_list

class InfoFiles(Mbase_subcmd.DebuggerSubcommand):
    '**info files** [*filename* [**all** | **brkpts** | **lines** | **sha1** | **size**]]\n\nShow information about the current file. If no filename is given and\nthe program is running then the current file associated with the\ncurrent stack entry is used. Sub options which can be shown about a file are:\n\n * **brkpts** Line numbers where there are statement boundaries. These\n lines can be used in breakpoint commands.\n\n * **sha1**\tA SHA1 hash of the source text. ' + 'This may be useful in comparing source code.\n\n * **size**\tThe number of lines in the file.\n\n * **all** All of the above information.\n'
    min_abbrev = 2
    need_stack = False
    short_help = 'Show information about an imported or loaded Python file'

    def complete(self, prefix):
        completions = sorted(['.'] + file_list())
        return Mcomplete.complete_token(completions, prefix)

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
            matches = [ file for file in file_list() if file.endswith(filename)
                      ]
            if len(matches) > 1:
                self.msg('Multiple files found ending filename string:')
                for match_file in matches:
                    self.msg('\t%s' % match_file)

            elif len(matches) == 1:
                canonic_name = pyficache.unmap_file(matches[0])
                m += ' matched debugger cache file:\n  ' + canonic_name
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
            if arg in ('all', 'size'):
                if pyficache.size(canonic_name):
                    self.msg('File has %d lines.' % pyficache.size(canonic_name))
                processed_arg = True
            if arg in ('all', 'sha1'):
                self.msg('SHA1 is %s.' % pyficache.sha1(canonic_name))
                processed_arg = True
            if arg in ('all', 'brkpts'):
                lines = pyficache.trace_line_numbers(canonic_name)
                if lines:
                    self.section('Possible breakpoint line numbers:')
                    fmt_lines = columnize.columnize(lines, ljust=False, arrange_vertical=False, lineprefix='  ')
                    self.msg(fmt_lines)
                processed_arg = True
            if not processed_arg:
                self.errmsg("Don't understand sub-option %s." % arg)


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoFiles(i)
    sub.run([])
    cp.curframe = inspect.currentframe()
    sub.run(['file.py', 'foo'])
    for width in (200, 80):
        sub.settings['width'] = width
        sub.run(['file.py', 'lines'])
        print sub.run([])

    sub.run(['file.py', 'all'])
    print sub.complete('')