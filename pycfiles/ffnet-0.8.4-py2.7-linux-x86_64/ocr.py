# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/examples/ocr.py
# Compiled at: 2018-10-28 11:56:52
from ffnet import ffnet, mlgraph, readdata
conec = mlgraph((64, 10, 10, 10))
net = ffnet(conec)
print 'READING DATA...'
data = readdata('data/ocr.dat', delimiter=' ')
input = data[:, :64]
target = data[:, 64:]
print 'TRAINING NETWORK...'
net.train_tnc(input[:58], target[:58], maxfun=2000, messages=1)
print
print 'TESTING NETWORK...'
output, regression = net.test(input[58:], target[58:], iprint=2)
try:
    from pylab import *
    from random import randint
    digitpat = randint(58, 67)
    subplot(211)
    imshow(input[digitpat].reshape(8, 8), interpolation='nearest')
    subplot(212)
    N = 10
    ind = arange(N)
    width = 0.35
    bar(ind, net(input[digitpat]), width, color='b')
    xticks(ind + width / 2.0, ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'))
    xlim(-width, N - width)
    axhline(linewidth=1, color='black')
    title('Trained network (64-10-10-10) guesses a digit above...')
    xlabel('Digit')
    ylabel('Network outputs')
    show()
except ImportError as e:
    print 'Cannot make plots. For plotting install matplotlib.\n%s' % e