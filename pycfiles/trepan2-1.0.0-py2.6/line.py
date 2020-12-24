# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/line.py
# Compiled at: 2015-06-06 14:30:14
import inspect, os, re
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan import clifns as Mclifns, misc as Mmisc

def find_function(funcname, filename):
    cre = re.compile('def\\s+%s\\s*[(]' % re.escape(funcname))
    try:
        fp = open(filename)
    except IOError:
        return
    else:
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
    """**info line**

Show information about the current line

See also:
---------

`info program`, `info frame`"""
    min_abbrev = 2
    max_args = 0
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
        else:
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
                self.msg('Line %s of "%s" <%s>' % (
                 lineno, filename, item))
            return
        filename = self.core.canonic_filename(self.proc.curframe)
        if not os.path.isfile(filename):
            filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
        filename = self.core.canonic_filename(self.proc.curframe)
        msg1 = 'Line %d of "%s"' % (inspect.getlineno(self.proc.curframe),
         self.core.filename(filename))
        msg2 = 'at instruction %d' % self.proc.curframe.f_lasti
        if self.proc.event:
            msg2 += ', %s event' % self.proc.event
        self.msg(Mmisc.wrapped_lines(msg1, msg2, self.settings['width']))
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    (d, cp) = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoLine(i)
    sub.run([])
    cp.curframe = inspect.currentframe()
    for width in (80, 200):
        sub.settings['width'] = width
        sub.run(['file.py', 'lines'])