# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sewergraph\core.py
# Compiled at: 2019-07-31 17:17:24
# Size of source mod 2**32: 15409 bytes
import networkx as nx
from .helpers import pairwise, get_node_values
from .hhcalculations import philly_storm_intensity

def hydrologic_calcs_on_sewers(G, nbunch=None, return_period=0):
    G1 = G.copy()
    for u, v, d in G1.edges(data=True, nbunch=nbunch):
        split_frac = d.get('flow_split_frac', 1)
        direct_ac = G1[u][v].get('local_area', 0) / 43560.0 * split_frac
        acres = G1.node[u]['cumulative_area'] * split_frac / 43560.0 + direct_ac
        C = G1.node[u].get('runoff_coefficient', 0.85)
        Cwt = G1.node[u].get('runoff_coefficient_weighted', 0.85)
        G1.node[u]['runoff_coefficient'] = C
        tc_path = G1.node[u]['tc_path']
        tc = G1.node[u]['tc']
        intensity = philly_storm_intensity(tc, return_period)
        peakQ = Cwt * intensity * acres
        d['upstream_area_ac'] = acres
        d['local_area_ac'] = direct_ac
        d['tc_path'] = tc_path
        d['tc'] = tc
        d['intensity'] = intensity
        d['peakQ'] = peakQ
        d['runoff_coefficient'] = C
        d['runoff_coefficient_weighted'] = Cwt
        d['CA'] = G1.node[u].get('CA', None)
        d['capacity_fraction'] = peakQ / max(d['capacity'], 1.0)
        d['capacity_per_ac'] = d['capacity'] / max(acres, 0.1)
        d['up_node'] = u
        d['dn_node'] = v

    return G1


def accumulate_downstream(G, accum_attr='local_area', cumu_attr_name=None, split_attr='flow_split_frac'):
    """
    pass through the graph from upstream to downstream and accumulate the value
    an attribute found in nodes and edges, and assign the accumulated value
    as a new attribute in each node and edge.

    Where there's a flow split, apply an optional split fraction to
    coded in the upstream edge.
    """
    G1 = G.copy()
    if cumu_attr_name is None:
        cumu_attr_name = 'cumulative_{}'.format(accum_attr)
    for n in nx.topological_sort(G1):
        attrib_val = G1.node[n].get(accum_attr, 0)
        for p in G1.predecessors(n):
            attrib_val += G1.node[p][cumu_attr_name] * G1[p][n].get(split_attr, 1)
            attrib_val += G1[p][n].get(accum_attr, 0)
            G1[p][n][cumu_attr_name] = attrib_val

        G1.node[n][cumu_attr_name] = attrib_val

    return G1


def propogate_weighted_C(G, gsi_capture={}):
    """
    loop through each node and propogate the weighted C from the top to bottom
    of the shed. where there's a flow split, apply the split fraction to
    coded in the upstream edge (based on relative sewer capacity).
    """
    G1 = G.copy()
    for n in nx.topological_sort(G1):
        area = sum(get_node_values(G1, [n], ['local_area', 'additional_area']))
        C = G1.node[n].get('runoff_coefficient', 0.85)
        area = area / 43560.0
        CA = C * area
        G1.node[n]['runoff_coefficient'] = C
        for p in G1.predecessors(n):
            pred = G1.node[p]
            CA += pred['CA'] * G1[p][n].get('flow_split_frac', 1.0)
            CA += G1[p][n].get('local_area', 0) * G1[p][n].get('runoff_coefficient', 0.85)

        node = G1.node[n]
        node['CA'] = CA
        if n in gsi_capture:
            frac = gsi_capture[n]['fraction']
            gsi_C = gsi_capture[n]['C']
            tot_area = node['cumulative_area']
            CA = (1.0 - frac) * tot_area * C + frac * tot_area * gsi_C
            node['CA'] = CA
            node['GSI Capture'] = gsi_capture[n]
        if node['cumulative_area'] > 0:
            node['runoff_coefficient_weighted'] = CA / node['cumulative_area']
        else:
            node['runoff_coefficient_weighted'] = C

    return G1


