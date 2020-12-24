# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ssh_keydb/akcmp.py
# Compiled at: 2012-09-26 05:09:33
import sys

def cmpline(line1, line2, i1, i2):
    items1 = line1.strip().rsplit(' ', 3)
    items2 = line2.strip().rsplit(' ', 3)
    if items1[(-2)] != items2[(-2)]:
        return False
    if line1 == line2:
        return True
    if items1[(-1)] != items2[(-1)]:
        print 'L#%i/%i ' % (i1 + 1, i2 + 1) + items1[(-1)] + ' differ on label (%s vs %s)' % (items1[(-1)], items2[(-1)])
    else:
        print 'L#%i/%i ' % (i1 + 1, i2 + 1) + items1[(-1)] + ' differ on command'
    return True


def akcmp(file1, file2):
    txt1 = file(file1).readlines()
    txt2 = file(file2).readlines()
    print '\nLeft: %s, Right: %s' % (file1, file2)
    for i1 in range(len(txt1)):
        line1 = txt1[i1]
        items1 = line1.strip().rsplit(' ', 3)
        found = False
        for i2 in range(len(txt2)):
            line2 = txt2[i2]
            found |= cmpline(line1, line2, i1, i2)

        if not found:
            print 'L#%i %s cannot be found' % (i1 + 1, items1[(-1)])


file1 = sys.argv[1]
file2 = sys.argv[2]
if len(sys.argv) > 3:
    if sys.argv[3] == '-l':
        akcmp(file1, file2)
    else:
        akcmp(file2, file1)
else:
    akcmp(file1, file2)
    akcmp(file2, file1)