# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/examples/mptrain.py
# Compiled at: 2018-10-28 11:56:52
from ffnet import ffnet, mlgraph
from scipy import rand
input = rand(10000, 10)
target = rand(10000, 1)
conec = mlgraph((10, 300, 1))
net = ffnet(conec)
if __name__ == '__main__':
    from time import time
    from multiprocessing import cpu_count
    weights0 = net.weights.copy()
    print 'TRAINING, this can take a while...'
    for n in range(1, cpu_count() + 1):
        net.weights[:] = weights0
        t0 = time()
        net.train_tnc(input, target, nproc=n, maxfun=50, messages=0)
        t1 = time()
        print '%s processes: %s s' % (n, t1 - t0)