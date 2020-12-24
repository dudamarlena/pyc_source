# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\common\clg.py
# Compiled at: 2013-12-11 23:17:46
"""
Read from clg (ccompare log files)

read()     a generator that yields records from the file

Copyright (C) 2011 Daniel Meliza <dan // meliza.org>
Created 2011-09-08
"""
import os.path

def _read_signals(fp):
    signal_names = {}
    for line in fp:
        if line.startswith('*'):
            return signal_names
        id, location = line.strip().split('\t')
        signal_names[id] = os.path.splitext(os.path.split(location)[(-1)])[0]

    raise RuntimeError("Signal list wasn't terminated properly")


def _yield_values(fp):
    fields = None
    for line in fp:
        if fields is None:
            fields = line.strip().split('\t')
        else:
            yield dict(zip(fields, line.strip().split('\t')))

    return


def read(filename):
    fp = open(filename, 'rt')
    for line in fp:
        if line.startswith('id'):
            break

    signal_names = _read_signals(fp)
    for line in fp:
        if line.startswith('** Results'):
            break

    for dd in _yield_values(fp):
        dd['ref'] = signal_names[dd['ref']]
        dd['tgt'] = signal_names[dd['tgt']]
        yield dd