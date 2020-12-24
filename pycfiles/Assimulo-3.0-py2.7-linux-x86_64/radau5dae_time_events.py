# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/radau5dae_time_events.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import Radau5DAE
from assimulo.problem import Implicit_Problem

class VanDerPolProblem(Implicit_Problem):

    def __init__(self, **kargs):
        Implicit_Problem.__init__(self, **kargs)
        self.name = 'Van der Pol (implicit) with time events'
        self.my = 1.0 / 1e-06

    def res(self, t, y, yd):
        yd_0 = y[1]
        yd_1 = self.my * ((1.0 - y[0] ** 2) * y[1] - y[0])
        res_0 = yd[0] - yd_0
        res_1 = yd[1] - yd_1
        return N.array([res_0, res_1])

    def time_events(self, t, y, yd, sw):
        events = [
         1.0, 2.0, 2.5, 3.0]
        for ev in events:
            if t < ev:
                tnext = ev
                break
            else:
                tnext = None

        return tnext

    def handle_event(self, solver, event_info):
        self.my *= 0.1


def run_example(with_plots=True):
    y0 = [
     2.0, -0.6]
    yd0 = [-0.6, -200000.0]
    imp_mod = VanDerPolProblem(y0=y0, yd0=yd0)
    imp_sim = Radau5DAE(imp_mod)
    t, y, yd = imp_sim.simulate(8.0)
    if with_plots:
        P.plot(t, y[:, 0], marker='o')
        P.xlabel('Time')
        P.ylabel('State')
        P.title(imp_mod.name)
        P.show()
    x1 = y[:, 0]
    assert N.abs(x1[(-1)] - 1.14330840983) < 0.001
    return (imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()