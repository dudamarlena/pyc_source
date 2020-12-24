# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/util/io.py
# Compiled at: 2019-08-05 00:35:42
import json, pprint

def read(fname='_tmp', lines=False, isjson=False, default=None, binary=False):
    try:
        f = open(fname, binary and 'rb' or 'r')
    except Exception as e:
        if default is not None:
            return default
        if lines:
            return []
        return

    if lines:
        text = f.readlines()
    else:
        text = f.read()
    f.close()
    if isjson:
        return json.loads(text)
    else:
        return text


def write(data, fname='_tmp', isjson=False, ispretty=False, binary=False, append=False, newline=False):
    f = open(fname, append and 'a' or binary and 'wb' or 'w')
    f.write(isjson and (ispretty and pprint.pformat(data) or json.dumps(data)) or data)
    if newline:
        f.write('\n')
    f.close()


def writejson(data, fname):
    write(data, '%s.json' % (fname,), True)
    write(data, '%s-pretty.json' % (fname,), True, True)