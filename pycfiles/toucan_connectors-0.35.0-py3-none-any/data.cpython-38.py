# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/micro_strategy/data.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 4450 bytes
from copy import deepcopy
from functools import singledispatch

def get_definition(results):
    dfn = deepcopy(results['result']['definition'])
    attrs = dfn['attributes']
    for attr in dfn['attributes']:
        if 'forms' in attr:
            attr['forms'] = {f:f['name'] for f in attr['forms']}
        dfn['attributes_id'] = {attr:attr['id'] for attr in attrs}
        dfn['attributes'] = {attr:attr['name'] for attr in attrs}
        dfn['metrics_id'] = {m:m['id'] for m in dfn['metrics']}
        dfn['metrics'] = {m:m['name'] for m in dfn['metrics']}
        return dfn


def fill_viewfilter_with_ids(vf, dfn):

    def fill_attribute(attr_name):
        if '@' in attr_name:
            attr_name, form_name = attr_name.split('@')
            try:
                dfn_attr = dfn['attributes'][attr_name]
            except KeyError:
                dfn_attr = dfn['attributes_id'][attr_name]
            else:
                return {'type':'form', 
                 'attribute':{'id': dfn_attr['id']}, 
                 'form':{'id': dfn_attr['forms'][form_name]['id']}}
        try:
            dfn_attr = dfn['attributes'][attr_name]
        except KeyError:
            dfn_attr = dfn['attributes_id'][attr_name]
        else:
            return {'type':'attribute', 
             'id':dfn_attr['id']}

    def fill_metric(metric_name):
        try:
            dfn_metric = dfn['metrics'][metric_name]
        except KeyError:
            dfn_metric = dfn['metrics_id'][metric_name]
        else:
            return {'type':'metric', 
             'id':dfn_metric['id']}

    def fill_constant(constant, data_type):
        data_type = data_type or ('Char' if isinstance(constant, str) else 'Real')
        return {'type':'constant',  'dataType':data_type,  'value':str(constant)}

    @singledispatch
    def visit(_):
        pass

    @visit.register(dict)
    def visit_dict(d):
        for v in d.values():
            visit(v)
        else:
            if 'attribute' in d:
                (d.update)(**fill_attribute(d.pop('attribute')))
            else:
                if 'metric' in d:
                    (d.update)(**fill_metric(d.pop('metric')))
                else:
                    if 'constant' in d:
                        (d.update)(**fill_constant(d.pop('constant'), d.get('dataType')))

    @visit.register(list)
    def visit_list(l):
        for e in l:
            visit(e)

    vf = deepcopy(vf)
    visit(vf)
    return vf


def get_attr_names(data: dict) -> dict:
    """Retrieves attribute names from returned data."""
    row = {}
    for index, col in enumerate(data['result']['definition']['attributes']):
        row[index] = col['name']
    else:
        return row


def get_metric_names(data: dict) -> dict:
    """Retrieves metric names from returned data."""
    row = {}
    for index, col in enumerate(data['result']['definition']['metrics']):
        row[index] = col['name']
    else:
        return row


def flatten_json(json_root: dict, attributes: dict, metrics: dict) -> list:
    """ Entry into recursive function to pull data from JSON based on attributes & metrics."""
    row = {}
    table = []

    def flatten(nodes, attributes, metrics, row, table):
        """ Recursive function that will traverse JSON to flatten data."""
        if isinstance(nodes, dict):
            for node in nodes:
                if node == 'depth':
                    row[attributes[nodes['depth']]] = nodes['element']['name']
                    if nodes['depth'] == len(attributes) - 1:
                        for value in metrics.values():
                            row[value] = nodes['metrics'][value]['rv']
                        else:
                            table.append(row.copy())

                flatten(nodes[node], attributes, metrics, row, table)

        else:
            if isinstance(nodes, list):
                for node in nodes:
                    flatten(node, attributes, metrics, row, table)

    flatten(json_root, attributes, metrics, row, table)
    return table