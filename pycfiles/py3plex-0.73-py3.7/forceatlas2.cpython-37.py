# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/fa2/forceatlas2.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 11095 bytes
import random, time, numpy, scipy
from tqdm import tqdm
from . import fa2util

class Timer:

    def __init__(self, name='Timer'):
        self.name = name
        self.start_time = 0.0
        self.total_time = 0.0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.total_time += time.time() - self.start_time

    def display(self):
        print(self.name, ' took ', '%.2f' % self.total_time, ' seconds')


class ForceAtlas2:

    def __init__--- This code section failed: ---

 L.  68         0  LOAD_FAST                'linLogMode'
                2  LOAD_FAST                'adjustSizes'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    30  'to 30'
               12  LOAD_FAST                'multiThreaded'
               14  DUP_TOP          
               16  ROT_THREE        
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_CONST               False
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_TRUE     40  'to 40'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            10  '10'
               30  POP_TOP          
             32_0  COME_FROM            28  '28'
               32  LOAD_GLOBAL              AssertionError
               34  LOAD_STR                 'You selected a feature that has not been implemented yet...'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            26  '26'

 L.  69        40  LOAD_FAST                'outboundAttractionDistribution'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               outboundAttractionDistribution

 L.  70        46  LOAD_FAST                'linLogMode'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               linLogMode

 L.  71        52  LOAD_FAST                'adjustSizes'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               adjustSizes

 L.  72        58  LOAD_FAST                'edgeWeightInfluence'
               60  LOAD_FAST                'self'
               62  STORE_ATTR               edgeWeightInfluence

 L.  73        64  LOAD_FAST                'jitterTolerance'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               jitterTolerance

 L.  74        70  LOAD_FAST                'barnesHutOptimize'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               barnesHutOptimize

 L.  75        76  LOAD_FAST                'barnesHutTheta'
               78  LOAD_FAST                'self'
               80  STORE_ATTR               barnesHutTheta

 L.  76        82  LOAD_FAST                'scalingRatio'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               scalingRatio

 L.  77        88  LOAD_FAST                'strongGravityMode'
               90  LOAD_FAST                'self'
               92  STORE_ATTR               strongGravityMode

 L.  78        94  LOAD_FAST                'gravity'
               96  LOAD_FAST                'self'
               98  STORE_ATTR               gravity

 L.  79       100  LOAD_FAST                'verbose'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               verbose

