# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\netblocker\netblock\nbcalc.py
# Compiled at: 2016-03-08 18:42:10
import sys
from b3.plugins.netblocker.netblock import netblock

def die(str):
    sys.stderr.write(sys.argv[0] + ': ' + str + '\n')
    sys.exit(1)


def warn(str):
    sys.stderr.write(sys.argv[0] + ': ' + str + '\n')


def dumpout(r):
    res = r.tocidr()
    if len(res) > 0:
        print ('\n').join(res)


def process(args):
    r = netblock.IPRanges()
    if len(args) == 3 and args[1] == '-':
        process(['%s-%s' % (args[0], args[2])])
        return
    opd = r.add
    for a in args:
        op = opd
        if a == '-':
            opd = r.remove
            continue
        else:
            if a == '+':
                opd = r.add
                continue
            if a[0] == '-':
                op = r.remove
                a = a[1:]
            try:
                op(a)
            except netblock.BadCIDRError as e:
                c = netblock.convcidr(a, 0)
                die('bad CIDR %s. Should start at IP %s' % (
                 a, netblock.ipstr(c[0])))
            except netblock.NBError as e:
                die('bad argument %s: %s' % (a, str(e)))

    dumpout(r)


def maybestdin(args):
    if len(args) == 0:
        process([ x.strip() for x in sys.stdin.readlines() ])
    else:
        process(args)


if __name__ == '__main__':
    maybestdin(sys.argv[1:])