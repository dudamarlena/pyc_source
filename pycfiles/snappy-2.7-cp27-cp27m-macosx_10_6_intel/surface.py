# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/surface.py
# Compiled at: 2017-05-26 08:27:22
from .simplex import *
from .tetrahedron import Tetrahedron
import sys
from .linalg import Vector, Matrix
MeetsQuad = {E01: Vector((1, 1, 0)), E02: Vector((1, 0, 1)), E21: Vector((0, 1, 1)), E32: Vector((1, 1, 0)), 
   E31: Vector((1, 0, 1)), E03: Vector((0, 1, 1))}
MeetsTri = {E01: Vector((1, 1, 0, 0)), E02: Vector((1, 0, 1, 0)), E21: Vector((0, 1, 1, 0)), E32: Vector((0, 0, 1, 1)), 
   E31: Vector((0, 1, 0, 1)), E03: Vector((1, 0, 0, 1))}
MeetsOct = {E01: Vector((1, 1, 2)), E02: Vector((1, 2, 1)), E21: Vector((2, 1, 1)), E32: Vector((1, 1, 2)), 
   E31: Vector((1, 2, 1)), E03: Vector((2, 1, 1))}
DisjointQuad = {E01: 2, E02: 1, E21: 0, E32: 2, 
   E31: 1, E03: 0}
QuadWeights = (
 Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))
WeightVector = Vector([1, 1, 1])
TypeVector = Vector([0, 1, 2])
QuadShifts = (
 (
  0, 1, -1), (-1, 0, 1), (1, -1, 0))
NonInteger = 'Error'

def gcd(x, y):
    if x == 0:
        if y == 0:
            raise ValueError('gcd(0,0) is undefined.')
        else:
            return abs(y)
    x = abs(x)
    y = abs(y)
    while y != 0:
        r = x % y
        x = y
        y = r

    return x


def reduce_slope(slope):
    a, b = slope
    if a == b == 0:
        return (slope, 0)
    g = gcd(a, b)
    a, b = a / g, b / g
    return ((a, b), g)


class Surface():

    def __init__(self, manifold, quadvector):
        self.Size = len(manifold)
        Q = Matrix(self.Size, 3, [ min(x, 1) for x in quadvector ])
        A = Matrix(self.Size, 3, quadvector)
        self.Quadvector = quadvector
        self.Coefficients = A.dot(WeightVector)
        self.Quadtypes = Q.dot(TypeVector)

    def type(self):
        if min(self.Coefficients) < 0:
            return 'almost-normal'
        else:
            return 'normal'

    def add_shifts(self):
        shifts = []
        for i in range(self.Size):
            shifts += [ self.Coefficients[i] * w for w in QuadShifts[self.Quadtypes[i]] ]

        self.Shifts = shifts

    def find_edge_linking_annuli(self, manifold):
        """
    Surface.find_edge_linking_annuli(mcomplex) returns a list of the
    indices of those edges for which the Surface contains an edge-linking
    annulus (and hence has an obvious compression).
    """
        if self not in manifold.NormalSurfaces:
            raise ValueError('That manifold does not contain the Surface!')
        linked_edges = []
        for edge in manifold.Edges:
            is_linked = 1
            for corner in edge.Corners:
                quad = DisjointQuad[corner.Subsimplex]
                if self.Coefficients[corner.Tetrahedron.Index] == 0 or self.Quadtypes[corner.Tetrahedron.Index] != quad:
                    is_linked = 0
                    break

            if is_linked:
                linked_edges.append(edge.Index)

        return linked_edges

    def info(self, out=sys.stdout):
        if self.type() == 'normal':
            out.write('Normal surface\n')
        for i in range(self.Size):
            quad_weight = self.Coefficients[i]
            if quad_weight == -1:
                weight = '  Quad Type Q%d3, weight: octagon' % self.Quadtypes[i]
            elif quad_weight > 0:
                weight = '  Quad Type  Q%d3, weight %d' % (self.Quadtypes[i], quad_weight)
            else:
                weight = 'No quads'
            out.write(weight + '\n')


