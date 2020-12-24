# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/mech_system_pendulum.py
# Compiled at: 2018-12-15 05:51:02
import assimulo.problem as ap, assimulo.special_systems as ass, numpy as N, scipy.linalg as sl
from assimulo.solvers import IDA, ODASSL

def pendulum():
    g = 13.7503671
    n_p = 2
    n_la = 1

    def forces(t, p, v):
        return N.array([0.0, -g])

    def GT(p):
        return N.array([p[0], p[1]]).reshape((2, 1))

    def constr3(t, y):
        p = y[0:2]
        return N.array([p[0] ** 2 + p[1] ** 2 - 1.0])

    def constr2(t, y):
        p, v = y[0:2], y[2:4]
        return N.array([p[0] * v[0] + p[1] * v[1]])

    def constr1(t, y):
        p, v, la = y[0:2], y[2:4], y[4:5]
        return N.array([v[0] ** 2 + v[1] ** 2 - la[0] * (p[0] ** 2 + p[1] ** 2) - p[1] * g])

    return ass.Mechanical_System(n_p, forces, n_la, [
     1.0, 0.0], [0.0, 0.0], [
     0], [
     0.0, 0.0], [0.0, -g], GT=GT, constr3=constr3, constr2=constr2, constr1=constr1)


def run_example(index='ind1', with_plots=True, with_test=False):
    my_pend_sys = pendulum()
    my_pend = my_pend_sys.generate_problem(index)
    my_pend.name = ('Index = {}').format(index)
    dae_pend = IDA(my_pend) if index not in ('ovstab2', 'ovstab1') else ODASSL(my_pend)
    dae_pend.atol = 1e-06
    dae_pend.rtol = 1e-06
    dae_pend.suppress_alg = True
    t, y, yd = dae_pend.simulate(10.0, 100)
    final_residual = my_pend.res(0.0, dae_pend.y, dae_pend.yd)
    print my_pend.name + '  Residuals after the integration run\n'
    print (final_residual, 'Norm:  ', sl.norm(final_residual))
    assert with_test and sl.norm(final_residual) < 0.15
    if with_plots:
        dae_pend.plot(mask=[1, 1] + (len(my_pend.y0) - 2) * [0])
    return (
     my_pend, dae_pend)


if __name__ == '__main__':
    index_values = [
     'ind1', 'ind2', 'ind3', 'ggl2', 'ovstab2', 'ovstab1']
    sim = {}
    mod = {}
    for ind in index_values:
        mod[ind], sim[ind] = run_example(index=ind)