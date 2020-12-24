# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/wequ.py
# Compiled at: 2014-10-07 19:06:10
# Size of source mod 2**32: 1979 bytes
NBCOL = 3

def wequ(fn):
    """ This module will read a net file "fn" containing
        components and node connection specifications. It will
        output the matrix node equations. Format of the 'net'
        data file example of one line:
                c1+y1+A*ya,3,4   equation, node 3, mutual (adjacent node 4
                A zero in the third column refers to common or ground.
        input: fn = filename of net file (connection list)
        output: square matrix (list of lists) of size equal number of
        voltage nodes."""
    with open(fn, 'r') as (equfile):
        nbnodes = 0
        nodedict = {}
        mdict = {}
        for line in equfile:
            if line == '\n' or line[0] == '#' or line == '':
                pass
            else:
                line = line[:line.find('#')]
                line = line.strip()
                line = line.upper()
                print('line = ', line)
                c, n, m = line.split(',', NBCOL)
                i = int(n)
                if i > nbnodes:
                    nbnodes = i
                if not int(m):
                    if n in nodedict:
                        nodedict[n] += ' + ' + c
                    else:
                        nodedict[n] = c
                    if int(m):
                        if n in mdict:
                            nn = len(mdict[n]) - 1
                            if mdict[n][nn][1] == m:
                                mdict[n][nn][0] += '+' + c
                            else:
                                mdict[n].append([c, m])
                        else:
                            mdict[n] = [
                             [
                              c, m]]

    mat = [
     [
      '0'] * nbnodes] * nbnodes
    for key in nodedict:
        i = int(key) - 1
        mat[i][i] = nodedict[key]

    for key in mdict:
        lst = mdict[key]
        for row in lst:
            mr = int(key) - 1
            mc = int(row[1]) - 1
            mat[mr][mc] = '-(' + row[0] + ')'

    return mat


if __name__ == '__main__':
    mat = wequ('examples/BainterFilter.net')
    print('mat = ', mat)