# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/doctestpdbhacks/__init__.py
# Compiled at: 2008-09-26 08:56:27


def format_stack_entry(self, frame_lineno, lprefix=': '):
    import linecache, repr
    (frame, lineno) = frame_lineno
    filename = self.canonic(frame.f_code.co_filename)
    if filename.startswith('<doctest'):
        lineno = frame.f_back.f_locals['example'].lineno + frame.f_back.f_locals['test'].lineno + 1
        filename = frame.f_back.f_locals['test'].filename
        s = 'doctest @ %s(%r)' % (filename, lineno)
    else:
        s = '%s(%r)' % (filename, lineno)
    if frame.f_code.co_name:
        s = s + frame.f_code.co_name
    else:
        s = s + '<lambda>'
    if '__args__' in frame.f_locals:
        args = frame.f_locals['__args__']
    else:
        args = None
    if args:
        s = s + repr.repr(args)
    else:
        s = s + '()'
    if '__return__' in frame.f_locals:
        rv = frame.f_locals['__return__']
        s = s + '->'
        s = s + repr.repr(rv)
    line = linecache.getline(filename, lineno)
    if line:
        s = s + lprefix + line.strip()
    return s


import bdb
bdb.Bdb.format_stack_entry = format_stack_entry
import linecache

def do_list(self, arg):
    self.lastcmd = 'list'
    last = None
    filename = self.curframe.f_code.co_filename
    if filename.startswith('<doctest'):
        frame = self.curframe
        cur_lineno = frame.f_back.f_locals['example'].lineno + frame.f_back.f_locals['test'].lineno + 1
        filename = frame.f_back.f_locals['test'].filename
    else:
        cur_lineno = self.curframe.f_lineno
    if arg:
        try:
            x = eval(arg, {}, {})
            if type(x) == type(()):
                (first, last) = x
                first = int(first)
                last = int(last)
                if last < first:
                    last = first + last
            else:
                first = max(1, int(x) - 5)
        except:
            print '*** Error in argument:', repr(arg)
            return

    elif self.lineno is None:
        first = max(1, cur_lineno - 5)
    else:
        first = self.lineno + 1
    if last is None:
        last = first + 10
    breaklist = self.get_file_breaks(filename)
    try:
        for lineno in range(first, last + 1):
            line = linecache.getline(filename, lineno)
            if not line:
                print '[EOF]'
                break
            else:
                s = repr(lineno).rjust(3)
                if len(s) < 4:
                    s = s + ' '
                if lineno in breaklist:
                    s = s + 'B'
                else:
                    s = s + ' '
                if lineno == cur_lineno:
                    s = s + '->'
                print s + '\t' + line,
                self.lineno = lineno

    except KeyboardInterrupt:
        pass

    return


import pdb
pdb.Pdb.do_list = do_list
pdb.Pdb.do_l = do_list