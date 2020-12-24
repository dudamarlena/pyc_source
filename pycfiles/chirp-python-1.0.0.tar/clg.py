# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\common\clg.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nRead from clg (ccompare log files)\n\nread()     a generator that yields records from the file\n\nCopyright (C) 2011 Daniel Meliza <dan // meliza.org>\nCreated 2011-09-08\n'
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