Parse error at or near `None' instruction at offset -1

    def init(self, G, pos=None):
        isSparse = False
        if isinstance(G, numpy.ndarray):
            assert G.shape == (G.shape[0], G.shape[0]), 'G is not 2D square'
            assert numpy.all(G.T == G), 'G is not symmetric.  Currently only undirected graphs are supported'
            if not isinstance(pos, numpy.ndarray):
                if not pos is None:
                    raise AssertionError('Invalid node positions')
        elif scipy.sparse.issparse(G):
            assert G.shape == (G.shape[0], G.shape[0]), 'G is not 2D square'
            if not isinstance(pos, numpy.ndarray):
                assert pos is None, 'Invalid node positions'
            G = G.tolil()
            isSparse = True
        else:
            assert False, 'G is not numpy ndarray or scipy sparse matrix'
        nodes = []
        for i in range(0, G.shape[0]):
            n = fa2util.Node()
            if isSparse:
                n.mass = 1 + len(G.rows[i])
            else:
                n.mass = 1 + numpy.count_nonzero(G[i])
            n.old_dx = 0
            n.old_dy = 0
            n.dx = 0
            n.dy = 0
            if pos is None:
                n.x = random.random()
                n.y = random.random()
            else:
                n.x = pos[i][0]
                n.y = pos[i][1]
            nodes.append(n)

        edges = []
        es = numpy.asarray(G.nonzero()).T
        for e in es:
            if e[1] <= e[0]:
                continue
            edge = fa2util.Edge()
            edge.node1 = e[0]
            edge.node2 = e[1]
            edge.weight = G[tuple(e)]
            edges.append(edge)

        return (nodes, edges)

    def forceatlas2(self, G, pos=None, iterations=100):
        speed = 1.0
        speedEfficiency = 1.0
        nodes, edges = self.init(G, pos)
        outboundAttCompensation = 1.0
        if self.outboundAttractionDistribution:
            outboundAttCompensation = numpy.mean([n.mass for n in nodes])
        barneshut_timer = Timer(name='BarnesHut Approximation')
        repulsion_timer = Timer(name='Repulsion forces')
        gravity_timer = Timer(name='Gravitational forces')
        attraction_timer = Timer(name='Attraction forces')
        applyforces_timer = Timer(name='AdjustSpeedAndApplyForces step')
        niters = range(iterations)
        if self.verbose:
            niters = tqdm(niters)
        for _i in niters:
            for n in nodes:
                n.old_dx = n.dx
                n.old_dy = n.dy
                n.dx = 0
                n.dy = 0

            if self.barnesHutOptimize:
                barneshut_timer.start()
                rootRegion = fa2util.Region(nodes)
                rootRegion.buildSubRegions()
                barneshut_timer.stop()
            else:
                repulsion_timer.start()
                if self.barnesHutOptimize:
                    rootRegion.applyForceOnNodes(nodes, self.barnesHutTheta, self.scalingRatio)
                else:
                    fa2util.apply_repulsion(nodes, self.scalingRatio)
            repulsion_timer.stop()
            gravity_timer.start()
            fa2util.apply_gravity(nodes, (self.gravity), useStrongGravity=(self.strongGravityMode))
            gravity_timer.stop()
            attraction_timer.start()
            fa2util.apply_attraction(nodes, edges, self.outboundAttractionDistribution, outboundAttCompensation, self.edgeWeightInfluence)
            attraction_timer.stop()
            applyforces_timer.start()
            values = fa2util.adjustSpeedAndApplyForces(nodes, speed, speedEfficiency, self.jitterTolerance)
            speed = values['speed']
            speedEfficiency = values['speedEfficiency']
            applyforces_timer.stop()

        if self.verbose:
            if self.barnesHutOptimize:
                barneshut_timer.display()
            repulsion_timer.display()
            gravity_timer.display()
            attraction_timer.display()
            applyforces_timer.display()
        return [(n.x, n.y) for n in nodes]

    def forceatlas2_networkx_layout(self, G, pos=None, iterations=100):
        import networkx
        if not isinstance(G, networkx.classes.graph.Graph):
            raise AssertionError('Not a networkx graph')
        else:
            if not isinstance(pos, dict):
                assert pos is None, 'pos must be specified as a dictionary, as in networkx'
            M = networkx.to_scipy_sparse_matrix(G, dtype='f', format='lil')
            if pos is None:
                l = self.forceatlas2(M, pos=None, iterations=iterations)
            else:
                poslist = numpy.asarray([pos[i] for i in G.nodes()])
            l = self.forceatlas2(M, pos=poslist, iterations=iterations)
        return dict(zip(G.nodes(), l))

    def forceatlas2_igraph_layout(self, G, pos=None, iterations=100, weight_attr=None):
        from scipy.sparse import csr_matrix
        import igraph

        def to_sparse(graph, weight_attr=None):
            edges = graph.get_edgelist()
            if weight_attr is None:
                weights = [
                 1] * len(edges)
            else:
                weights = graph.es[weight_attr]
            if not graph.is_directed():
                edges.extend([(v, u) for u, v in edges])
                weights.extend(weights)
            return csr_matrix((weights, zip(*edges)))

        assert isinstance(G, igraph.Graph), 'Not a igraph graph'
        if not isinstance(pos, (list, numpy.ndarray)):
            assert pos is None, 'pos must be a list or numpy array'
        if isinstance(pos, list):
            pos = numpy.array(pos)
        adj = to_sparse(G, weight_attr)
        coords = self.forceatlas2(adj, pos=pos, iterations=iterations)
        return igraph.layout.Layout(coords, 2)