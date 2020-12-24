# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/examples/sin.py
# Compiled at: 2018-10-28 11:56:52
from ffnet import ffnet
from math import pi, sin, cos
conec = [
 (1, 2), (1, 3), (1, 4), (1, 5), (2, 6), (3, 6), (4, 6), (5, 6),
 (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
net = ffnet(conec)
patterns = 16
input = [[0.0]] + [ [k * 2 * pi / patterns] for k in xrange(1, patterns + 1) ]
target = [ [sin(x[0])] for x in input ]
print 'FINDING STARTING WEIGHTS WITH GENETIC ALGORITHM...'
net.train_genetic(input, target, individuals=20, generations=500)
print 'TRAINING NETWORK...'
net.train_tnc(input, target, maxfun=5000, messages=1)
print
print 'TESTNG NETWORK...'
output, regression = net.test(input, target, iprint=2)
try:
    from pylab import *
    points = 128
    xaxis = [0.0] + [ k * 2 * pi / points for k in xrange(1, points + 1) ]
    sine = [ sin(x) for x in xaxis ]
    cosine = [ cos(x) for x in xaxis ]
    netsine = [ net([x])[0] for x in xaxis ]
    netcosine = [ net.derivative([x])[0][0] for x in xaxis ]
    subplot(211)
    plot(xaxis, sine, 'b--', xaxis, netsine, 'k-')
    legend(('sine', 'network output'))
    grid(True)
    title('Outputs of trained network.')
    subplot(212)
    plot(xaxis, cosine, 'b--', xaxis, netcosine, 'k-')
    legend(('cosine', 'network derivative'))
    grid(True)
    show()
except ImportError:
    print 'Cannot make plots. For plotting install matplotlib...'