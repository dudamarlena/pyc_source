# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/matutil.py
# Compiled at: 2014-06-14 02:26:24
# Size of source mod 2**32: 6234 bytes


def evalmat(mat):
    """Evaluate Matrix
        Called with a list of lists (Square Matrix)
        returns the value of the Matrix"""
    sign = 1
    result = 0
    if len(mat) == 2 and len(mat[0]) == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    else:
        nbrows = range(len(mat))
        for row in nbrows:
            if row % 2 == 0:
                sign = 1
            else:
                sign = -1
            minor = []
            if mat[row][0] == 0:
                pass
            else:
                for mrow in nbrows:
                    if mrow != row:
                        minor.append(mat[mrow][1:])

            result += sign * mat[row][0] * evalmat(minor)

        return result


def insertmat(mat, data, offset):
    """ Function to insert one Matrix (1,m) (data) in another Matrix (n,m) (mat)
        at location 'offset' and return the resulting Matrix (res).
        The lenght of "data" must be the same as the number of rows in  "mat". """
    res = []
    for row in range(len(mat)):
        res.append(mat[row][:])
        res[row][offset] = data[row]

    return res


def multmat(mata, matb):
    """ Multiply matrix A by Matrix B
    such that |C| = |A| X |B| """

    def sub_sum_product(mata, matb):
        """ Called form function 'multmat'
        not to be called from external programs...."""
        res_mat = []
        for colb in range(len(matb[0])):
            sum_product = 0
            for cola in range(len(mata)):
                sum_product += mata[cola] * matb[cola][colb]

            res_mat.append(sum_product)

        return res_mat

    result = []
    for rowa in range(len(mata)):
        result.append(sub_sum_product(mata[rowa], matb))

    return result


if __name__ == '__main__':
    print('Null Matrix Test')
    amat = [[1, 1], [1, 1]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == 0:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('Unit Matrix Test')
    amat = [[1, 0], [0, 1]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == 1:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('3X3  Null Matrix Test')
    amat = [[0, 1, 6], [0, 2, -3], [0, 9, 12]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == 0:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('3X3 Matrix Test')
    amat = [[3, 1, 6], [2, 2, -3], [5, 9, 12]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == 162:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('3X3 Unit Matrix Test')
    amat = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == 1:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('3X3 General Matrix Test')
    amat = [[3, 5, 1], [2, -2, 2], [1, 9, 5]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == -104:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('5x5 More Complex Matrix Test')
    amat = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14],
     [
      15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
    print('Input Matrix = {}'.format(amat))
    ans = evalmat(amat)
    PF = 'Fail'
    if ans == 0:
        PF = 'Pass'
    print('ans = {:d}, {:s}'.format(ans, PF))
    print()
    print('Test "insertmat function" ')
    amat = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    imat = [100, 200, 300, 400]
    print('Input Matrix = {}'.format(amat))
    print('Insert Data = {}'.format(imat))
    ans = insertmat(amat, imat, 2)
    PF = 'Fail'
    if ans == [[1, 2, 100], [4, 5, 200], [7, 8, 300], [10, 11, 400]]:
        PF = 'Pass'
    print('ans = {}, {:s}'.format(ans, PF))
    print()
    ans = insertmat(amat, imat, 0)
    PF = 'Fail'
    if ans == [[100, 2, 3], [200, 5, 6], [300, 8, 9], [400, 11, 12]]:
        PF = 'Pass'
    print('ans = {}, {:s}'.format(ans, PF))
    print()
    ans = insertmat(amat, imat, 1)
    PF = 'Fail'
    if ans == [[1, 100, 3], [4, 200, 6], [7, 300, 9], [10, 400, 12]]:
        PF = 'Pass'
    print('ans = {}, {:s}'.format(ans, PF))
    print()
    print('Test "multmat" function')
    print('Test 1')
    a = [[1, 2, 3], [4, 5, 6], [1, 2, 3]]
    b = [[7, 8], [1, 2], [5, 6]]
    print('a = {}'.format(a))
    print('b = {}'.format(b))
    c = multmat(a, b)
    PF = 'Fail'
    if c == [[24, 30], [63, 78], [24, 30]]:
        PF = 'Pass'
    print('Result = {} {:s}'.format(c, PF))
    print()
    print('Test 2')
    a = [[1, 2], [4, 5]]
    b = [[7, 8], [1, 2]]
    print('a = {}'.format(a))
    print('b = {}'.format(b))
    c = multmat(a, b)
    PF = 'Fail'
    if c == [[9, 12], [33, 42]]:
        PF = 'Pass'
    print('Result = {} {:s}'.format(c, PF))