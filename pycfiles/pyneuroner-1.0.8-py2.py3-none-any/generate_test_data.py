# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyneuroml/plot/generate_test_data.py
# Compiled at: 2018-09-10 05:44:50
from random import random
import math
t_max = 1
flat = open('flat.spikes', 'w')
noisy = open('noisy.spikes', 'w')
sines = open('sines.spikes', 'w')
rates = {0: 100, 1: 150}
for id in rates:
    rate = float(rates[id])
    isi = 1 / rate
    t = isi
    while t <= t_max:
        flat.write('%i\t%s\n' % (id, t))
        noisy.write('%i\t%s\n' % (id, t + 0.002 * random()))
        t += isi

for id in range(100):
    av_isi = 0.01
    t = av_isi
    while t <= t_max:
        av_isi = 0.01 + 0.005 * math.sin(t / 0.1)
        sines.write('%i\t%s\n' % (id, t))
        t += av_isi * (0.8 + 0.4 * random())

flat.close()
noisy.close()
sines.close()