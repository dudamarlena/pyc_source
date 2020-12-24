# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/flytrax/generate_fake_trx_file.py
# Compiled at: 2009-04-14 12:30:53
import numpy, time, traxio
(w, h) = (1600, 1200)
frames = 100
fname = 'fake'
x = 30
y = 40
(roi_w, roi_h) = (40, 60)
for framenumber in range(frames):
    x += 2
    y += 1
    x0 = x - roi_w // 2
    y0 = y - roi_h // 2
    if framenumber == 0:
        a = numpy.zeros((h, w), dtype=numpy.uint8)
        tw = traxio.TraxDataWriter(fname, a)
    else:
        a = numpy.zeros((roi_h, roi_w), dtype=numpy.uint8)
        a[(x - x0, y - y0)] = 200
        tw.write_data(roi_img=a, posx=x, posy=y, orientation=0.0, windowx=x0, windowy=y0, timestamp=time.time(), area=0.0)