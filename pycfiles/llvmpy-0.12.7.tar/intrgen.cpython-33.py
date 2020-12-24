# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sklam/dev/llvmpy/dist/0.12.7/tools/intrgen.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 831 bytes
import sys

def gen(f, out=sys.stdout):
    intr = []
    maxw = 0
    flag = False
    for line in open(f):
        if line.startswith('#ifdef GET_INTRINSIC_ENUM_VALUES'):
            flag = True
        elif flag:
            if line.startswith('#endif'):
                break
            else:
                item = line.split()[0].replace(',', '')
                if len(item) > maxw:
                    maxw = len(item)
                intr.append(item)
                continue

    maxw = len('INTR_') + maxw
    idx = 1
    for i in intr:
        s = 'INTR_' + i.upper()
        out.write('%s = %d\n' % (s.ljust(maxw), idx))
        idx += 1


if __name__ == '__main__':
    gen(sys.argv[1])