# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/breakpoint.py
# Compiled at: 2017-09-29 16:00:08
"""Breakpoints as used in a debugger.

This code is a rewrite of the stock python bdb.Breakpoint"""
__all__ = [
 'BreakpointManager', 'Breakpoint']
import os.path

class BreakpointManager:
    """Manages the list of Breakpoints.

    Breakpoints are indexed by number in the `bpbynumber' list, and
    through a (file,line) tuple which is a key in the `bplist'
    dictionary. If the breakpoint is a function it is in `fnlist' as
    well.  Note there may be more than one breakpoint per line which
    may have different conditions associated with them.
    """
    __module__ = __name__

    def __init__(self):
        self.reset()

    def bpnumbers(self):
        """Returns a list of strings of breakpoint numbers"""
        return [ '%d' % bp.number for bp in self.bpbynumber if bp is not None ]

    def get_breakpoint(self, i):
        if isinstance(i, str):
            try:
                i = int(i)
            except ValueError:
                return (
                 False, 'Breakpoint value %r is not a number.' % i, None)

        if 1 == len(self.bpbynumber):
            return (
             False, 'No breakpoints set.', None)
        elif i >= len(self.bpbynumber) or i <= 0:
            return (
             False, 'Breakpoint number %d out of range 1..%d.' % (i, len(self.bpbynumber) - 1), None)
        bp = self.bpbynumber[i]
        if bp is None:
            return (
             False, 'Breakpoint %d previously deleted.' % i, None)
        return (
         True, None, bp)

    def add_breakpoint(self, filename, lineno, temporary=False, condition=None, func=None):
        bpnum = len(self.bpbynumber)
        if filename:
            filename = os.path.realpath(filename)
        brkpt = Breakpoint(bpnum, filename, lineno, temporary, condition, func)
        self.bpbynumber.append(brkpt)
        if (filename, lineno) in self.bplist:
            self.bplist[(filename, lineno)].append(brkpt)
        else:
            self.bplist[(filename, lineno)] = [
             brkpt]
        if func:
            if func in self.fnlist:
                self.fnlist[func].append(brkpt)
            else:
                self.fnlist[func] = [
                 brkpt]
        return brkpt

    def delete_all_breakpoints(self):
        bp_list = []
        for bp in self.bpbynumber:
            if bp:
                bp_list.append(str(bp.number))
                self.delete_breakpoint(bp)

        if not bp_list:
            return 'There are no breakpoints'
        else:
            return 'Deleted breakpoints %s' % (', ').join(bp_list)

    def delete_breakpoint(self, bp):
        """ remove breakpoint `bp'"""
        bpnum = bp.number
        self.bpbynumber[bpnum] = None
        index = (bp.filename, bp.line)
        if index not in self.bplist:
            return False
        self.bplist[index].remove(bp)
        if not self.bplist[index]:
            del self.bplist[index]
        return True

    def delete_breakpoint_by_number(self, bpnum):
        """Remove a breakpoint given its breakpoint number."""
        (success, msg, bp) = self.get_breakpoint(bpnum)
        if not success:
            return (
             False, msg)
        self.delete_breakpoint(bp)
        return (True, '')

    def en_disable_all_breakpoints(self, do_enable=True):
        """Enable or disable all breakpoints."""
        bp_list = [ bp for bp in self.bpbynumber if bp ]
        bp_nums = []
        if do_enable:
            endis = 'en'
        else:
            endis = 'dis'
        if not bp_list:
            return 'No breakpoints to %sable' % endis
        for bp in bp_list:
            bp.enabled = do_enable
            bp_nums.append(str(bp.number))

        return 'Breakpoints %sabled: %s' % (endis, (', ').join(bp_nums))

    def en_disable_breakpoint_by_number(self, bpnum, do_enable=True):
        """Enable or disable a breakpoint given its breakpoint number."""
        (success, msg, bp) = self.get_breakpoint(bpnum)
        if not success:
            return (
             success, msg)
        if do_enable:
            endis = 'en'
        else:
            endis = 'dis'
        if bp.enabled == do_enable:
            return (
             False, 'Breakpoint (%r) previously %sabled' % (str(bpnum), endis))
        bp.enabled = do_enable
        return (True, '')

    def delete_breakpoints_by_lineno(self, filename, lineno):
        """Removes all breakpoints at a give filename and line number.
        Returns a list of breakpoints numbers deleted.
        """
        if (
         filename, lineno) not in self.bplist:
            return []
        breakpoints = self.bplist[(filename, lineno)]
        bpnums = [ bp.number for bp in breakpoints ]
        for bp in list(breakpoints):
            self.delete_breakpoint(bp)

        return bpnums

    def find_bp(self, filename, lineno, frame):
        """Determine which breakpoint for this file:line is to be acted upon.

        Called only if we know there is a bpt at this
        location.  Returns breakpoint that was triggered and a flag
        that indicates if it is ok to delete a temporary breakpoint.

        """
        possibles = self.bplist[(filename, lineno)]
        for i in range(0, len(possibles)):
            b = possibles[i]
            if not b.enabled:
                continue
            if not checkfuncname(b, frame):
                continue
            b.hits += 1
            if not b.condition:
                if b.ignore > 0:
                    b.ignore = b.ignore - 1
                    continue
                else:
                    return (b, True)
            else:
                try:
                    val = eval(b.condition, frame.f_globals, frame.f_locals)
                    if val:
                        if b.ignore > 0:
                            b.ignore = b.ignore - 1
                        else:
                            return (
                             b, True)
                except:
                    return (
                     b, False)

        return (None, None)

    def last(self):
        return len(self.bpbynumber) - 1

    def reset(self):
        """ A list of breakpoints by breakpoint number.  Each entry is
        None or an instance of Breakpoint.  Index 0 is unused, except
        for marking an effective break .... see effective(). """
        self.bpbynumber = [
         None]
        self.bplist = {}
        self.fnlist = {}
        return


