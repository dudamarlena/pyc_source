# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioUtil/bgzip.py
# Compiled at: 2016-02-24 03:36:29
# Size of source mod 2**32: 2890 bytes
"""
bgzip file IO
TODO: extend to generally pipe IO ??

Sein Tao, <sein.tao@gmail.com>
2015-08-21 16:40:08 CST
"""
import io, subprocess, warnings, builtins, types

def open(filename, mode='r', encoding=None, errors=None, newline=None):
    """open bgzip file, handles text wrapper"""
    zmode = mode.replace('t', '')
    binary_file = BGzipFile(filename, zmode)
    if 'b' not in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    else:
        return binary_file


class BGzipFile(io.BufferedIOBase):
    __doc__ = 'BGzipFile handles IO from bgzip command.'
    _cmd = 'bgzip'

    def __new__(cls, filename, mode='r'):
        """Constructor, program indecates the path to excutable file"""
        raw_mode = mode
        if 't' in mode:
            warnings.warn("'t' in BGzipFile: not competable mode.")
            mode = mode.replace('t', '')
        elif 'b' not in mode:
            mode += 'b'
        else:
            if 'r' in mode:
                pipe = subprocess.Popen([cls._cmd, '-d'], stdin=(builtins.open(filename, mode)),
                  stdout=(subprocess.PIPE))
                fh = pipe.stdout
            else:
                if 'w' in mode:
                    pipe = subprocess.Popen([cls._cmd], stdin=(subprocess.PIPE),
                      stdout=(builtins.open(filename, mode)))
                    fh = pipe.stdin
                else:
                    raise ValueError('Invalid mode: {}'.format(raw_mode))

        def close(fh):
            fh._close()
            if pipe.wait() != 0:
                warnings.warn('file close error:{}'.format(filename))

        fh._close = fh.close
        fh.close = types.MethodType(close, fh)
        return fh