def accumulate_travel_time(G):
    """
    loop through each node and accumulate the travel time with its immediate
    upstream nodes and edges. where there are multiple precedessors, choose the
    upstream node + edge pair with the maximum travel time.

    while traversing the topologically sorted network, accumulate the list of
    upstream tc nodes for each subsequent node. This builds the tc_path param so
    we don't have to do any further tc computation.
    """
    G1 = G.copy()
    for n, d in G1.nodes(data=True):
        if G1.in_degree(n) == 0 and 'tc' not in d:
            d['tc'] = 3
            d['tc_path'] = n

    for n in nx.topological_sort(G1):
        tc = sum(get_node_values(G1, [n], ['tc']))
        path = get_node_values(G1, [n], ['tc_path'])
        upstream_tc_options = [(G1[p][n]['travel_time'] + G1.node[p]['tc'], G1.node[p]['tc_path']) for p in G1.predecessors(n)]
        if len(upstream_tc_options) > 0:
            upstream_tc_options.sort(reverse=True)
            tc += upstream_tc_options[0][0]
            path += upstream_tc_options[0][1] + [n]
        G1.node[n]['tc'] = tc
        G1.node[n]['tc_path'] = path

    return G1


def analyze_downstream(G, nbunch=None, in_place=False, terminal_nodes=None, parameter='capacity_per_ac'):
    """
    Assign terminal nodes to each node in the network, then find the limiting
    sewer reach between each node and its terminal node.
    """
    if not in_place:
        G1 = G.copy()
    else:
        G1 = G
    if terminal_nodes is None:
        terminal_nodes = [n for n, d in G1.out_degree() if d == 0]
    for tn in terminal_nodes:
        G1.node[tn]['limiting_rate'] = 9999
        G1.node[tn]['limiting_sewer'] = None
        for p in G1.predecessors(tn):
            edge = G1[p][tn]
            if isinstance(edge, nx.classes.coreviews.AtlasView):
                for fid, ed in edge.items():
                    ed['limiting_rate'] = ed[parameter]

            else:
                G1[p][tn]['limiting_rate'] = G1[p][tn][parameter]

    for n in list(reversed(list(nx.topological_sort(G1)))):
        dn_node_rates = [(G1.node[s]['limiting_rate'], G1.node[s]['limiting_sewer']) for s in G1.successors(n)]
        dn_edge_rates = [(G1[n][s][parameter], G1[n][s]['facilityid']) for s in G1.successors(n)]
        dn_rates = dn_node_rates + dn_edge_rates
        if len(dn_rates) > 0:
            sorted_rates = sorted(dn_rates)
            rate, fid = sorted_rates[0]
            G1.node[n]['limiting_rate'] = rate
            G1.node[n]['limiting_sewer'] = fid
            for s in G1.successors(n):
                G1[n][s]['limiting_rate'] = rate
                G1[n][s]['limiting_sewer'] = fid

    return G1


def assign_inflow_ratio(G, inflow_attr='TotalInflowV'):
    """
    find junctions with multiple inflows and assign relative
    contribution ratios to each upstream edge, based on the
    ratio of the inflow_attr.

    This assumes the inflow_attr is a node attribute that needs
    to be assigned to each edge
    """
    G2 = G.copy()
    for n, inflow in G2.nodes(data=inflow_attr):
        for s in G2.successors(n):
            G2[n][s][inflow_attr] = inflow

    junction_nodes = [n for n, d in G2.in_degree() if d > 1]
    for j in junction_nodes:
        inflows = [inflow for _, _, inflow in G2.in_edges(j, data=inflow_attr)]
        total = sum([_f for _f in inflows if _f])
        for u, v, inflow in G2.in_edges(j, data=inflow_attr):
            G2[u][v]['relative_contribution'] = 1
            if total != 0:
                G2[u][v]['relative_contribution'] = float(inflow) / float(total)

    return G2


