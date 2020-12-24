# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alphan/Documents/svn/academic/bu/research/implementation/lomap-ltl_optimal_multi-agent_planner/trunk/examples/ijrr2014_rec_hor/planner.py
# Compiled at: 2015-04-14 17:07:12
import networkx as nx, itertools as it
from matplotlib.path import Path
import lomap
from lomap.algorithms.dijkstra import dijkstra_to_all, source_to_target_dijkstra
from collections import defaultdict
from pprint import pprint as pp
import logging
logger = logging.getLogger(__name__)

class Planner:

    def __init__(self, env, quad, global_spec, local_spec, prio):
        self.env = env
        self.quad = quad
        self.global_spec = global_spec
        self.local_spec = local_spec
        self.prio = prio
        self.global_ts = self.construct_global_ts()
        logger.debug('Global TS has %s states and %s edges.' % self.global_ts.size())
        self.global_nba = lomap.Buchi()
        self.global_nba.buchi_from_formula(global_spec)
        logger.debug('Global NBA has %s states and %s edges.' % self.global_nba.size())
        self.global_pa = lomap.ts_times_buchi(self.global_ts, self.global_nba)
        self.clean_final_states()
        assert len(self.global_pa.final) > 0, "Global spec '%s' is not satisfiable" % global_spec
        logger.debug('Global product automaton has %s states and %s edges.' % self.global_pa.size())
        self.dist_table, self.path_table = self.compute_dist_and_path_tables()
        logger.debug('Global product automaton distance table: %s' % self.dist_table)
        logger.debug('Global product automaton path table: %s' % self.path_table)
        self.global_pa_state = self.compute_global_pa_init()
        logger.debug('Initial global product automaton state: %s' % (self.global_pa_state,))
        self.local_fsa = self.construct_local_fsa()
        logger.debug('Local FSA has %s states and %s edges.' % self.local_fsa.size())
        assert len(self.local_fsa.init.keys()) == 1, 'Local FSA must be deterministic with a single initial state.'
        self.local_fsa_state = self.local_fsa.init.keys()[0]
        logger.debug('Initial local FSA state: %s.' % self.local_fsa_state)

    def compute_global_pa_init(self):
        dist_star, state_star = float('Inf'), None
        for s in self.global_pa.init:
            dist = self.dist_table[s]
            if dist < dist_star:
                dist_star = dist
                state_star = s

        return state_star

    def construct_local_fsa(self):
        ts = lomap.Ts()
        edges = []
        init_state = None
        if self.local_spec == '(assist|extinguish)*':
            edges += [('init', 'init', {'input': set(['assist'])})]
            edges += [('init', 'init', {'input': set(['extinguish'])})]
            init_state = 'init'
        else:
            if self.local_spec == '(pickup.dropoff)*':
                edges += [('empty', 'cargo', {'input': set(['pickup'])})]
                edges += [('cargo', 'empty', {'input': set(['dropoff'])})]
                init_state = 'empty'
            elif self.local_spec == '(pickup1.dropoff1|pickup2.dropoff2)*':
                edges += [('empty', 'cargoa', {'input': set(['pickup1'])})]
                edges += [('cargoa', 'empty', {'input': set(['dropoff1'])})]
                edges += [('empty', 'cargob', {'input': set(['pickup2'])})]
                edges += [('cargob', 'empty', {'input': set(['dropoff2'])})]
                init_state = 'empty'
            else:
                assert False, 'Local spec %s is not implemented' % self.local_spec
            for s, v, d in edges:
                ts.g.add_edge(s, v, None, d)

        ts.init[init_state] = 1
        return ts

    def construct_local_ts(self):
        ts = lomap.Ts()
        ts.name = 'Local TS'
        center_cell = (
         self.quad.x, self.quad.y)
        ts.init[center_cell] = 1
        for cx, cy in it.product(range(0, self.quad.sensing_range), repeat=2):
            cell = self.quad.get_sensing_cell_global_coords((cx, cy))
            props = self.quad.sensed[cx][cy]['local_reqs']
            ts.g.add_node(cell, prop=props)

        assert len(ts.g) == self.quad.sensing_range ** 2
        for cell in ts.g:
            x, y = cell
            controls = {'e': (x + 1, y), 'n': (x, y + 1), 'w': (x - 1, y), 's': (x, y - 1), 'h': (x, y)}
            for ctrl in controls:
                neigh = controls[ctrl]
                if neigh not in ts.g:
                    continue
                ts.g.add_edge(cell, neigh, weight=1, control=ctrl)

        return ts

    def next_command(self):
        local_ts = self.construct_local_ts()
        local_ts_state = local_ts.init.keys()[0]
        d_star, cell_next_star, target_cell_star, g_next_star, path_star = (
         float('inf'), None, None, None, None)
        local_reqs = reduce(lambda a, b: a | b, [ local_ts.g.node[cell]['prop'] for cell in local_ts.g ], set([]))
        logger.debug('Sensed local requests: %s' % local_reqs)
        enabled_reqs = set([])
        for _, _, d in self.local_fsa.g.out_edges_iter((self.local_fsa_state,), data=True):
            enabled_reqs = enabled_reqs | d['input']

        serviceable_reqs = local_reqs & enabled_reqs
        global_req_cells = reduce(lambda a, b: a | b, [ set([q]) for q in local_ts.g if q in self.env.global_reqs ], set([]))
        local_req_cells = reduce(lambda a, b: a | b, [ set([q]) for q in local_ts.g if local_ts.g.node[q]['prop'] ], set([]))
        if not serviceable_reqs:
            for cur, neigh in self.global_pa.g.out_edges_iter(self.global_pa_state):
                if neigh[0] in local_ts.g:
                    avoid_cells = (global_req_cells | local_req_cells) - {neigh[0]}
                    target_cells = {
                     neigh[0]}
                else:
                    avoid_cells = global_req_cells | local_req_cells
                    target_cells = set([])
                    x_min, y_min = self.quad.get_sensing_cell_global_coords((0, 0))
                    x_max, y_max = self.quad.get_sensing_cell_global_coords((self.quad.sensing_range - 1, self.quad.sensing_range - 1))
                    for local_cell in local_ts.g.nodes_iter():
                        x, y = local_cell
                        if x == x_min or x == x_max or y == y_min or y == y_max:
                            target_cells.add(local_cell)

                    target_cells = target_cells - avoid_cells
                for u, v, k in local_ts.g.in_edges_iter(avoid_cells, keys=True):
                    local_ts.g[u][v][k]['weight'] = float('inf')

                dists, paths = dijkstra_to_all(local_ts.g, local_ts_state)
                for u, v, k in local_ts.g.in_edges_iter(avoid_cells, keys=True):
                    local_ts.g[u][v][k]['weight'] = 1

                for target_cell in target_cells:
                    d_plan = abs(target_cell[0] - neigh[0][0]) + abs(target_cell[1] - neigh[0][1])
                    d_plan += self.dist_table[neigh]
                    d_plan += dists[target_cell]
                    if d_plan < d_star or d_plan == d_star and target_cell_star and (target_cell[0] < target_cell_star[0] or target_cell[0] == target_cell_star[0] and target_cell[1] > target_cell_star[1]):
                        d_star = d_plan
                        g_next_star = neigh
                        cell_next_star = paths[target_cell][1]
                        path_star = paths[target_cell]
                        target_cell_star = target_cell

        else:
            max_prio = min([ self.prio[req] for req in serviceable_reqs ])
            target_reqs = set([ req for req in serviceable_reqs if self.prio[req] == max_prio ])
            target_cells = set([ cell for cell in local_ts.g if local_ts.g.node[cell]['prop'] & target_reqs ])
            logger.debug('Will service local requests: %s at cells %s' % (target_reqs, target_cells))
            avoid_cells = (global_req_cells | local_req_cells) - target_cells
            logger.debug('Cells to avoid: %s' % avoid_cells)
            for u, v, k in local_ts.g.in_edges_iter(avoid_cells, keys=True):
                local_ts.g[u][v][k]['weight'] = float('inf')

            dists, paths = dijkstra_to_all(local_ts.g, local_ts_state)
            for u, v, k in local_ts.g.in_edges_iter(avoid_cells, keys=True):
                local_ts.g[u][v][k]['weight'] = 1

            for target_cell in target_cells:
                if dists[target_cell] == float('inf'):
                    continue
                d_plan = dists[target_cell]
                if d_plan < d_star:
                    d_star = d_plan
                    g_next_star = None
                    cell_next_star = paths[target_cell][1]
                    path_star = paths[target_cell]

        assert d_star != float('inf'), 'Could not find a feasible local plan'
        logger.debug('Path to target: %s, cell_next_star: %s' % (path_star, cell_next_star))
        assert len(local_ts.g[local_ts_state][cell_next_star]) == 1, 'Local TS cannot have parallel edges'
        control_star = local_ts.g[local_ts_state][cell_next_star][0]['control']
        if g_next_star and g_next_star[0] == cell_next_star:
            self.global_pa_state = g_next_star
            logger.debug('Updated global product automaton state to: %s' % (g_next_star,))
        found_next_local_fsa_state = False
        next_local_req = local_ts.g.node[cell_next_star]['prop']
        if next_local_req:
            for _, next_local_fsa_state, d in self.local_fsa.g.out_edges_iter((self.local_fsa_state,), data=True):
                if d['input'] == next_local_req:
                    self.local_fsa_state = next_local_fsa_state
                    found_next_local_fsa_state = True
                    break

            assert found_next_local_fsa_state, 'Local FSA does not have a transition for %s from its current state %s' % (next_local_req, self.local_fsa_state)
        if next_local_req:
            self.env.local_reqs[cell_next_star]['on'] = False
        return (control_star, path_star)

    def clean_final_states(self):
        unreaching_finals = set()
        unreaching_finals.update(self.global_pa.final)
        for final in self.global_pa.final:
            dist, _ = source_to_target_dijkstra(self.global_pa.g, final, final, degen_paths=False, weight_key='weight')
            if dist == float('inf'):
                continue
            unreaching_finals -= set([final])

        self.global_pa.final -= unreaching_finals
        for state in unreaching_finals:
            if state in self.global_pa.init:
                del self.global_pa.init[state]

        self.global_pa.g.remove_nodes_from(unreaching_finals)

    def compute_dist_and_path_tables(self):
        dist_table = dict()
        path_table = dict()
        for node in self.global_pa.g.nodes():
            dist_table[node] = float('inf')
            path_table[node] = None
            dists, paths = dijkstra_to_all(self.global_pa.g, node, degen_paths=True, weight_key='weight')
            for final in self.global_pa.final:
                if final in dists and dists[final] < dist_table[node]:
                    dist_table[node] = dists[final]
                    path_table[node] = paths[final]

        return (
         dist_table, path_table)

    def construct_global_ts(self):
        logger.debug('Constructing the global TS')
        ts = lomap.Ts()
        ts.name = 'Global TS'
        init_state = (
         self.quad.x, self.quad.y)
        ts.init[init_state] = 1
        for cell in self.env.global_reqs:
            ts.g.add_node(cell, prop=self.env.global_reqs[cell]['reqs'])

        for u, v in it.product(self.env.global_reqs, repeat=2):
            dist = abs(u[0] - v[0]) + abs(u[1] - v[1])
            assert (u == v) != (dist > 0), 'Global requests cannot be co-located.'
            dist = 1 if dist == 0 else dist
            logger.debug('%s -> %s (dist: %s)' % (u, v, dist))
            ts.g.add_edge(u, v, weight=dist, control='N/A', label=dist)

        if init_state not in self.env.global_reqs:
            ts.g.add_node(init_state, prop=set([]))
            for v in self.env.global_reqs:
                dist = abs(init_state[0] - v[0]) + abs(init_state[1] - v[1])
                logger.debug('%s -> %s (dist: %s)' % (init_state, v, dist))
                ts.g.add_edge(init_state, v, weight=dist, control='N/A', label=dist)

        return ts