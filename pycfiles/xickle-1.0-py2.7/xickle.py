# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.netbsd-6.1.4-i386/egg/xickle.py
# Compiled at: 2014-09-10 01:05:37
import cStringIO as StringIO, logging, xmltodict
logging.basicConfig(level=logging.FATAL)

def loads(__xml):
    dumpedString = xmltodict.parse(__xml)
    return dict(dumpedString)


def load(file_):
    __xml = None
    with open(file_) as (fin):
        __xml = loads(fin.read())
    return __xml


def dumps(dictionary):
    __xml = xmltodict.unparse(dictionary)
    return __xml


def dump(obj, output):
    __bytes = dumps(obj)
    logging.debug(__bytes)
    with open(output, 'w') as (fout):
        fout.write(__bytes)
    return fout.name