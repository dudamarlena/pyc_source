# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/meminfo.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 1080 bytes
from size.size import Size

def parse_meminfo():
    with open('/proc/meminfo') as (fp):
        data = fp.read()
    d = {}
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        k, v = line.split(':')
        v = v.strip()
        if 'kB' in v:
            v = Size(v).bytes
        d[k] = v

    return d


if __name__ == '__main__':
    print(parse_meminfo())