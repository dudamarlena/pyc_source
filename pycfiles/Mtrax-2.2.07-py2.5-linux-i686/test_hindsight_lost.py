# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/test_hindsight_lost.py
# Compiled at: 2008-01-29 20:48:29
import ellipsesk as ell, numpy as num, matchidentities, hindsight
from params import params
import estconncomps as est, pylab as mpl
colors = [
 'r', 'g', 'b', 'y']
tracks = []
params.dampen = 0.0
tracks.append(ell.TargetList())
tracks[0][0] = ell.Ellipse(10.0, 10.0, 1.0, 2.0, num.pi / 3, 0.0, 0)
tracks[0][0].compute_area()
tracks.append(ell.TargetList())
tracks[1][0] = tracks[0][0].copy()
tracks[1][0].x += 10.0
tracks[1][0].y += 10.0
tracks.append(ell.TargetList())
prev = tracks[0].copy()
curr = tracks[1].copy()
pred = matchidentities.cvpred(prev, curr)
tracks.append(ell.TargetList())
prev = curr
curr = pred
pred = matchidentities.cvpred(prev, curr)
tracks.append(ell.TargetList())
prev = curr
curr = pred
pred = matchidentities.cvpred(prev, curr)
pred0 = pred[0].copy()
pred0.identity = 1
tracks[4][1] = pred0
tracks.append(ell.TargetList())
prev = curr
curr = pred
pred = matchidentities.cvpred(prev, curr)
pred0 = pred[0].copy()
pred0.identity = 1
tracks[5][1] = pred0
tracks.append(ell.TargetList())
prev = curr
curr = pred
pred = matchidentities.cvpred(prev, curr)
pred0 = pred[0].copy()
pred0.identity = 1
tracks[6][1] = pred0
params.nids = 2
bw = []
bounds = [
 0, 100, 0, 100]
nr = bounds[1] - bounds[0]
nc = bounds[3] - bounds[2]
for track in tracks:
    tmp = num.zeros((nr, nc), dtype=bool)
    for ellipse in track.itervalues():
        tmp |= est.ellipsepixels(ellipse, bounds)

    bw.append(tmp)

dfore = []
for b in bw:
    dfore.append(b.astype(float))

class BG:

    def __init__(self, dfore, bw):
        self.dfore = dfore
        self.bw = bw

    def sub_bg(self, frame):
        return (self.dfore[frame], self.bw[frame])


bg = BG(dfore, bw)
hind = hindsight.Hindsight(tracks, bg)
hind.initialize_milestones()
print 'milestones: '
print hind.milestones
print 'tracks: '
print tracks
for t in range(2, len(tracks)):
    hind.fixerrors(t)

for t in range(len(tracks)):
    mpl.imshow(bw[t])
    for (id, e) in tracks[t].iteritems():
        est.drawellipse(e, colors[id])

    mpl.show()