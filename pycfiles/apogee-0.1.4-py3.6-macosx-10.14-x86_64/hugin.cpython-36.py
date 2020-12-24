# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/io/parsers/hugin.py
# Compiled at: 2019-11-27 14:51:48
# Size of source mod 2**32: 4646 bytes
import re, itertools
from collections import OrderedDict
import numpy as np

def deformat(s):
    s = str(s)
    s = re.sub('\\n', ' ', s)
    s = re.sub('\\t', ' ', s)
    return s


class HuginReader:
    __doc__ = 'Read and build a BayesianNetwork from a HUGIN file.'

    def __init__(self):
        self._data = OrderedDict()

    def write(self, model: 'GraphicalModel', *args, **kwargs):
        """Write a model as a HUGIN-formatted file."""
        raise NotImplementedError('Writing HUGIN models is not yet supported.')

    def read(self, filename: str) -> dict:
        """Read a HUGIN-formatted file as an Apogee BayesianNetwork."""
        with open(filename, 'r') as (file):
            return self.parse(file.read())

    def parse(self, data: str):
        nodes, potentials = self._extract(deformat(data.strip()))
        self.parse_nodes(nodes)
        self.parse_potentials(potentials)
        return self.to_dict()

    def parse_nodes(self, nodes):
        for node in nodes:
            name = node[0].strip()
            self._data[name] = {}
            node_data = [x.strip().split(';') for x in node[1:]][0]
            node_data = [x for x in node_data if len(x) > 0]
            for element in node_data:
                element = element.strip()
                if re.search('(.*) = \\((.*)\\)', element) is not None:
                    element = re.search('(.*) = \\((.*)\\)', element)
                    if element.group(1) == 'states':
                        key = element.group(1)
                        value = element.group(2).replace('"', '').strip().split(' ')
                    if element.group(1) == 'position':
                        key = element.group(1)
                        value = [int(x) for x in element.group(2).replace('"', '').strip().split(' ')]
                else:
                    if re.search('(.*) = \\"(.*)\\"', element) is not None:
                        element = re.search('(.*) = \\"(.*)\\"', element)
                        key, value = element.group(1), element.group(2)
                    else:
                        raise ValueError("Encountered unknown error in parsing element. '{0}'".format(element))
                    self._data[name][key] = value

    def parse_potentials(self, potentials):
        for potential in potentials:
            scope, data = potential
            if re.search('\\((.*)\\|', scope) is not None:
                key = re.search('\\((.*)\\|', scope).group(1).strip()
                parents = re.search('\\|(.*)\\)', scope).group(1).strip()
                parents = [x for x in parents.split(' ') if x is not '']
            else:
                key = re.search('\\((.*)\\)', scope).group(1).strip()
                parents = []
            data = [float(x) for x in re.findall('\\d+\\.\\d+', data)]
            if len(parents) > 0:
                pstates = [self._data[x]['states'] for x in parents]
                m = len(list((itertools.product)(*pstates)))
                n = len(self._data[key]['states'])
                data = np.array(data).reshape((m, n)).flatten('F')
            self._data[key]['parameters'] = data
            self._data[key]['neighbours'] = parents
            if 'position' not in self._data[key].keys():
                self._data[key]['position'] = [
                 0, 0, 0]

    def to_dict(self) -> dict:
        data = {}
        for key, value in self._data.items():
            del value['position']
            data[key] = value

        return data

    def to_extended_dict(self) -> dict:
        nodes = OrderedDict()
        edges = []
        for key, value in self._data.items():
            local = dict(name=key,
              cpt=(value['cpt']),
              states=(value['states']),
              x=(value['position'][0]),
              y=(value['position'][1]),
              z=0)
            for parent in value['neighbours']:
                edge = dict(start=parent, end=key, weight=1.0, d='true')
                edges.append(edge)

            nodes[key] = local

        return {'nodes':nodes,  'edges':edges}

    @staticmethod
    def _extract(data) -> tuple:
        patterns = re.compile('node (.*?) \\{(.+?)\\}')
        nodes = re.findall(patterns, data)
        patterns = re.compile('potential (.*?) \\{(.+?)\\}')
        potentials = re.findall(patterns, data)
        return (nodes, potentials)