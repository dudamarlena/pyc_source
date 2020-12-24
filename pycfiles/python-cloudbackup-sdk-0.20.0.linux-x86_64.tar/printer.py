# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cloudbackup/utils/printer.py
# Compiled at: 2017-05-12 15:59:18
"""
Print Utility

Wraps the built-in print such that the output is captured to a configurable file.
The file is specified in the [globals] section of the agenttests.ini:

[globals]
print=<file>

If not specified (print = None or '') then defaults to sys.stdout.
If the 'file' parameter to print() is something other than sys.stdout, then both
    the configured file and the specified file will receive the output.

The caller may optionally call setPrefix() to set prefix to all print statements.
If the prefix is None, then it will be skipped. There is no need to have a space
at the end of the prefix as one will automatically be added. This is useful to
record the output in a manner that will be re-orderable later on - for example,
prepend the test name and platform when splitting out platforms to multiple threads
to speed up processing.
"""
from __future__ import print_function
import os, sys
try:
    import __builtin__ as builtins
except ImportError:
    import builtins

__actual_print = print
__name_prefix = dict()
__name_key_fn = os.getpid
__output_file = None

def setOutputFile(filename):
    global __output_file
    __output_file = filename


def getOutputFile():
    return __output_file


def __local_print(*args, **kwargs):
    """
    Local print() implementation to enable directing to two sources - the programmed output (stdout or specified by 'file') and a configured
    output, specified via the configuration file; as well as adding a per-line prefix
    """
    global __name_key_fn
    global __name_prefix
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    out = kwargs.get('file', sys.stdout)
    flush = kwargs.get('flush', False)
    sysout = out
    filename = __output_file
    if filename is not None:
        if len(filename):
            out = open(filename, 'a+')
    print_args = list(args)
    key = __name_key_fn()
    if key in __name_prefix:
        print_args.insert(0, __name_prefix[key])
    print_args.append(end)
    for arg in print_args:
        __actual_print(arg, sep=sep, end='', file=out)
        if sysout != sys.stdout:
            __actual_print(arg, sep=sep, end='', file=sysout)

    if flush:
        out.flush()
        sysout.flush()
    return


def setPrefix(key, name=None):
    """
    Set the output prefix
    """
    __name_prefix[key] = name


def getPrefix(key):
    """
    Retrieve the output prefix
    """
    if key in __name_prefix:
        return __name_prefix[key]
    else:
        return
        return


def clearPrefix(key):
    """
    Clear output prefix
    """
    del __name_prefix[key]


def setKeyFn(fn):
    """
    set the prefix dictionary key function

    Note: This is not multithread/multiprocess safe. It should only be set before anything starts setting the keys.
    """
    global __name_key_fn
    __name_key_fn = fn


def getKeyFn():
    """
    return the prefix dictionary key function
    """
    return __name_key_fn


builtins.print = __local_print