class ClosedSurface(Surface):

    def __init__(self, manifold, quadvector):
        Surface.__init__(self, manifold, quadvector)
        self.build_weights(manifold)
        self.build_bounding_info(manifold)
        self.find_euler_characteristic(manifold)

    def build_weights(self, manifold):
        """
    Use self.QuadWeights self.QuadTypes vector to construct
    self.Weights and self.EdgeWeights.  The vector self.Weights has size
    7T and gives the weights of triangles and quads in each 3-simplex.
    In each bank of 7 weights, the first 4 are triangle weights and the
    last 3 are quad weights.
    """
        self.Weights = Vector(7 * self.Size)
        eqns = []
        constants = []
        edge_matrix = []
        for edge in manifold.Edges:
            edge_row = Vector(7 * len(manifold))
            corner = edge.Corners[0]
            j = corner.Tetrahedron.Index
            edge_row[(7 * j):(7 * j + 4)] = MeetsTri[corner.Subsimplex]
            if not self.Coefficients[j] == -1:
                edge_row[(7 * j + 4):(7 * j + 7)] = MeetsQuad[corner.Subsimplex]
            else:
                edge_row[(7 * j + 4):(7 * j + 7)] = MeetsOct[corner.Subsimplex]
            edge_matrix.append(edge_row)
            for i in range(len(edge.Corners) - 1):
                j = edge.Corners[i].Tetrahedron.Index
                k = edge.Corners[(i + 1)].Tetrahedron.Index
                row = Vector(4 * len(manifold))
                row[(4 * j):(4 * j + 4)] = MeetsTri[edge.Corners[i].Subsimplex]
                row[4 * k:4 * k + 4] -= MeetsTri[edge.Corners[(i + 1)].Subsimplex]
                eqns.append(row)
                c = 0
                if self.Coefficients[k] == -1:
                    c = MeetsOct[edge.Corners[(i + 1)].Subsimplex][self.Quadtypes[k]]
                elif MeetsQuad[edge.Corners[(i + 1)].Subsimplex][self.Quadtypes[k]]:
                    c = self.Coefficients[k]
                if self.Coefficients[j] == -1:
                    c -= MeetsOct[edge.Corners[i].Subsimplex][self.Quadtypes[j]]
                elif MeetsQuad[edge.Corners[i].Subsimplex][self.Quadtypes[j]]:
                    c -= self.Coefficients[j]
                constants.append(c)

            for vertex in manifold.Vertices:
                eqns.append(vertex.IncidenceVector)
                constants.append(0)

        A = Matrix(eqns)
        b = Vector(constants)
        x = A.solve(b)
        for vertex in manifold.Vertices:
            vert_vec = vertex.IncidenceVector
            m = min([ x[i] for i, w in enumerate(vert_vec) if w ])
            x -= Vector(m * vert_vec)

        for i in range(len(manifold)):
            for j in range(4):
                v = x[(4 * i + j)]
                assert int(v) == v
                self.Weights[7 * i + j] = int(v)

            if not self.Coefficients[i] == -1:
                self.Weights[(7 * i + 4):(7 * i + 7)] = self.Coefficients[i] * QuadWeights[int(self.Quadtypes[i])]
            else:
                self.Weights[(7 * i + 4):(7 * i + 7)] = QuadWeights[int(self.Quadtypes[i])]

        self.EdgeWeights = Matrix(edge_matrix).dot(self.Weights)

    def find_euler_characteristic(self, manifold):
        valences = Vector(manifold.EdgeValences)
        for edge in manifold.Edges:
            if edge.IntOrBdry == 'bdry':
                valences[edge.Index] += 1

        V = sum(self.EdgeWeights)
        E = self.EdgeWeights * valences / 2
        F = sum(abs(self.Weights))
        self.EulerCharacteristic = V - E + F

    def get_weight(self, tet_number, subsimplex):
        D = {V0: 0, V1: 1, V2: 2, V3: 3, E03: 4, E12: 4, E13: 5, E02: 5, E23: 6, E01: 6}
        return self.Weights[(7 * tet_number + D[subsimplex])]

    def has_quad(self, tet_number):
        return max([ self.get_weight(tet_number, e) for e in [E01, E02, E03] ]) > 0

    def get_edge_weight(self, edge):
        j = edge.Index
        return self.EdgeWeights[j]

    def build_bounding_info(self, manifold):
        if self.type() != 'normal':
            return (0, 0, None)
        else:
            bounds_subcomplex = 1
            double_bounds_subcomplex = 1
            for w in self.EdgeWeights:
                if w != 0 and w != 2:
                    bounds_subcomplex = 0
                if w != 0 and w != 1:
                    double_bounds_subcomplex = 0
                if not (bounds_subcomplex or double_bounds_subcomplex):
                    break

            if bounds_subcomplex or double_bounds_subcomplex:
                thick_or_thin = 'thin'
                for tet in manifold.Tetrahedra:
                    inside = 1
                    for e in OneSubsimplices:
                        w = self.get_edge_weight(tet.Class[e])
                        if w != 0:
                            inside = 0
                            break

                    if inside:
                        thick_or_thin = 'thick'
                        break

            else:
                thick_or_thin = None
            self.BoundingInfo = (bounds_subcomplex, double_bounds_subcomplex, thick_or_thin)
            return

    def is_edge_linking_torus(self):
        zeroes = 0
        zero_index = None
        for i in range(len(self.EdgeWeights)):
            w = self.EdgeWeights[i]
            if w == 0:
                if zeroes > 0:
                    return (0, None)
                zeroes = 1
                zero_index = i
            elif w != 2:
                return (0, None)

        return (
         1, zero_index)

    def info(self, manifold, out=sys.stdout):
        if self.type() == 'normal':
            q, e = self.is_edge_linking_torus()
            if q:
                out.write('Normal surface #%d is thin linking torus of edge %s\n' % (
                 manifold.NormalSurfaces.index(self), manifold.Edges[e]))
                return
            out.write('Normal surface #%d of Euler characteristic %d\n' % (
             manifold.NormalSurfaces.index(self), self.EulerCharacteristic))
            b, d, t = self.BoundingInfo
            if b == 1:
                out.write('  Bounds %s subcomplex\n' % t)
            elif d == 1:
                out.write('  Double bounds %s subcomplex\n' % t)
            else:
                out.write("  doesn't bound subcomplex\n")
        else:
            out.write('Almost-normal surface #%d of Euler characteristic %d\n' % (
             manifold.AlmostNormalSurfaces.index(self),
             self.EulerCharacteristic))
        out.write('\n')
        for i in range(self.Size):
            quad_weight = self.Coefficients[i]
            if quad_weight == -1:
                weight = '  Quad Type Q%d3, weight: octagon' % self.Quadtypes[i]
            elif quad_weight > 0:
                weight = '  Quad Type  Q%d3, weight %d' % (self.Quadtypes[i], quad_weight)
            else:
                weight = 'No quads'
            out.write('  In tetrahedron %s :  %s\n' % (
             manifold.Tetrahedra[i], weight))
            out.write('\tTri weights V0: %d V1: %d V2 : %d V3 : %d\n' % (
             self.get_weight(i, V0),
             self.get_weight(i, V1),
             self.get_weight(i, V2),
             self.get_weight(i, V3)))
            out.write('\n')

        for i in range(len(self.EdgeWeights)):
            out.write('  Edge %s has weight %d\n' % (
             manifold.Edges[i], self.EdgeWeights[i]))

    def casson_split(self, manifold):
        """

      Returns the "Casson Split" of the manifold along the normal
      surface.  That is, splits the manifold open along the surface
      and replaces the "combinatorial I-bundles" by I-bundles over
      disks.  Of course, doing so may change the topology of
      complementary manifold.
      
      """
        M = manifold
        have_quads = [ self.has_quad(i) for i in range(len(M)) ]
        new_tets = {}
        for i in have_quads:
            new_tets[i] = Tetrahedron()

        for i in have_quads:
            T = new_tets[i]