class Breakpoint:
    """Breakpoint class implements temporary breakpoints, ignore
    counts, disabling and (re)-enabling breakpoints and breakpoint
    conditionals.
    """
    __module__ = __name__

    def __init__(self, number, filename, line, temporary=False, condition=None, funcname=None):
        self.condition = condition
        self.enabled = True
        self.filename = filename
        if filename:
            self.filename = os.path.realpath(filename)
        self.func_first_executable_line = None
        self.funcname = funcname
        self.hits = 0
        self.ignore = 0
        self.line = line
        self.number = number
        self.temporary = temporary
        return

    def __str__(self):
        if self.temporary:
            disp = 'del  '
        else:
            disp = 'keep '
        if self.enabled:
            disp = disp + 'yes  '
        else:
            disp = disp + 'no   '
        msg = '%-4dbreakpoint   %s at %s:%d' % (self.number, disp, self.filename, self.line)
        if self.condition:
            msg += '\n\tstop only if %s' % self.condition
        if self.ignore:
            msg += msg('\n\tignore next %d hits' % self.ignore)
        if self.hits:
            if self.hits > 1:
                ss = 's'
            else:
                ss = ''
            msg += ('\n\tbreakpoint already hit %d time%s' % self.hits, ss)
        return msg

    def enable(self):
        self.enabled = True
        return self.enabled

    def disable(self):
        self.enabled = False
        return self.enabled

    def icon_char(self):
        """Return a one-character "icon" giving the state of the breakpoint
        't': temporary breakpoint
        'B': enabled breakpoint
        'b': disabled breakpoint
        """
        if self.temporary:
            return 't'
        elif self.enabled:
            return 'B'
        else:
            return 'b'


def checkfuncname(b, frame):
    """Check whether we should break here because of `b.funcname`."""
    if not b.funcname:
        if b.line != frame.f_lineno:
            return False
        return True
    if frame.f_code.co_name != b.funcname:
        return False
    if not b.func_first_executable_line:
        b.func_first_executable_line = frame.f_lineno
    if b.func_first_executable_line != frame.f_lineno:
        return False
    return True


if __name__ == '__main__':
    bpmgr = BreakpointManager()
    print bpmgr.last()
    bp = bpmgr.add_breakpoint('foo', 5)
    print bp.icon_char()
    print bpmgr.last()
    print repr(bp)
    print str(bp)
    bp.disable()
    print str(bp)
    for i in (10, 1):
        (status, msg) = bpmgr.delete_breakpoint_by_number(i)
        print 'Delete breakpoint %s: %s %s' % (i, status, msg)

    import inspect
    frame = inspect.currentframe()
    print 'Stop at bp: %s' % checkfuncname(bp, frame)

    def foo(bp, bpmgr):
        frame = inspect.currentframe()
        print 'Stop at bp2: %s' % checkfuncname(bp, frame)
        bp3 = bpmgr.add_breakpoint('foo', frame.f_lineno + 1)
        print 'Stop at bp3: %s' % checkfuncname(bp3, frame)


    bp2 = bpmgr.add_breakpoint(None, None, False, None, 'foo')
    foo(bp2, bpmgr)
    bp3 = bpmgr.add_breakpoint('foo', 5, temporary=True)
    print bp3.icon_char()
    print bpmgr.bpnumbers()
    bp = bpmgr.add_breakpoint('bar', 3)
    filename = bp.filename
    for i in range(3):
        bp = bpmgr.add_breakpoint('bar', 6)

    print bpmgr.delete_breakpoints_by_lineno(filename, 6)
    print bpmgr.delete_breakpoints_by_lineno(filename, 6)
    print bpmgr.bpnumbers()