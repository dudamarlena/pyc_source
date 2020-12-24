# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Termcap.py
# Compiled at: 2011-10-05 18:50:45
"""Termcap utilities

$Id: Termcap.py,v 1.4 2011/10/05 22:50:45 csoftmgr Exp $"""
__version__ = '$Revision: 1.4 $'[11:-2]
import os, re, sys, Csys
from Csys.Edits import termcap2chars
_Count = 0

class _LineDict(object):

    def __init__(self, line):
        global _Count
        _Count += 1
        self.nmbr = _Count
        self.line = line

    def __cmp__(self, other):
        return cmp(self.nmbr, other.nmbr)


def _file2string(fname, wantarray=False, pattern=None):
    patterns = (
     (
      re.compile('\\\\\\n', re.DOTALL), ''),
     (
      re.compile(':\\t*:'), ':'))
    lines = {}
    if hasattr(fname, 'readlines'):
        fh = fname
    else:
        fh = open(fname)
    for line in fh:
        line = line.rstrip()
        if not line.startswith('#'):
            line = _LineDict(line)
            lines[line.nmbr] = line

    lines = lines.values()
    lines.sort()
    body = ('\n').join([ line.line for line in lines ])
    for pat, repl in patterns:
        body = pat.sub(repl, body)

    if wantarray or pattern:
        body = body.split('\n')
        if pattern:
            body = Csys.grep(pattern, body)
        return body
    return body


_termcapBodies = {}

class Termcap(Csys.CSClass):
    _attributes = {'term': os.environ.get('TERM', ''), 
       'termcap': os.environ.get('TERMCAP', '/etc/termcap')}
    _boolPattern = re.compile('^\\w\\w$')
    _numPattern = re.compile('^(\\w\\w)#(.*)')
    _strPattern = re.compile('^(\\w\\w)=(.*)')

    def __init__(self, term=None, termcap=None, expand=True):
        Csys.CSClass.__init__(self)
        if term:
            self.term = term
        if termcap:
            self.termcap = termcap
        cols = self.__dict__
        termcap = self.termcap
        if not os.path.isfile(termcap) and not re.compile('(^|\\|)%s[:\\|]' % self.term).search(termcap):
            termcap = '/etc/termcap'
        if os.path.isfile(termcap):
            termcaps = _termcapBodies.get(termcap)
            if not termcaps:
                termcaps = _file2string(termcap, wantarray=True)
                _termcapBodies[termcap] = termcaps
            pattern = '(^|\\|)%s[:\\|]' % self.term
            try:
                entries = Csys.grep(pattern, termcaps[:])
                self.entries = entries[0]
            except IndexError as e:
                self.entries = ''

        else:
            self.entries = termcap
        for field in [ f.strip() for f in self.entries.split(':') if f.strip() ]:
            if self._boolPattern.match(field):
                cols[field] = True
                continue
            R = self._numPattern.match(field)
            if R:
                cols[R.group(1)] = int(R.group(2))
                continue
            R = self._strPattern.match(field)
            if R:
                k, v = R.group(1), R.group(2)
                if expand:
                    v = termcap2chars(v)
                cols[k] = v.rstrip(':')

        if 'tc' in cols:
            tc = Termcap(term=self.tc, termcap=self.termcap, expand=expand)
            for field, value in tc.__dict__.items():
                if field not in cols:
                    cols[field] = value

        if 'pc' in cols and cols['pc'] == '':
            self.pc = '\x00'
        if 'bc' in cols and cols['bc'] == '':
            self.bc = '\x08'

    def __getattr__(self, name):
        """This is largely to provide default behavior for old
                perl programs which reference undefined attributes"""
        cols = self.__dict__
        name = name.lstrip('tc_')
        if name == 'init_string':
            name = 'is'
        return cols.get(name, '')


_termcapEntries = {}

def getTermcap(term=None, termcap=None, expand=True):
    """Get termcap entry and cache it"""
    key = repr((term, termcap, expand))
    tc = _termcapEntries.get(key) or Termcap(term, termcap, expand)
    _termcapEntries[key] = tc
    return tc


if __name__ == '__main__':
    print 'OK'
    termcap = Termcap(term='hp4mplus-dx', termcap='/csoft/etc/cssysvlp/termcap')
    print termcap.dumpAttrs()
    print '>%s<' % termcap.ti
    sys.exit(0)
    print termcap.ae
    body = _file2string('/csoft/etc/cssysvlp/termcap', wantarray=True, pattern='\\|nec860\\|')
    for line in body:
        print line
        print ''