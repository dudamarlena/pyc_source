# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/dat2csv.py
# Compiled at: 2008-04-20 13:19:45
import sys
__revision__ = '$Rev$'

def dat2csv(ifname, ofname):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()
    words = [ x.split() for x in lines ]
    ofile = file(ofname, 'w+')
    for x in words:
        for y in x:
            ofile.write(y + '\n')

    ofile.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        dat2csv(sys.argv[1], sys.argv[2])
    else:
        print 'Usage %s ifile ofile' % sys.argv[0]