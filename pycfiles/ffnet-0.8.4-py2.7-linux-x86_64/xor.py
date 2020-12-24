# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/examples/xor.py
# Compiled at: 2018-10-28 11:56:52
from ffnet import ffnet, mlgraph
conec = mlgraph((2, 2, 1))
net = ffnet(conec)
input = [
 [
  0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
target = [[1.0], [0.0], [0.0], [1.0]]
print 'FINDING STARTING WEIGHTS WITH GENETIC ALGORITHM...'
net.train_genetic(input, target, individuals=20, generations=500)
print 'TRAINING NETWORK...'
net.train_tnc(input, target, maxfun=1000, messages=1)
print
print 'TESTING NETWORK...'
output, regression = net.test(input, target, iprint=2)
from ffnet import savenet, loadnet, exportnet
print 'Network is saved...'
savenet(net, 'xor.net')
print 'Network is reloaded...'
net = loadnet('xor.net')
print 'Network is tested again, but nothing is printed...'
output, regression = net.test(input, target, iprint=0)
print
print 'Exporting trained network to the fortran source...'
exportnet(net, 'xor.f')
print 'Done...'
print 'Look at the generated xor.f file.'
print 'Note: you must compile xor.f along with the ffnet.f'
print 'file which can be found in ffnet sources.'