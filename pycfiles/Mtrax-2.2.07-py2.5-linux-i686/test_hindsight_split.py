# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/test_hindsight_split.py
# Compiled at: 2008-01-29 20:48:29
import scipy.ndimage.measurements as meas, ellipsesk as ell, numpy as num, matchidentities
m_id = matchidentities
import hindsight
from params import params
import estconncomps as est, pylab as mpl
params.dampen = 0.0

def find_flies(old0, old1, obs):
    """All arguments are EllipseLists. Returns an EllipseList."""
    if len(obs) == 0:
        flies = ell.TargetList()
        return flies
    targ = m_id.cvpred(old0, old1)
    ids = []
    for i in targ.iterkeys():
        ids.append(i)

    vals = []
    for i in targ.itervalues():
        vals.append(i)

    cost = num.zeros((len(obs), len(targ)))
    for (i, observation) in enumerate(obs):
        for (j, target) in enumerate(vals):
            if target.isDummy():
                cost[(i, j)] = params.max_jump + eps
            else:
                cost[(i, j)] = observation.dist(target)

    (obs_for_target, unass_obs) = m_id.matchidentities(cost)
    flies = ell.TargetList()
    for tt in range(len(targ)):
        if obs_for_target[tt] >= 0:
            obs[obs_for_target[tt]].identity = ids[tt]
            flies.append(obs[obs_for_target[tt]])

    for oo in range(len(obs)):
        if unass_obs[oo]:
            obs[oo].identity = params.nids
            params.nids += 1
            flies.append(obs[oo])

    return (
     flies, obs_for_target, unass_obs)


tracks_true = []
cc = []
tracks_true.append(ell.TargetList())
tracks_true[0][0] = ell.Ellipse(50.0, 10.0, 2.0, 4.0, num.pi / 3, 0.0, 0)
tracks_true[0][0].compute_area()
tracks_true.append(ell.TargetList())
tracks_true[1][0] = ell.Ellipse(50.0, 20.0, 2.0, 4.0, num.pi / 3, 0.0, 0)
tracks_true[1][0].compute_area()
for t in range(2, 9):
    tracks_true.append(matchidentities.cvpred(tracks_true[(-2)], tracks_true[(-1)]))

bw = []
bounds = [0, 100, 0, 100]
nr = bounds[1] - bounds[0]
nc = bounds[3] - bounds[2]
for track_true in tracks_true:
    tmp = num.zeros((nr, nc), dtype=bool)
    for ellipse in track_true.itervalues():
        tmp |= est.ellipsepixels(ellipse, bounds)

    bw.append(tmp)

for t in range(3, 6):
    x = tracks_true[t][0].x
    bw[t][:, x] = False

colors = ['r', 'g', 'b', 'y']
tracks = []
cc = []
obs = ell.find_ellipses(bw[0].astype(float), bw[0], False)
(L, ncc) = meas.label(bw[0])
cc.append(L)
tracks.append(ell.TargetList())
for (i, o) in enumerate(obs):
    o.identity = i
    tracks[0].append(o)

params.nids = len(tracks[0])
for t in range(1, len(bw)):
    obs = ell.find_ellipses(bw[t].astype(float), bw[t], False)
    nids = params.nids
    (L, ncc) = meas.label(bw[t])
    if len(tracks) == 1:
        (targ, obs_for_target, unass_obs) = find_flies(tracks[(-1)], tracks[(-1)], obs)
    else:
        (targ, obs_for_target, unass_obs) = find_flies(tracks[(-1)], tracks[(-1)], obs)
    tracks.append(targ)
    c = L.copy()
    for (t, o) in enumerate(obs_for_target):
        if o > 0:
            c[L == o + 1] = t + 1

    for oo in range(len(obs)):
        if unass_obs[oo]:
            c[L == oo + 1] = nids + 1
            nids += 1

    cc.append(c)

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
for t in range(2, len(tracks)):
    hind.fixerrors(t)

for t in range(len(tracks)):
    mpl.imshow(bw[t])
    for (id, e) in tracks[t].iteritems():
        est.drawellipse(e, colors[id])

    mpl.show()