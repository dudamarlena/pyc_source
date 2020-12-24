# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/verify.py
# Compiled at: 2020-04-20 10:24:57
import os, marshal, tempfile
from xdis.magics import MAGIC, PYTHON_MAGIC_INT, int2magic
from xdis.version_info import PYTHON3, PYTHON_VERSION, IS_PYPY
from xdis.load import load_module

def wr_long(f, x):
    """Internal; write a 32-bit int to a file in little-endian order."""
    if PYTHON3:
        f.write(bytes([x & 255]))
        f.write(bytes([x >> 8 & 255]))
        f.write(bytes([x >> 16 & 255]))
        f.write(bytes([x >> 24 & 255]))
    else:
        f.write(chr(x & 255))
        f.write(chr(x >> 8 & 255))
        f.write(chr(x >> 16 & 255))
        f.write(chr(x >> 24 & 255))


def dump_compile(codeobject, filename, timestamp, magic):
    """Write code object as a byte-compiled file

    Arguments:
    codeobject: code object
    filefile: bytecode file to write
    timestamp: timestamp to put in file
    magic: Pyton bytecode magic
    """
    path_tmp = '%s.%s' % (filename, id(filename))
    fc = None
    try:
        fc = open(path_tmp, 'wb')
        if PYTHON3:
            fc.write(bytes([0, 0, 0, 0]))
        else:
            fc.write('\x00\x00\x00\x00')
        wr_long(fc, timestamp)
        marshal.dump(codeobject, fc)
        fc.flush()
        fc.seek(0, 0)
        fc.write(magic)
        fc.close()
        os.rename(path_tmp, filename)
    except OSError:
        try:
            os.unlink(path_tmp)
        except OSError:
            pass
        else:
            raise

    if fc:
        fc.close()
    return


def compare_code(c1, c2):
    assert c1.co_argcount == c2.co_argcount
    assert len(c1.co_consts) == len(c2.co_consts), 'consts:\n%s\nvs.\n%s' % (c1.co_consts, c2.co_consts)
    assert c1.co_filename == c2.co_filename
    assert c1.co_firstlineno == c2.co_firstlineno
    assert c1.co_flags == c2.co_flags
    assert c1.co_lnotab == c2.co_lnotab
    assert c1.co_name == c2.co_name
    assert c1.co_names == c2.co_names
    assert c1.co_nlocals == c2.co_nlocals
    assert c1.co_stacksize == c2.co_stacksize
    assert c1.co_varnames == c2.co_varnames


def compare_bytecode_files(bc_file1, bc_file2):
    f = open(bc_file1, 'rb')
    bytes1 = f.read()
    f.close
    f = open(bc_file2, 'rb')
    bytes2 = f.read()
    f.close
    if PYTHON_VERSION == 3.2:
        assert IS_PYPY and bytes1[4:] == bytes2[4:], 'bytecode:\n%s\nvs\n%s' % (bytes1[4:], bytes2[4:])
    else:
        assert bytes1 == bytes2, 'bytecode:\n%s\nvs\n%s' % (bytes1, bytes2)


def verify_file(real_source_filename, real_bytecode_filename):
    """Compile *real_source_filename* using
    the running Python interpreter. Then
    write bytecode out to a new place again using
    Python's routines.

    Next load it in using two of our routines.
    Compare that the code objects there are equal.

    Next write out the bytecode (using the same Python
    bytecode writin routine as in step 1.

    Finally compare the bytecode files.
    """
    tempdir = tempfile.gettempdir()
    source_filename = os.path.join(tempdir, 'testing.py')
    if not os.path.exists(real_source_filename):
        return
    if PYTHON_VERSION < 3.0:
        f = open(real_source_filename, 'U')
    elif PYTHON_VERSION == 3.0:
        return
    elif 3.1 <= PYTHON_VERSION <= 3.4:
        f = open(real_source_filename, 'rb')
    else:
        f = open(real_source_filename, newline=None, errors='backslashreplace')
    codestring = f.read()
    f.close()
    codeobject1 = compile(codestring, source_filename, 'exec')
    (version, timestamp, magic_int, codeobject2, is_pypy, source_size, _) = load_module(real_bytecode_filename)
    if magic_int == 3180 + 7:
        magic_int = 48
    assert MAGIC == int2magic(magic_int), 'magic_int %d vs %d in %s/%s' % (magic_int, PYTHON_MAGIC_INT, os.getcwd(), real_bytecode_filename)
    bytecode_filename1 = os.path.join(tempdir, 'testing1.pyc')
    dump_compile(codeobject1, bytecode_filename1, timestamp, MAGIC)
    (version, timestamp, magic_int, codeobject3, is_pypy, source_size, _) = load_module(real_bytecode_filename, fast_load=not is_pypy)
    bytecode_filename2 = os.path.join(tempdir, 'testing2.pyc')
    dump_compile(codeobject1, bytecode_filename2, timestamp, int2magic(magic_int))
    compare_bytecode_files(bytecode_filename1, bytecode_filename2)
    return