# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/tools/onoworst.py
# Compiled at: 2019-02-26 15:15:16
# Size of source mod 2**32: 886 bytes


def generate_onoworst(outpath, vertnumber):
    f = open(outpath, 'w')
    for i in range(vertnumber - 1):
        f.write('{fro} {to}\n'.format(fro=i, to=(i + 1)))
        f.write('{fro} {to}\n'.format(fro=i, to=vertnumber))

    f.close()


def generate_dirctworst(outpath, vertnumber):
    f = open(outpath, 'w')
    for i in range(vertnumber):
        f.write('{fro} {to}\n'.format(fro=i, to=((i + 1) % vertnumber)))

    f.write('{fro} {to}\n'.format(fro=0, to=vertnumber))
    f.close()


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    size = int(float(sys.argv[2]))
    generate_dirctworst(path, size)