# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/examples/stock.py
# Compiled at: 2018-10-28 11:56:52
from ffnet import ffnet, mlgraph, readdata
from numpy import array
conec = mlgraph((3, 22, 12, 1))
net = ffnet(conec)
print 'READING DATA...'
data = readdata('data/black-scholes.dat', usecols=(1, 2, 3, 4), skiprows=1)
input = data[:, :3]
target = data[:, -1]
print 'TRAINING NETWORK...'
import sys
sys.stdout.flush()
net.train_tnc(input, target, maxfun=5000, messages=1)
print
print 'TESTING NETWORK...'
output, regression = net.test(input, target, iprint=0)
Rsquared = regression[0][2]
maxerr = abs(array(output).reshape(len(output)) - array(target)).max()
print 'R-squared:           %s  (should be >= 0.999999)' % str(Rsquared)
print 'max. absolute error: %s  (should be <= 0.05)' % str(maxerr)
print
print 'Is ffnet ready for a stock?'
try:
    from pylab import *
    plot(target, 'b--')
    plot(output, 'k-')
    legend(('target', 'output'))
    xlabel('pattern')
    ylabel('price')
    title('Outputs vs. target of trained network.')
    grid(True)
    show()
except ImportError as e:
    print 'Cannot make plots. For plotting install matplotlib.\n%s' % e