# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sewergraph\cost_estimates.py
# Compiled at: 2019-07-31 17:17:24
# Size of source mod 2**32: 2076 bytes
from .hhcalculations import replacement_sewer_size
from sewergraph.save_load import gdf_from_graph
circular_unit_costs = {12:570,  18:570,  21:610,  24:680,  27:760,  30:860,  36:1020, 
 42:1200,  48:1400,  54:1550,  60:1700,  66:1960, 
 72:2260,  84:2600,  90:3000}
rect_cost_per_sqft = 80

def replacements_for_capacity(G, enforced_cap_frac=1.0):
    """
    for undersized sewers with capacity fractions greater than the
    enforced_cap_frac, calculate what replacement sewer is required.
    """
    for u, v, d in G.edges(data=True):
        if d.get('capacity_fraction', 0) > enforced_cap_frac:
            q = d['peakQ']
            slope = d['slope_used_in_calcs']
            diam, h, w, capacity = replacement_sewer_size(q, slope)
            if diam is not None:
                unit_cost = circular_unit_costs.get(diam, 3000)
            else:
                unit_cost = h * w * rect_cost_per_sqft / 144.0
            total_cost = unit_cost * d['length']
            d['replacement_diam'] = diam
            d['replacement_h'] = h
            d['replacement_w'] = w
            d['replacement_capacity'] = capacity
            d['replacement_unit_cost_per_ft'] = unit_cost
            d['replacement_cost'] = total_cost
        else:
            d.pop('replacement_diam', None)
            d.pop('replacement_h', None)
            d.pop('replacement_w', None)
            d.pop('replacement_capacity', None)
            d.pop('replacement_unit_cost_per_ft', None)
            d.pop('replacement_cost', None)


def estimate_sewer_replacement_costs(G, target_cap_frac=1.0):
    """
    calculate the required replacement size of all sewers to meet the
    target_cap_frac
    """
    replacements_for_capacity(G, target_cap_frac)
    df = gdf_from_graph(G, return_type='edges')
    millions = df[(df.replacement_cost > 0)].replacement_cost.sum() / 1000000
    return millions