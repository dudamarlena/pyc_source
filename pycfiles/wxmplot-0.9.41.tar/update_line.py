# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./update_line.py
# Compiled at: 2016-12-12 14:32:00
_doc_ = '\n\nFast update of a plot with update_line.\n\nUsing update_line(x, y, trace=i) will replace the data plotted\nin trace i with the (x, y) values supplied.  This is much faster\nthan re-running plot(), and is recommended if the only change is\nthat the data has changed.\n\nThe example here shows two traces (1 using the right axis, 1 the\nleft axis) that are updated, as to simulate adding data.\n'
from numpy import arange, sin, cos
import time
x = arange(1200)
y1 = sin(x / 123)
y2 = 41 + 22 * cos(x / 587.0)
newplot(x[:2], y1[:2], side='left', ymin=-1.2, ymax=1.2)
t0 = time.time()
npts = 40
s = int((len(x) - 1) / npts)
ndraws = 0
for i in range(npts):
    print '==> ', i, ndraws, 1 + s * i, time.time() - t0
    update_line(x[:1 + s * i], y1[:1 + s * i], trace=1)

update_trace(x, y1, trace=1, redraw=True)
print 'updated plot %i times in %.2f seconds' % (npts, time.time() - t0)