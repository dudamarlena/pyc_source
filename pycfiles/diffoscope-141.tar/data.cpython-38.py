# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lamby/git/debian/reproducible-builds/diffoscope/tests/utils/data.py
# Compiled at: 2020-04-15 14:13:01
# Size of source mod 2**32: 2146 bytes
import contextlib, os, re, pytest
from diffoscope.comparators.binary import FilesystemFile
import diffoscope.comparators.utils.specialize as specialize
re_normalize_zeros = re.compile('^(?P<prefix>[ \\-\\+])(?P<offset>[0-9a-f]+)(?=: )', re.MULTILINE)

def init_fixture(filename):
    return pytest.fixture(lambda : specialize(FilesystemFile(filename)))


def data(filename):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)


def get_data--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              data
                4  LOAD_FAST                'filename'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_STR                 'utf-8'
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'f'

 L.  46        18  LOAD_FAST                'f'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       14  '14'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 26


@contextlib.contextmanager
def cwd_data():
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = os.getcwd
    os.chdir(data(''))
    try:
        (yield)
    finally:
        os.chdir(prev_cwd)


def load_fixture(filename):
    return init_fixture(data(filename))


def normalize_zeros(s):

    def repl(x):
        return '{}{:08x}'.format(x.group('prefix'), int(x.group('offset'), 16))

    return re_normalize_zeros.sub(repl, s)