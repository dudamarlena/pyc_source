# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/graph_utils.py
# Compiled at: 2017-01-24 09:43:53
"""
    graph_utils
    ~~~~~~~~~~~

    Function for network manipulation.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import math, json, igraph

class NetworkBuilder:

    def __init__(self, seqBitManip, use_reverse_complements):
        self.bitManip = seqBitManip
        self.use_reverse_complements = use_reverse_complements

    def areConnected(self, source, target):
        return self.bitManip.areNeighbors(self.bitManip.seqToBits(source), self.bitManip.seqToBits(target))

    def createGenoNet(self, repertoire, sequences, scores):
        network = igraph.Graph()
        network['name'] = repertoire
        network.add_vertices(len(sequences))
        network.vs['escores'] = scores
        network.vs['sequences'] = sequences
        bitseqs = [ self.bitManip.seqToBits(seq) for seq in sequences ]
        edges = [ (i, j) for i in range(len(bitseqs) - 1) for j in range(i + 1, len(bitseqs)) if self.bitManip.areNeighbors(bitseqs[i], bitseqs[j])
                ]
        network.add_edges(edges)
        return network

    def getExternalNeighbors(self, sequence, network):
        all_neighbors = self.bitManip.generateNeighbors(self.bitManip.seqToBits(sequence))
        if self.use_reverse_complements:
            for neighbor in list(all_neighbors):
                rc = self.bitManip.getReverseComplement(neighbor)
                if rc != neighbor and rc in all_neighbors:
                    all_neighbors.remove(neighbor)

        neighbors_within_net = [ self.bitManip.seqToBits(network.vs[neighbor]['sequences']) for neighbor in self.getNeighbors(sequence, network)
                               ]
        if self.use_reverse_complements:
            neighbors_within_net.extend([ self.bitManip.getReverseComplement(neighbor) for neighbor in neighbors_within_net
                                        ])
        extern_neighbors = list(set(all_neighbors) - set(neighbors_within_net))
        return extern_neighbors

    def getAllExtNeighbors(self, network):
        ext_neighbors = set()
        sequences = network.vs['sequences']
        if self.use_reverse_complements:
            ext_neighbors = self.external_neighbors_rc(sequences, network)
        else:
            for sequence in sequences:
                ext_neighbors |= set(self.getExternalNeighbors(sequence, network))

        return list(ext_neighbors)

    def external_neighbors_rc(self, sequences, network):
        external_neighbors = set()
        for sequence in sequences:
            sequence_neighbors = set(self.getExternalNeighbors(sequence, network))
            sequence_neighbors -= external_neighbors & sequence_neighbors
            if sequence_neighbors:
                sequence_neighbors_rc = set([ self.bitManip.getReverseComplement(n) for n in sequence_neighbors
                                            ])
                sequence_neighbors_rc -= external_neighbors & sequence_neighbors_rc
                external_neighbors |= sequence_neighbors_rc

        return external_neighbors

    def getVertex(self, sequence, network):
        try:
            return network.vs.find(sequences=sequence)
        except ValueError:
            print 'Error! ... Non-existent vertex requested: ' + str(sequence)

    def getNeighbors(self, sequence, network):
        return network.neighbors(self.getVertex(sequence, network))

    def plotNetwork(self, network, layout, outPath):
        vertices = [ network.vs[i].index for i in range(0, network.vcount()) ]
        degrees = network.outdegree(vertices)
        visual_style = {}
        visual_style['vertex_size'] = [ x * 10 * x * 10 for x in network.vs['Evolvability']
                                      ]
        layout = network.layout(layout)
        igraph.plot(network, (outPath + network['name'] + '_evonet.svg'), bbox=(1500,
                                                                                1500), **visual_style)

    def getComponents(self, network):
        vertexCluster = network.components()
        return vertexCluster.sizes()

    def getGiantComponent(self, network):
        return network.components().giant()

    def createNeighborhoodNet(self, sequence, network):
        sequences = [
         sequence]
        escores = []
        vertex = self.getVertex(sequence, network)
        neighbors = network.neighbors(vertex)
        escores.append(network.vs[vertex.index]['escores'])
        for neighbor in neighbors:
            sequences.append(network.vs[neighbor]['sequences'])
            escores.append(network.vs[neighbor]['escores'])

        neighborhoodNet = igraph.Graph()
        neighborhoodNet.add_vertices(len(sequences))
        neighborhoodNet.vs['label'] = [ sequences[i] + '\n' + str(escores[i]) for i in range(len(sequences))
                                      ]
        for i in range(1, len(sequences)):
            neighborhoodNet.add_edge(0, i)

        print sequences
        return neighborhoodNet

    def createEvoNet(self, title, genoNets):
        repertoires = [ gn['name'].rpartition('_dominant')[0] if gn['name'].rpartition('_dominant')[0] else gn['name'] for gn in genoNets
                      ]
        evolvability = [ gn['Evolvability'] for gn in genoNets ]
        network = igraph.Graph(directed=True)
        network['name'] = title
        network.add_vertices(len(repertoires))
        labels = [ repertoires[i] + '\n' + str(float(('{0:.2f}').format(evolvability[i]))) for i in range(len(repertoires))
                 ]
        network.vs['label'] = labels
        network.vs['Repertoires'] = repertoires
        network.vs['GenotypeSet'] = repertoires
        network.vs['Evolvability'] = evolvability
        edges = [ (i, j) for i in range(len(repertoires)) for j in range(len(repertoires)) if i != j and self.repertoiresAreConnected(genoNets[i], repertoires[j])
                ]
        network.add_edges(edges)
        repToNetDict = {repertoires[i]:genoNets[i] for i in range(len(repertoires))}
        weights = [ self.getEdgeWeight(edges[i], network, repToNetDict) for i in range(len(edges))
                  ]
        network.es['weight'] = weights
        network.es['label'] = weights
        return network

    def repertoiresAreConnected(self, gn1, rep2):
        areConnected = False
        evoTargets = json.loads(gn1['Evolvability_targets'])
        if evoTargets:
            if rep2 in evoTargets:
                areConnected = True
        return areConnected

    def getEdgeWeight(self, edge, en, repToNetDict):
        srcRep = en.vs[edge[0]]['Repertoires']
        trgRep = en.vs[edge[1]]['Repertoires']
        srcGN = repToNetDict[srcRep]
        allTargets = srcGN.vs['Evolvability_targets']
        extNeighbors = []
        for trgDict in allTargets:
            if trgRep in trgDict:
                extNeighbors.extend(trgDict[trgRep])

        extNeighbors = list(set(extNeighbors))
        return len(extNeighbors)