def relative_outfall_contribution(G):
    """
    calculate the relative contribution of node J to each
    downstream outfall. This function creates a dictionary of
    outfalls and relative contributions within each node of
    the graph, G.
    """
    G1 = G.copy()
    for tn in [n for n, d in G1.out_degree() if d == 0]:
        G1.node[tn]['outfall_contrib'] = {tn: 1.0}
        for p in G1.predecessors(tn):
            G1[p][tn]['outfall_contrib'] = {tn: 1.0}

    G1inv = G1.reverse()
    for j in nx.topological_sort(G1inv):
        of_contrib_j = G1inv.node[j].get('outfall_contrib', {})
        G1inv.node[j]['outfall_contrib'] = of_contrib_j
        for s in G1inv.predecessors(j):
            of_contrib_sj = G1inv[s][j].get('outfall_contrib', {})
            G1inv[s][j]['outfall_contrib'] = of_contrib_j
            S = G1inv.node[s]
            for OF, w_SOF in list(S['outfall_contrib'].items()):
                w_JOF = w_SOF * G1inv[s][j].get('relative_contribution', 1)
                of_contrib_j.update({OF: w_JOF})

            G1inv.node[j]['outfall_contrib'].update(of_contrib_j)
            G1inv[s][j]['outfall_contrib'].update(of_contrib_j)

    return G1inv.reverse()


def analyze_flow_splits(G, split_frac_attr='capacity'):
    """
    loop through nodes, find nodes with more than 1 outflow (flow split)
    tag the immediately downstream edges as flow splitters and calculate a
    flow split ratio to apply to each of the downstream edges.
    """
    G1 = G.copy()
    splitters = [(n, deg) for n, deg in G1.out_degree() if deg > 1]
    for splitter, out_degree in splitters:
        dwn_edges = [(splitter, dn) for dn in G1.successors(splitter)]
        G1.node[splitter]['flow_split'] = splitter
        G1.node[splitter]['flow_split_edges'] = dwn_edges
        total_capacity = max(sum([G1[u][v][split_frac_attr] for u, v in dwn_edges]), 1)
        for u, v in dwn_edges:
            G1[u][v]['flow_split'] = 'Y'
            if G1.in_degree(u) == 0:
                G1[u][v]['flow_split'] = 'summet'
                G1.node[u]['flow_split'] = 'summet'
            G1[u][v]['flow_split_frac'] = G1[u][v][split_frac_attr] / total_capacity

    return G1


def map_to_lower_res_graph(G1, G2, rm_nodes=None, return_agg=False):
    """
    given a skeletonized graph G2 benchmarked to a baseline
    graph G1, generate a map of nodes removed from G1 to their closest
    nodes in G2
    """
    node_map = {}
    agg_map = {}
    if rm_nodes is None:
        rm_nodes = [n for n in G1 if n not in G2]
    else:
        if any([n not in G1 for n in rm_nodes]):
            raise 'WHOA rm_node not found in G1'
    for n in rm_nodes:
        found_dn = 0
        searched_count = 0
        for dn in nx.dfs_preorder_nodes(G1, n):
            searched_count += 1
            if dn in G2:
                node_map.update({n: dn})
                agg_map.setdefault(dn, set()).add(n)
                found_dn += 1
                break

        if found_dn == 0:
            node_map.update({n: 'UNMATCHED'})
            agg_map.setdefault('UNMATCHED', set()).add(n)

    if return_agg:
        return agg_map
    return node_map


def find_edge(G, facilityid):
    """find an edge given a facilityid"""
    for u, v, fid in G.edges(data='facilityid'):
        if fid == facilityid:
            return (
             u, v)


def set_flow_direction(G1, out):
    """
    THATS THE ONEEEEEEE BOIIIIII
    """
    H1 = G1.to_undirected()
    rev_edges = []
    for n in H1.nodes():
        if nx.has_path(H1, n, out):
            for path in nx.shortest_simple_paths(H1, n, out):
                for u, v in list(pairwise(path)):
                    if G1.has_edge(u, v) is False:
                        rev_edges.append((v, u))

    G2 = G1.copy()
    for u, v in set(rev_edges):
        d = G2[u][v].copy()
        G2.remove_edge(u, v)
        G2.add_edge(v, u)
        for k, val in list(d.items()):
            G2[v][u][k] = val

    return G2