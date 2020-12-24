# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/sumparam.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'

def findatom(ifname, atmclass2):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()
    words = [ x.split() for x in lines ]
    for i in range(len(lines)):
        x = words[i]
        if len(x) > 2 and x[0] == 'atom' and int(x[2]) == atmclass2:
            print lines[i].strip()


def findatom2(ifname, atmtype, conns):
    for line in file(ifname):
        x = line.split()
        if len(x) >= 4 and x[0] == 'atom' and int(x[(-3)]) == atmtype and int(x[(-1)]) == conns:
            print line.strip()


def main():
    import sys
    if len(sys.argv) != 4:
        import os.path
        print >> sys.stderr, 'Usage: %s ifname atmtype connnum' % os.path.basename(sys.argv[0])
        sys.exit(1)
    findatom2(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))


if __name__ == '__main__':
    main()