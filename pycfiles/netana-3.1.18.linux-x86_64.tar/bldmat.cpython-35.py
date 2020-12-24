# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/bldmat.py
# Compiled at: 2014-06-13 19:28:46
# Size of source mod 2**32: 902 bytes


def bldmat(nbrow=2, nbcol=2, obj='0'):
    """Build matrix of obj's nbrows by nbcols.
    Call: bldmat(nbrow=2,nbcol=2,obj='0')
    Returns: Matrix (list of lists) of obj."""
    res = []
    for row in range(nbrow):
        temp = []
        for col in range(nbcol):
            temp.append(obj)

        if nbrow == 1:
            return temp
        res.append(temp)

    return res


if __name__ == '__main__':
    mat = bldmat(10, 10)
    print('10X10 "0" matrix')
    print('{}'.format(mat))
    mat = bldmat(1, 10)
    print('1X10 "0" matrix')
    print('{}'.format(mat))
    mat = bldmat(3, 3, 'A')
    print('3X3 "A" matrix')
    print('{}'.format(mat))
    mat[0][0] = 'B'
    print('{}'.format(mat))