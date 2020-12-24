# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chuan/GitHub/OrthNet/orthnet/utils/multi_dim.py
# Compiled at: 2018-03-08 02:47:33
# Size of source mod 2**32: 1305 bytes


def enumerate_dim(n, dim):
    """
        enumerate dims:
                find DIM nonnegative numbers, the sum of which is n, return result in lexicographical order.

        input:
                n: total order
                dim: dimension (number of variables)

        output:
                a 2D-list, each element a combination (a list)

        >>> enumerate_dim(3, 2)
        >>> [[3, 0], [2, 1], [1, 2], [0, 3]]
        """

    def dfs(res, cur, n, dim):
        if dim == 1:
            res.append(cur + [n])
            return
        for i in reversed(range(n + 1)):
            dfs(res, cur + [i], n - i, dim - 1)

    res = []
    dfs(res, [], n, dim)
    return res


def enum_dim(n, dim):
    """
        enumerate dims:
                find DIM nonnegative numbers, the sum of which <= n, return result in lexicographical order.

        input:
                n: total order
                dim: dimension (number of variables)

        output:
                a 2D-list, each element a combination (a list)

        >>> enum_dim(3, 2)
        >>> [[0, 0], [1, 0], [0, 1], [2, 0], [1, 1], [0, 2], [3, 0], [2, 1], [1, 2], [0, 3]]
        """
    res = [
     [
      [0 for i in range(dim)]]]
    for i in range(n):
        cur = []
        for comb in res[(-1)]:
            for j in range(len(comb)):
                tmp = comb[:]
                tmp[j] += 1
                flag = 1
                for k in cur:
                    if tmp == k:
                        flag = 0
                        break

                if flag:
                    cur.append(tmp)

        res.append(cur)

    return res


def dim(n, d):
    res = []
    for i in range(n + 1):
        res.append(enum_dim(i, d))

    return res