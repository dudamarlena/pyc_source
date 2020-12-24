# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/line.py
# Compiled at: 2013-03-24 02:33:10
import inspect, os, re
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..')
Mclifns = import_relative('clifns', '.....pydbgr')
Mmisc = import_relative('misc', '.....pydbgr')
Mfile = import_relative('lib.file', '.....pydbgr')

def find_function(funcname, filename):
    cre = re.compile('def\\s+%s\\s*[(]' % re.escape(funcname))
    try:
        fp = open(filename)
    except IOError:
        return

    lineno = 1
    answer = None
    while True:
        line = fp.readline()
        if line == '':
            break
        if cre.match(line):
            answer = (
             funcname, filename, lineno)
            break
        lineno = lineno + 1

    fp.close()
    return answer


class InfoLine(Mbase_subcmd.DebuggerSubcommand):
    """Show information about the current line"""
    __module__ = __name__
    min_abbrev = 2
    need_stack = True
    short_help = 'Show current-line information'

    def lineinfo(self, identifier):
        failed = (None, None, None)
        idstring = identifier.split("'")
        if len(idstring) == 1:
            ident = idstring[0].strip()
        elif len(idstring) == 3:
            ident = idstring[1].strip()
        else:
            return failed
        if ident == '':
            return failed
        parts = ident.split('.')
        if parts[0] == 'self':
            del parts[0]
            if len(parts) == 0:
                return failed
        fname = self.proc.defaultFile()
        if len(parts) == 1:
            item = parts[0]
        else:
            (m, f) = file.lookupmodule(('.').join(parts[1:]), self.debugger.mainpyfile, self.core.canonic)
            if f:
                fname = f
            item = parts[(-1)]
        answer = find_function(item, fname)
        return answer or failed

    def run(self, args):
        """Current line number in source file"""
        if not self.proc.curframe:
            self.errmsg('No line number information available.')
            return
        if len(args) == 3:
            answer = self.lineinfo(args[2])
            if answer[0]:
                (item, filename, lineno) = answer
                if not os.path.isfile(filename):
                    filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
                self.msg('Line %s of "%s" <%s>' % (lineno, filename, item))
            return
        filename = self.core.canonic_filename(self.proc.curframe)
        if not os.path.isfile(filename):
            filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
        filename = self.core.canonic_filename(self.proc.curframe)
        msg1 = 'Line %d of "%s"' % (inspect.getlineno(self.proc.curframe), self.core.filename(filename))
        msg2 = 'at instruction %d' % self.proc.curframe.f_lasti
        if self.proc.event:
            msg2 += ', %s event' % self.proc.event
        self.msg(Mmisc.wrapped_lines(msg1, msg2, self.settings['width']))
        return False


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    d = Mdebugger.Debugger()
    (d, cp) = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoLine(i)
    sub.run([])
    cp.curframe = inspect.currentframe()
    for width in (80, 200):
        sub.settings['width'] = width
        sub.run(['file.py', 'lines'])