def dot_product(x, y):
    assert len(x) == len(y)
    dot = 0
    for i in range(len(x)):
        dot += x[i] * y[i]

    return dot


class SpunSurface(Surface):

    def __init__(self, manifold, quadvector):
        Surface.__init__(self, manifold, quadvector)
        self.Incompressible = None
        self.BoundarySlope = None
        return

    def add_boundary_slope(surface, cusp_equations):
        surface.BoundarySlope = (-dot_product(surface.Shifts, cusp_equations[1]),
         dot_product(surface.Shifts, cusp_equations[0]))

    def find_euler_characteristic(self, manifold):
        quadvector = array(self.Quadvector, 'd')
        floatresult = dot(manifold.Anglevector, quadvector)
        intresult = round(floatresult)
        error = abs(floatresult - intresult)
        if error > 1e-07:
            raise OverflowError('Yikes! A non-integral euler characteristic!')
        return -int(intresult)

    def info(self, manifold, out=sys.stdout):
        out.write('SpunSurface.\n Slope: %s; Boundary components: %d; ' % reduce_slope(self.BoundarySlope))
        out.write('Euler characteristic: %d\n' % self.find_euler_characteristic(manifold))
        out.write(' Incompressible: %s\n' % self.Incompressible)
        for i in range(self.Size):
            quad_weight = self.Coefficients[i]
            if quad_weight > 0:
                weight = '  Tet %d: Quad Type  Q%d3, weight %d' % (
                 i, self.Quadtypes[i], quad_weight)
            else:
                weight = '  Tet %d: no quads' % i
            out.write(weight + '\n')


class ClosedSurfaceInCusped(ClosedSurface):

    def __init__(self, manifold, quadvector):
        ClosedSurface.__init__(self, manifold, quadvector)
        self.Incompressible = None
        self.BoundarySlope = None
        return

    def info(self, manifold, out=sys.stdout):
        out.write('ClosedSurfaceInCusped #%d:  Euler %d;  Incompressible %s\n' % (
         manifold.ClosedSurfaces.index(self), self.EulerCharacteristic, self.Incompressible))
        q, e = self.is_edge_linking_torus()
        if q:
            out.write('    is thin linking surface of edge %s\n' % manifold.Edges[e])
            return
        b, d, t = self.BoundingInfo
        if b == 1:
            out.write('  Bounds %s subcomplex\n' % t)
        else:
            if d == 1:
                out.write('  Double bounds %s subcomplex\n' % t)
            else:
                out.write("  Doesn't bound subcomplex\n")
            for i in range(self.Size):
                quad_weight = self.Coefficients[i]
                if quad_weight > 0:
                    weight = '  Quad Type  Q%d3, weight %d' % (self.Quadtypes[i], quad_weight)
                else:
                    weight = 'No quads'
                out.write('  In tet %s :  %s\n' % (
                 manifold.Tetrahedra[i], weight))
                out.write('\tTri weights V0: %d V1: %d V2 : %d V3 : %d\n' % (
                 self.get_weight(i, V0),
                 self.get_weight(i, V1),
                 self.get_weight(i, V2),
                 self.get_weight(i, V3)))
                out.write('\n')

            for i in range(len(self.EdgeWeights)):
                out.write('  Edge %s has weight %d\n' % (
                 manifold.Edges[i], self.EdgeWeights[i]))