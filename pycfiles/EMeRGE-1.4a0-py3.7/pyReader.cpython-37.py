# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\CSV2DSS\pyReader.py
# Compiled at: 2020-01-02 17:26:08
# Size of source mod 2**32: 16368 bytes
"""
Created on Wed Sep 11 1:43:57 2019
@author: kduwadi
"""
import numpy as np, pandas as pd, pathlib, os, networkx as nx, copy, random, math

class Reader:
    code_name = {'consumer_ht.csv':{'code':'N', 
      'type':'Consumer_HT'}, 
     'consumer_lt.csv':{'code':'N', 
      'type':'Consumer_LT'}, 
     'distribution_transformer.csv':{'code':'N', 
      'type':'DTs'}, 
     'ht_cable_attributes.csv':{'code':'L', 
      'type':'HT_cable',  'feature':'Attribute data'}, 
     'ht_cable_nodes.csv':{'code':'L', 
      'type':'HT_cable',  'feature':'Coordinates'}, 
     'ht_line_attributes.csv':{'code':'L', 
      'type':'HT_line',  'feature':'Attribute data'}, 
     'ht_line_nodes.csv':{'code':'L', 
      'type':'HT_line',  'feature':'Coordinates'}, 
     'ht_pole.csv':{'code':'N', 
      'type':'HTpole'}, 
     'lt_cable_attributes.csv':{'code':'L', 
      'type':'LT_cable',  'feature':'Attribute data'}, 
     'lt_cable_nodes.csv':{'code':'L', 
      'type':'LT_cable',  'feature':'Coordinates'}, 
     'lt_line_attributes.csv':{'code':'L', 
      'type':'LT_line',  'feature':'Attribute data'}, 
     'lt_line_nodes.csv':{'code':'L', 
      'type':'LT_line',  'feature':'Coordinates'}, 
     'lt_pole.csv':{'code':'N', 
      'type':'LTpole'}, 
     'power_transformer.csv':{'code':'N', 
      'type':'PTs'}}

    def __init__(self, settings):
        self._Reader__settings = settings
        self.path = os.path.join(self._Reader__settings['Project path'], self._Reader__settings['Feeder name'])
        self.filelists = os.listdir(self.path)
        self.feedername = self._Reader__settings['Feeder name']
        self._Reader__Create_file_dictionary()
        print('\n -------------------------', self.feedername, ' Feeder', '-----------------------------------------')
        self.Line_data = {}
        for Element, FileDict in self.LineFiles.items():
            CoordinateData = pd.read_csv((os.path.join(self.path, FileDict['Coordinates'])), index_col=None)
            AttributeData = pd.read_csv((os.path.join(self.path, FileDict['Attribute data'])), index_col=None)
            self.Line_data[Element] = {'CD':CoordinateData,  'ATD':AttributeData}

        self.Node_data = {}
        for Element, Filepath in self.NodeFiles.items():
            NodeData = pd.read_csv((os.path.join(self.path, Filepath)), index_col=None)
            self.Node_data[Element] = NodeData

        self.NXgraph = nx.Graph()
        if 'HT_line' in self.LineFiles:
            print('Creating HT_edges')
            self._Reader__Add_edge('HT_line', 'HT')
        if 'HT_cable' in self.LineFiles:
            print('Creating HT_Cables')
            self._Reader__Add_edge('HT_cable', 'HT')
        elif 'HT_line' in self.LineFiles or 'HT_cable' in self.LineFiles:
            self._Reader__GetGraphMetrics()
        else:
            print('The network you are trying to build does not seem to have high tension network. Make sure this is correct. If its wrong please abort the program and make sure you have csvs with correct names...!!!')
        if 'LT_line' in self.LineFiles:
            print('Creating LT_edges')
            self._Reader__Add_edge('LT_line', 'LT')
        if 'LT_cable' in self.LineFiles:
            print('Creating LT_Cables')
            self._Reader__Add_edge('LT_cable', 'LT')
        elif not 'DTs' in self.NodeFiles or 'HT_line' in self.LineFiles or 'HT_cable' in self.LineFiles:
            self._Reader__add_distribution_transformers()
        else:
            print('Distribution transformers are used to connect HT and LT network , without HT network program can not utillize distribution_transformer.csv: if this is substation transformer please make sure you include this in power_transformer.csv')
        if 'LT_line' in self.LineFiles or 'LT_cable' in self.LineFiles:
            self._Reader__GetGraphMetrics()
        else:
            print('The network you are trying to build does not seem to have low tension network. Make sure this is correct. If its wrong please abort the program and make sure you have csvs with correct names...!!!')
            if 'HT_line' not in self.LineFiles and 'HT_cable' not in self.LineFiles:
                assert False, 'There is no network build upto this point: make sure files are named correctly or check if folder is empty'
            elif 'PTs' in self.NodeFiles:
                self._Reader__add_power_transformers()
            else:
                print('Caution: This network does not seem to have power transformers !!!')
            if 'Consumer_LT' in self.NodeFiles:
                print('Adding LT customers to network')
                self._Reader__add__loads(self.Node_data['Consumer_LT'], 'LT')
            if 'Consumer_HT' in self.NodeFiles:
                print('Adding HT customers to network')
                self._Reader__add__loads(self.Node_data['Consumer_HT'], 'HT')
            self._Reader__GetGraphMetrics()
            print('Successfully build the ', self.feedername, ' Feeder !!!!!!')

    def __Create_file_dictionary(self):
        self.LineFiles = {}
        self.NodeFiles = {}
        for i in range(len(self.filelists)):
            this_dict = self.code_name[self.filelists[i]]
            if this_dict['code'] == 'N':
                self.NodeFiles[this_dict['type']] = self.filelists[i]
            elif this_dict['type'] not in self.LineFiles:
                self.LineFiles[this_dict['type']] = {}
                self.LineFiles[this_dict['type']][this_dict['feature']] = self.filelists[i]
            else:
                self.LineFiles[this_dict['type']][this_dict['feature']] = self.filelists[i]

    def __Add_edge(self, tag, acronym):
        cData = self.Line_data[tag]['CD']
        aData = self.Line_data[tag]['ATD']
        D = len(aData)
        for i in range(D):
            AttData = aData.loc[i]
            shapeID = AttData['shapeid']
            ElmCoordinateData = cData[(cData['shapeid'] == shapeID)]
            ElmCoordinateData.index = range(len(ElmCoordinateData))
            X1 = ElmCoordinateData['x'][0]
            X2 = ElmCoordinateData['x'][(len(ElmCoordinateData) - 1)]
            Y1 = ElmCoordinateData['y'][0]
            Y2 = ElmCoordinateData['y'][(len(ElmCoordinateData) - 1)]
            Attributes = {'Type':tag, 
             'Length':AttData['length'], 
             'Phase_con':AttData['phase'], 
             'Cable size phase':AttData['csize'], 
             'num_of_cond':AttData['num_of_cond'], 
             'Cable type phase':AttData['cname'], 
             'spacing':AttData['spacing'], 
             'units':AttData['units']}
            if 'nname' in AttData:
                Attributes['Cable type neutral'] = AttData['nname']
                Attributes['Cable size neutral'] = AttData['nsize']
            (self.NXgraph.add_edge)(('{}_{}_{}'.format(X1, Y1, acronym)), ('{}_{}_{}'.format(X2, Y2, acronym)), **Attributes)
            self.NXgraph.node['{}_{}_{}'.format(X1, Y1, acronym)]['x'] = X1
            self.NXgraph.node['{}_{}_{}'.format(X1, Y1, acronym)]['y'] = Y1
            self.NXgraph.node['{}_{}_{}'.format(X1, Y1, acronym)]['Type'] = acronym + 'node'
            self.NXgraph.node['{}_{}_{}'.format(X2, Y2, acronym)]['x'] = X2
            self.NXgraph.node['{}_{}_{}'.format(X2, Y2, acronym)]['y'] = Y2
            self.NXgraph.node['{}_{}_{}'.format(X2, Y2, acronym)]['Type'] = acronym + 'node'

    def __GetGraphMetrics(self):
        self.Islands = list(nx.connected_component_subgraphs(self.NXgraph))
        self.NumIslands = len(self.Islands)
        self.Loops = nx.cycle_basis(self.NXgraph)
        if self.NumIslands > 1:
            print('Caution: the network upto this point has {} islands: running inbuilt algorithm to fix island issue'.format(self.NumIslands))
            self._Reader__fix_network_islands()
            assert len(list(nx.connected_component_subgraphs(self.NXgraph))) == 1, 'Especial error -- > The inbuilt algorithm is not able to successully fix issue of islands: Please consult with NREL team ro fix this !!!'
        return

    def __fix_network_islands(self):
        self.Islands = list(nx.connected_component_subgraphs(self.NXgraph))
        for i in range(len(self.Islands) - 1):
            D = 99999999
            for node1 in self.Islands[0].nodes():
                X0 = self.Islands[0].node[node1]['x']
                Y0 = self.Islands[0].node[node1]['y']
                for k in range(len(self.Islands)):
                    if k != 0:
                        for node2 in self.Islands[k].nodes():
                            X1 = self.Islands[k].node[node2]['x']
                            Y1 = self.Islands[k].node[node2]['y']
                            if np.sqrt((X0 - X1) ** 2 + (Y0 - Y1) ** 2) < D and self.NXgraph.nodes[node2]['Type'] == self.NXgraph.nodes[node1]['Type']:
                                D = np.sqrt((X0 - X1) ** 2 + (Y0 - Y1) ** 2)
                                N1 = node1
                                N2 = node2

            self.NXgraph = nx.contracted_nodes(self.NXgraph, N1, N2)
            self.Islands = list(nx.connected_component_subgraphs(self.NXgraph))

    def __add_distribution_transformers(self):
        print('Adding distribution transformers')
        typeData = self.Node_data['DTs']
        for i in range(len(typeData)):
            transData = typeData.loc[i]
            ElmDict = transData.to_dict()
            ElmDict['Type'] = 'DTs'
            X0, Y0 = transData['x'], transData['y']
            dist_from_ht_node, dist_from_lt_node, nearest_ht_node, nearest_lt_node = (99999999,
                                                                                      99999999,
                                                                                      None,
                                                                                      None)
            for Node in self.NXgraph.nodes():
                X1 = self.NXgraph.node[Node]['x']
                Y1 = self.NXgraph.node[Node]['y']
                if self.NXgraph.node[Node]['Type'] == 'HTnode':
                    if np.sqrt((X1 - X0) ** 2 + (Y1 - Y0) ** 2) < dist_from_ht_node:
                        dist_from_ht_node = np.sqrt((X1 - X0) ** 2 + (Y1 - Y0) ** 2)
                        nearest_ht_node = Node
                    elif self.NXgraph.node[Node]['Type'] == 'LTnode' and np.sqrt((X1 - X0) ** 2 + (Y1 - Y0) ** 2) < dist_from_lt_node:
                        dist_from_lt_node = np.sqrt((X1 - X0) ** 2 + (Y1 - Y0) ** 2)
                        nearest_lt_node = Node

            (self.NXgraph.add_edge)(nearest_ht_node, nearest_lt_node, **ElmDict)

    def __add_power_transformers(self):
        print('Adding power transformers')
        typeData = self.Node_data['PTs']
        transData = typeData.loc[0]
        ElmDict = transData.to_dict()
        ElmDict['Type'] = 'PTs'
        X0, Y0, dist_from_ht, node_of_interest = (self.Node_data['PTs'].x[0], self.Node_data['PTs'].y[0], 9999999, None)
        for Node in self.NXgraph.nodes():
            if self.NXgraph.node[Node]['Type'] == 'HTnode':
                X1 = self.NXgraph.node[Node]['x']
                Y1 = self.NXgraph.node[Node]['y']
                if np.sqrt((X0 - X1) ** 2 + (Y0 - Y1) ** 2) < dist_from_ht:
                    dist_from_consumer_ht = np.sqrt((X0 - X1) ** 2 + (Y0 - Y1) ** 2)
                    node_of_interest = Node

        (self.NXgraph.add_edge)(('{}_{}_EHT'.format(X0, Y0)), node_of_interest, **ElmDict)
        self.NXgraph.node['{}_{}_EHT'.format(X0, Y0)]['x'] = X0
        self.NXgraph.node['{}_{}_EHT'.format(X0, Y0)]['y'] = Y0
        self.NXgraph.node['{}_{}_EHT'.format(X0, Y0)]['Type'] = 'EHTnode'

    def __add__loads(self, con_data, tag):
        for i in range(len(con_data)):
            X0, Y0 = con_data.x[i], con_data.y[i]
            dist_from_consumer_lt, node_of_interest = (9999999, None)
            for Node in self.NXgraph.nodes():
                if self.NXgraph.node[Node]['Type'] == tag + 'node':
                    X1 = self.NXgraph.node[Node]['x']
                    Y1 = self.NXgraph.node[Node]['y']
                    if np.sqrt((X0 - X1) ** 2 + (Y0 - Y1) ** 2) < dist_from_consumer_lt:
                        dist_from_consumer_lt = np.sqrt((X0 - X1) ** 2 + (Y0 - Y1) ** 2)
                        node_of_interest = Node

            if con_data.phase[i] != self._Reader__settings['three_phase']:
                if self._Reader__settings['random_phase_allocation'] == 'yes' and tag == 'LT':
                    phase = random.choice(self._Reader__settings['single_phase'])
                else:
                    phase = con_data.phase[i]
            else:
                line_type = 'Service_line' if tag == 'LT' else tag + '_line'
                phase_conductor_type = self._Reader__settings['servicewire_phase_conductor_type'] if tag == 'LT' else self._Reader__settings['phase_conductor_type_ht_consumer']
                phase_conductor_size = self._Reader__settings['servicewire_phase_conductor_size'] if tag == 'LT' else self._Reader__settings['phase_conductor_size_ht_consumer']
                if phase != 'RYB':
                    num_of_cond = self._Reader__settings['service_wire_num_of_cond']['single_phase']
                else:
                    num_of_cond = self._Reader__settings['service_wire_num_of_cond']['three_phase'] if tag == 'LT' else self._Reader__settings['ht_consumer_conductor_num_of_cond']['three_phase']
            spacing = self._Reader__settings['service_wire_spacing'] if tag == 'LT' else self._Reader__settings['ht_consumer_conductor_spacing']
            Attributes = {'Type':line_type, 
             'Phase_con':phase, 
             'Length':dist_from_consumer_lt, 
             'num_of_cond':num_of_cond, 
             'Cable size phase':phase_conductor_size, 
             'Cable type phase':phase_conductor_type, 
             'spacing':spacing, 
             'units':self._Reader__settings['units_for_coordinate']}
            (self.NXgraph.add_edge)(('{}_{}_{}'.format(X0, Y0, tag)), node_of_interest, **Attributes)
            self.NXgraph.node['{}_{}_{}'.format(X0, Y0, tag)]['x'] = X0
            self.NXgraph.node['{}_{}_{}'.format(X0, Y0, tag)]['y'] = Y0
            self.NXgraph.node['{}_{}_{}'.format(X0, Y0, tag)]['Type'] = 'STnode' if tag == 'LT' else 'HTnode'
            NodeData = self.NXgraph.node['{}_{}_{}'.format(X0, Y0, tag)]
            if 'loads' not in NodeData:
                NodeData['loads'] = {}
            NodeData['loads'][con_data.ID[i]] = {'kw':con_data.kw[i], 
             'pf':con_data.pf[i], 
             'phase':phase, 
             'kv':con_data.kv[i], 
             'tec':con_data.tec[i], 
             'con_type':con_data.cust_type[i], 
             'load_type':con_data.load_type[i]}