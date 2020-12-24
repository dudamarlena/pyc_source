# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/KyunghoonKim/anaconda/lib/python2.7/site-packages/pynetviz/linkurious.py
# Compiled at: 2015-10-20 21:35:23
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


def make_html(url='../src/iframe/pylinkurious.html', filename='./NetworkX_Graph.html'):
    html = '\n<!DOCTYPE html>\n<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n  <meta charset="utf-8">\n  <meta http-equiv="X-UA-Compatible" content="IE=edge">\n  <title>PyLinkurious</title>\n  <meta name="description" content="">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body>\n\n  <iframe name="pylinkurious-iframe"\n    src="$url?cb=setUpFrame"\n    width="100%"\n    height="500"\n    frameborder="0"\n    webkitallowfullscreen mozallowfullscreen allowfullscreen>\n  </iframe>\n\n  <script>\n  // Function called once the iframe is initialized:\n  function setUpFrame() {\n\n    // Get Linkurious.js instance:\n    var LK = window.frames[\'pylinkurious-iframe\'].LK;\n\n    // Update UI components\n    LK.updateUI();\n\n    // Load a graph sample:\n    LK.sigma.graph.read({\n      nodes: [\n        { id: \'n0\', label: \'Node 0\', x: 0, y: 0, size: 1 },\n        { id: \'n1\', label: \'Node 1\', x: 50, y: -10, size: 1 }\n      ],\n      edges: [\n        {\n          id: \'e0\',\n          label: \'Edge 0\',\n          source: \'n0\',\n          target: \'n1\',\n          size: 1\n        }\n      ]\n    });\n\n    // Display the graph:\n    LK.sigma.refresh();\n    LK.plugins.locate.center();\n\n    console.log(\'nb nodes\', LK.sigma.graph.nodes().length);\n  }\n\n  </script>\n</body>\n</html>\n    '
    s = Template(html).safe_substitute(url=url)
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