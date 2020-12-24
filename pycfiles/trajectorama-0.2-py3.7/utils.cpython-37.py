# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trajectorama/utils.py
# Compiled at: 2020-01-31 12:39:05
# Size of source mod 2**32: 648 bytes
import datetime, errno, fbpca, os, sys

def tprint(string):
    string = str(string)
    sys.stdout.write(str(datetime.datetime.now()) + ' | ')
    sys.stdout.write(string + '\n')
    sys.stdout.flush()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        try:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
        finally:
            exc = None
            del exc


def reduce_dimensionality(X, dim_red_k=100):
    k = min((dim_red_k, X.shape[0], X.shape[1]))
    from fbpca import pca
    U, s, Vt = pca(X, k=k)
    return U[:, range(k)] * s[range(k)]