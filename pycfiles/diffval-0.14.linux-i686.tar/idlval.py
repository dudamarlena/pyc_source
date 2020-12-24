# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/diffval/idlval.py
# Compiled at: 2010-10-25 18:32:39
import session, test, os, sys
test_start_line = '### idlval testing begins ###'
test_end_line = '### idlval testing ends ###'
mem_start_line = '### idlval mem check begins ###'
mem_end_line = '### idlval mem check ends ###'
halting_line = '% Execution halted at: '
not_a_test_line = "% Attempt to call undefined procedure/function: 'TEST'."

def match(first, second, exact=True):
    if exact:
        if first == second:
            return True
    elif second.startswith(first):
        return True
    return False


def index(line, array, exact=True):
    if sys.hexversion >= 33947648:
        return next((i for i in xrange(len(array)) if match(line, array[i], exact)), None)
    else:
        for i in xrange(len(array)):
            if match(line, array[i], exact):
                return i

        return
        return


class idlsession(session.session):

    def __init__(self, test, include=[], log=None):
        self._args = [
         '-IDL_PATH', '"+' + (':').join(include) + '<IDL_DEFAULT>"',
         '-IDL_MORE', 'False', '-quiet']
        self._input = [
         'PRINTF, -2, "' + test_start_line + '"',
         '.COMPILE ' + test,
         'test',
         'PRINTF, -2, "' + test_end_line + '"',
         'PRINTF, -2, "' + mem_start_line + '"',
         'HELP, OUTPUT = idlval_mem_check, /HEAP',
         'PRINTF, -2, idlval_mem_check',
         'PRINTF, -2, "' + mem_end_line + '"',
         'exit']
        exe = 'idl'
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            exe += 'de'
        session.session.__init__(self, executable=exe, log=log)


class idltest(test.test):

    def __init__(self, *args, **kwargs):
        test.test.__init__(self, *args, **kwargs)
        self._expects['memcheck'] = [
         'Heap Variables:     # Pointer: 0     # Object : 0']
        self._results['memcheck'] = []
        self._expects['halting'] = []
        self._results['halting'] = []

    def _create(self):
        return idlsession(test=self._path, include=self._include, log=self._log)

    def _checksuccess(self):
        if index(not_a_test_line, self._results['stderr']):
            return
        else:
            start = index(mem_start_line, self._results['stderr'])
            end = index(mem_end_line, self._results['stderr'])
            if start != None:
                if end != None:
                    self._results['memcheck'] = self._results['stderr'][start + 1:end]
                    self._results['stderr'] = self._results['stderr'][0:start - 1] + self._results['stderr'][end + 1:]
                else:
                    self._results['memcheck'] = self._results['stderr'][start + 1:] + [
                     '### Session did not terminate ###']
                    self._results['stderr'] = self._results['stderr'][0:start - 1]
            else:
                self._results['memcheck'] = [
                 '### Session did not terminate ###']
            start = index(test_start_line, self._results['stderr'])
            end = index(test_end_line, self._results['stderr'])
            if start != None:
                if end != None:
                    self._results['stderr'] = self._results['stderr'][0:start - 1] + self._results['stderr'][start + 1:end - 1] + self._results['stderr'][end + 1:]
                else:
                    self._results['stderr'] = self._results['stderr'][0:start - 1] + self._results['stderr'][start + 1:] + ['### Session did not terminate ###']
            else:
                self._results['stderr'] = self._results['stderr'] + [
                 '### Session did not run ###']
                if 'stderr' not in self._expects:
                    self._expects['stderr'] = []
            start = index(halting_line, self._results['stderr'], exact=False)
            if start:
                self._results['halting'] = [
                 self._results['stderr'][start]]
                if 'stderr' not in self._expects:
                    self._expects['stderr'] = []
            else:
                self._results['halting'] = []
            if 'stdout' in self._results:
                if self._results['stdout'] == []:
                    self._results['stdout'] += ['']
            if 'stdout' in self._expects:
                self._expects['stdout'] += ['']
            return test.test._checksuccess(self)