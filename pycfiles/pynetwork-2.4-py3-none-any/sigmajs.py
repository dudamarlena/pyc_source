# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/KyunghoonKim/anaconda/lib/python2.7/site-packages/pynetviz/sigmajs.py
# Compiled at: 2015-11-01 11:34:56
import random
from string import Template
from IPython.display import display, HTML
import networkx as nx
__author__ = 'Kyunghoon Kim'
__version__ = '0.1.0'
__email__ = 'kyunghoon@unist.ac.kr'

def node_info(G, node_name, alpha=0.6, r=0, g=0, b=204, x=0, y=0, size=1):
    """Allocate a attribute of each node.
    
    Parameters
    ----------
    G: networkx.classes.graph.Graph
        Graph
    node_name: string or int
        Node Label
    alpha: float
        Transparent
    r: int
        Red of RGB
    g: int
        Green of RGB
    b: int
        Blue of RGB
    x: float
        position of x-axis
    y: float
        position of y-axis
    size: float
        size of node
    """
    if x == 0:
        x = random.random()
    if y == 0:
        y = random.random()
    G.node[node_name]['label'] = node_name
    G.node[node_name]['viz'] = {'color': {'a': alpha, 'r': r, 'g': g, 'b': b}, 'position': {'x': x, 'y': y, 'z': 0.0}, 'size': size}
    return G


def make_html(drawEdges, gexfname='./NetworkX_Graph.gexf', filename='./NetworkX_Graph.html'):
    html = '\n<!-- START SIGMA IMPORTS -->\n<script src="https://rawgit.com/Linkurious/linkurious.js/develop/dist/sigma.min.js"></script>\n<!-- END SIGMA IMPORTS -->\n<script src="https://cdn.rawgit.com/Linkurious/linkurious.js/develop/plugins/sigma.parsers.gexf/gexf-parser.js"></script>\n<script src="https://cdn.rawgit.com/Linkurious/linkurious.js/develop/plugins/sigma.parsers.gexf/sigma.parsers.gexf.js"></script>\n<div id="container">\n  <style>\n    #graph-container {\n      top: 0;\n      bottom: 0;\n      left: 0;\n      right: 0;\n      position: absolute;\n    }\n  </style>\n  <div id="graph-container"></div>\n</div>\n<script>\n/**\n * Here is just a basic example on how to properly display a graph\n * exported from Gephi in the GEXF format.\n *\n * The plugin sigma.parsers.gexf can load and parse the GEXF graph file,\n * and instantiate sigma when the graph is received.\n *\n * The object given as the second parameter is the base of the instance\n * configuration object. The plugin will just add the "graph" key to it\n * before the instanciation.\n */\nsigma.parsers.gexf(\'$gexfname\', {\n  container: \'graph-container\',\n  settings: {\n    drawEdges: $drawEdges\n  }\n}, 1);\n</script>\n    '
    s = Template(html).safe_substitute(drawEdges=drawEdges, gexfname=gexfname)
    HTMLfile = open(filename, 'w')
    HTMLfile.write(s)
    HTMLfile.close()


def make_gexf(G, layout=None, size=None, filename='./NetworkX_Graph.gexf'):
    if layout and size:
        for node in G.nodes():
            G = node_info(G, node, size=size[node], x=layout[node][0], y=layout[node][1])

    elif layout and not size:
        for node in G.nodes():
            G = node_info(G, node, x=layout[node][0], y=layout[node][1])

    elif not layout and size:
        for node in G.nodes():
            G = node_info(G, node, size=size[node])

    else:
        for node in G.nodes():
            G = node_info(G, node)

    nx.write_gexf(G, filename)


def view_html(filename='./NetworkX_Graph.html', height=500):
    """Display the html file.
    
    Parameters
    ----------
    filename: string
        location of html file
    height: int
        height of iframe
    """
    html = '<iframe name="pylinkurious-iframe"\n    src="$filename"\n    width="100%"\n    height="$height"\n    frameborder="0"\n    webkitallowfullscreen mozallowfullscreen allowfullscreen>\n    </iframe>'
    s = Template(html).safe_substitute(filename=filename, height=height)
    display(HTML(s))