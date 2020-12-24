# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/spread.py
# Compiled at: 2020-04-04 10:01:37
# Size of source mod 2**32: 9319 bytes
from __future__ import absolute_import
from __future__ import print_function
from xml.dom import minidom, Node
import os, json
from numpy import *
import networkx as nx
from networkx.readwrite import json_graph
import codecs, six

class Spread:

    def __init__(self, graphobj, outdir='.', encoding='utf-8'):
        self.g = graphobj
        self.nxg = nx.MultiDiGraph()
        self.outdir = outdir
        self.encoding = encoding
        self.create_tree()
        nx.write_graphml((self.nxg), (os.path.join(outdir, 'spread.graphml')), encoding=encoding)
        nx.write_gml(self.nxg, os.path.join(outdir, 'spread.gml'))
        nl = json_graph.node_link_data(self.nxg)
        with open(os.path.join(outdir, 'spread.json'), 'w') as (f):
            json.dump(nl, f)

    def create_tree(self):
        """
        Generates a unambiguous spread tree by selecting the most likely infector for each site
        """
        for n in self.g.epipath:
            infected = self.g.site_dict[n[1]]
            infectors = n[(-1)]
            self.nxg.add_node((n[1]), name=(infected.sitename), time=(n[0]))
            for i, c in six.iteritems(infectors):
                self.nxg.add_edge((n[1]), (i.geocode), weight=(float(c)))

    def writeGML(self, tree, outdir, encoding, fname='spreadtree.gml'):
        """
        Save the tree in the GML format
        """
        try:
            os.chdir(outdir)
        except:
            pass

        dir(self)
        f = codecs.open(fname, 'w', encoding)
        f.writelines(['Creator "Epigrass"\n',
         'Version ""\n',
         'graph\n[\n',
         '\thierarchic\t1\n\tlabel\t"Spread Tree"\n\tdirected\t1\n'])
        Spread.writeENGML(f, tree)
        f.write(']')
        f.close()
        print('Wrote %s' % fname)

    writeGML = classmethod(writeGML)

    def writeENGML(self, fobj, tree):
        """
        Write the edges and Nodes section of a GML file
        """
        f = fobj
        nodes = dict([(i[1], n) for n, i in enumerate(tree)])
        for n, k in enumerate(six.iterkeys(nodes)):
            nodes[k] = n

        for i, n in six.iteritems(nodes):
            f.writelines(['\tnode\n', '\t[\n'])
            f.writelines(['\t\tid\t%s\n' % n, '\t\tlabel\t"%s"\n' % i])
            f.writelines(['\t\tgraphics\n', '\t\t[\n', '\t\t\tw\t60\n', '\t\t\th\t30\n'])
            f.writelines(['\t\t\ttype\t"roundrectangle"\n', '\t\t\tfill\t"#FFCC00"\n', '\t\t\toutline\t"#000000"\n', '\t\t]\n'])
            f.writelines(['\t\tLabelGraphics\n', '\t\t[\n', '\t\t\ttext\t"%s"\n' % i, '\t\t\tfontSize\t13\n', '\t\t\tfontName\t"Dialog"\n', '\t\t\tanchor\t"c"\n', '\t\t]\n', '\t]\n'])

        for n, i in enumerate(tree):
            lab = str(i[0])
            tid = nodes[i[1]]
            try:
                sid = nodes[i[2]]
            except KeyError:
                continue

            f.writelines(['\tedge\n', '\t[\n'])
            f.writelines(['\t\tsource\t%s\n' % sid, '\t\ttarget\t%s\n' % tid, '\t\tlabel\t"%s"\n' % lab, '\t\tgraphics\n', '\t\t[\n'])
            f.writelines(['\t\t\tfill\t"#000000"\n', '\t\t\ttargetArrow\t"standard"\n', '\t\t]\n', '\t]\n'])

    writeENGML = classmethod(writeENGML)