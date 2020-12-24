# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/makemake.py
# Compiled at: 2009-09-17 18:52:54
"""This module is designed to build makefiles."""
import os, re, sys, tempfile, datetime, subprocess
from gmisclib import die
from gmisclib import avio
from gmisclib import fiatio
from gmisclib import gpkmisc
_debug = False
_log = None
makeflags = []
makefile = None
_makefd = None
_makeprog = ['make']
_did_header = False
DB_format = 'fiatio'

def maketemp(dir='/tmp', prefix='maketemp', suffix=''):
    global _makefd
    global makefile
    gpkmisc.makedirs(dir)
    handle, makefile = tempfile.mkstemp(dir=dir, prefix=prefix, suffix=suffix)
    _makefd = os.fdopen(handle, 'w')


def _write(*s):
    for x in s:
        _makefd.writelines([x, '\n'])


def _header():
    global _did_header
    if _did_header:
        return
    _write('# Makefile produced by gmisclib/makemake.py')
    _write('.SUFFIXES:', '')
    _write('.PHONY: all', '')
    _did_header = True


def setlog(f):
    global _log
    _log = open(f, 'a')


def log(*s):
    """Log some strings, one per line."""
    for x in s:
        _log.writelines([x, '\n'])

    _log.flush()


_qp = re.compile('[^a-zA-Z0-9_.+,/:-]')

def quote(s):

    def replf(x):
        return '\\%s' % x

    return re.sub(_qp, replf, s)


def var(k, v):
    """Pass a variable to make."""
    _header()
    _write('%s = %s' % (k, v))


def rule(a, *b):
    """Writes a rule into a makefile.   All lines except the
        first are indented.
        """
    _write('', a)
    _write(*[ '\t%s' % t for t in b ])
    _write('')


def blank():
    _header()
    _write('')


def set_debug():
    global _debug
    _debug = True


def finish():
    global _makeprog
    global makeflags
    _makefd.close()
    if _debug:
        tmp = open(makefile, 'r')
        sys.stdout.writelines(tmp.readlines())
    else:
        args = _makeprog + ['-f', makefile] + makeflags
        print '# calling', args
        rv = subprocess.call(args)
        os.remove(makefile)
        if rv != 0:
            die.info('CALL: %s' % (' ').join(args))
            die.die('Make fails with %d' % rv)


def date():
    return datetime.datetime.now().ctime()


class FileNotFound(Exception):

    def __init__(self, *s):
        Exception.__init__(self, *s)


def path_to(s):
    for d in os.environ['PATH'].split(':'):
        tmp = os.path.join(d, s)
        if os.access(tmp, os.X_OK):
            return tmp

    raise FileNotFound, s


def set_make_prog(*s):
    global _makeprog
    try:
        path_to(s[0])
    except FileNotFound:
        die.die("Specified make program '%s' not on PATH" % s[0])

    _makeprog = s


def ncpu--- This code section failed: ---

 L. 144         0  LOAD_CONST               0
                3  STORE_FAST            0  'n'

 L. 145         6  SETUP_LOOP           67  'to 76'
                9  LOAD_GLOBAL           0  'open'
               12  LOAD_CONST               '/proc/cpuinfo'
               15  LOAD_CONST               'r'
               18  CALL_FUNCTION_2       2  None
               21  GET_ITER         
               22  FOR_ITER             50  'to 75'
               25  STORE_FAST            1  'x'

 L. 146        28  LOAD_FAST             1  'x'
               31  LOAD_ATTR             1  'split'
               34  LOAD_CONST               ':'
               37  CALL_FUNCTION_1       1  None
               40  LOAD_CONST               0
               43  BINARY_SUBSCR    
               44  LOAD_ATTR             2  'strip'
               47  CALL_FUNCTION_0       0  None
               50  LOAD_CONST               'processor'
               53  COMPARE_OP            2  ==
               56  POP_JUMP_IF_FALSE    22  'to 22'

 L. 147        59  LOAD_FAST             0  'n'
               62  LOAD_CONST               1
               65  INPLACE_ADD      
               66  STORE_FAST            0  'n'
               69  JUMP_BACK            22  'to 22'
               72  JUMP_BACK            22  'to 22'
               75  POP_BLOCK        
             76_0  COME_FROM             6  '6'

 L. 148        76  LOAD_FAST             0  'n'
               79  LOAD_CONST               0
               82  COMPARE_OP            4  >
               85  POP_JUMP_IF_TRUE     97  'to 97'
               88  LOAD_ASSERT              AssertionError
               91  LOAD_CONST               'Silly!'
               94  RAISE_VARARGS_2       2  None

 L. 149        97  LOAD_GLOBAL           4  'str'
              100  LOAD_FAST             0  'n'
              103  CALL_FUNCTION_1       1  None
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 106


def read(fn):
    if DB_format == 'avio':
        h, d, c = avio.read_hdc(open(fn, 'r'))
    elif DB_format == 'fiatio':
        h, d, c = fiatio.read(open(fn, 'r'))
    else:
        die.die('Unknown metadata format: %s' % DB_format)
    return (
     h, d)