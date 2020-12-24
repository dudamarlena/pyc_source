# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/tests/test_iterative.py
# Compiled at: 2018-05-17 07:18:17
from pynfold import fold
import numpy as np
from matplotlib import pyplot as plt

def smear(xt):
    xeff = 0.3 + 0.7 / 20.0 * (xt + 10.0)
    x = np.random.rand()
    if x > xeff:
        return None
    else:
        xsmear = np.random.normal(-2.5, 0.2)
        return xt + xsmear


dim = 40
f = fold(method='iterative')
f.set_response(dim, -10, 10)
for i in range(10000):
    xt = np.random.normal(0.3, 2.5)
    x = smear(xt)
    if x is not None:
        f.fill(x, xt)
    else:
        f.miss(xt)

f.data = f.measured.x
fig, ax = plt.subplots()
fig.facecolor = 'white'
ax.plot(range(dim), f.data, label='data')
for i in range(0, 4):
    f.iterations = i
    f.run()
    h = f.iterative.reco_hist()
    ax.plot(np.linspace(0, dim, dim / 2), h, marker='o', linestyle=':', label=('{} iterations').format(i))

ax.plot(np.linspace(0, dim, dim / 2), f.truth.x, label='truth')
left, bottom, width, height = [0.08, 0.53, 0.35, 0.35]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.imshow(np.matrix(f.response).T, interpolation='nearest', origin='low', extent=[
 f.xlo, f.xhi, f.xlo, f.xhi], cmap='Reds')
ax2.yaxis.tick_right()
plt.title('$R(x_\\mathrm{meas}|y_\\mathrm{true})$')
ax.legend()
plt.savefig('iterative.png')