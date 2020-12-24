# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Proyectos\MatplotLib.py
# Compiled at: 2016-08-26 12:42:31
# Size of source mod 2**32: 1540 bytes
import matplotlib.pyplot as plt, numpy as np, scipy.stats as ss
from matplotlib.animation import FuncAnimation

class UpdateDist(object):

    def __init__(self, ax, prob=0.5):
        self.success = 0
        self.prob = prob
        self.line, = ax.plot([], [], 'k-')
        self.x = np.linspace(0, 1, 200)
        self.ax = ax
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 15)
        self.ax.grid(True)
        self.ax.axvline(prob, linestyle='--', color='black')

    def init(self):
        self.success = 0
        self.line.set_data([], [])
        return (self.line,)

    def __call__(self, i):
        if i == 0:
            return self.init()
        else:
            if np.random.rand(1) < self.prob:
                self.success += 1
            y = ss.beta.pdf(self.x, self.success + 1, i - self.success + 1)
            self.line.set_data(self.x, y)
            return (self.line,)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ud = UpdateDist(ax, prob=0.7)
anim = FuncAnimation(fig, ud, frames=(np.arange(100)), init_func=(ud.init), interval=100,
  blit=True)
plt.show()