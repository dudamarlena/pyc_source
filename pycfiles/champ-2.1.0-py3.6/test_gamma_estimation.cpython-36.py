# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/champ/test_gamma_estimation.py
# Compiled at: 2018-08-27 07:54:09
# Size of source mod 2**32: 1742 bytes
import igraph as ig
from math import log
import matplotlib.pyplot as plt
from champ.parameter_estimation import iterative_monolayer_resolution_parameter_estimation
from numpy import mean
xs = []
ys1 = []
ys2 = []
for q in range(3, 16):
    community_sizes = [
     250] * q
    n = 250 * q
    p_in = 16 * n / (q * 250 * 249)
    p_out = 8 * n / (q * (q - 1) * 250 * 250)
    pref_matrix = [[p_in if i == j else p_out for j in range(q)] for i in range(q)]
    G = ig.Graph.SBM(n, pref_matrix, community_sizes)
    k = mean([G.degree(v) for v in range(n)])
    true_omega_in = p_in * (2 * G.ecount()) / (k * k)
    true_omega_out = p_out * (2 * G.ecount()) / (k * k)
    true_gamma = (true_omega_in - true_omega_out) / (log(true_omega_in) - log(true_omega_out))
    print('##########' + ' {} communities, true gamma={:0.4f} '.format(q, true_gamma) + '##########')
    gamma, _ = iterative_monolayer_resolution_parameter_estimation(G, gamma=1.0, tol=0.001, verbose=True)
    xs.append(q)
    ys1.append(true_gamma)
    ys2.append(gamma)

p1 = plt.scatter(xs, ys1, marker='o')
p2 = plt.scatter(xs, ys2, marker='+')
plt.legend((p1, p2), ('True Gamma', 'Estimated Gamma'))
plt.show()
G = ig.Graph.Famous('Zachary')
current_gamma = 0.0
while current_gamma < 2.0:
    print('##########' + ' initial gamma: {:.2f} '.format(current_gamma) + '##########')
    try:
        iterative_monolayer_resolution_parameter_estimation(G, gamma=current_gamma, tol=0.001, verbose=True)
    except ValueError:
        print('Degenerate partition')

    current_gamma += 0.1