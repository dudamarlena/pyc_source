# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/mcomplex.py
# Compiled at: 2019-07-15 23:56:54
from __future__ import print_function
from .simplex import *
from .tetrahedron import Tetrahedron
from .corner import Corner
from .arrow import Arrow
from .face import Face
from .edge import Edge
from .vertex import Vertex
from .surface import Surface, SpunSurface, ClosedSurface, ClosedSurfaceInCusped
from . import files
from . import linalg
from . import homology
import os, sys, random
try:
    import snappy
except ImportError:
    snappy = None

VERBOSE = 0
Shift = {E01: (-1, 1, 0), E02: (1, 0, -1), E21: (0, -1, 1), E32: (
       -1, 1, 0), 
   E31: (1, 0, -1), E03: (0, -1, 1)}
VertexVector = {V0: (1, 0, 0, 0), V1: (0, 1, 0, 0), V2: (
      0, 0, 1, 0), 
   V3: (0, 0, 0, 1)}

class Insanity(Exception):
    pass


class Mcomplex():

    def __init__(self, tetrahedron_list=None):
        if tetrahedron_list is None:
            tetrahedron_list = []
        if isinstance(tetrahedron_list, str) and snappy == None:
            tetrahedron_list = tets_from_data(files.read_SnapPea_file(file_name=tetrahedron_list))
        if snappy:
            if isinstance(tetrahedron_list, str):
                tetrahedron_list = snappy.Triangulation(tetrahedron_list, remove_finite_vertices=False)
            if hasattr(tetrahedron_list, '_get_tetrahedra_gluing_data'):
                tetrahedron_list = tets_from_data(tetrahedron_list._get_tetrahedra_gluing_data())
        self.Tetrahedra = tetrahedron_list
        self.Edges = []
        self.Faces = []
        self.Vertices = []
        self.NormalSurfaces = []
        self.AlmostNormalSurfaces = []
        self.build()
        return

    def copy(self, base_arrow=None):
        new_tets = []
        new_to_old = {}
        old_to_new = {}
        for tet in self.Tetrahedra:
            new_tet = Tetrahedron()
            old_to_new[tet] = new_tet
            new_to_old[new_tet] = tet
            new_tets.append(new_tet)

        for new_tet in new_tets:
            for face in TwoSubsimplices:
                new_tet.attach(face, old_to_new[new_to_old[new_tet].Neighbor[face]], new_to_old[new_tet].Gluing[face].tuple())

        if base_arrow == None:
            return Mcomplex(new_tets)
        else:
            new_arrow = base_arrow.copy()
            new_arrow.Tetrahedron = old_to_new[base_arrow.Tetrahedron]
            return (Mcomplex(new_tets), new_arrow)
            return

    def build(self):
        for i in range(len(self.Tetrahedra)):
            self.Tetrahedra[i].Index = i

        self.build_face_classes()
        self.build_edge_classes()
        self.build_vertex_classes()
        self.build_one_skeleton()
        self.LinkGenera = [ vertex.link_genus() for vertex in self.Vertices ]

    def rebuild(self):
        for tet in self.Tetrahedra:
            tet.clear_Class()

        for face in self.Faces:
            face.erase()

        for edge in self.Edges:
            edge.erase()

        for vertex in self.Vertices:
            vertex.erase()

        self.Faces = []
        self.Edges = []
        self.Vertices = []
        self.build()

    def add_tet(self, tet):
        self.Tetrahedra.append(tet)

    def clear_tet(self, tet):
        for two_subsimplex in TwoSubsimplices:
            face = tet.Class[two_subsimplex]
            if not face == None:
                face.erase()
            try:
                self.Faces.remove(face)
            except ValueError:
                pass

        for one_subsimplex in OneSubsimplices:
            edge = tet.Class[one_subsimplex]
            if not edge == None:
                edge.erase()
            try:
                self.Edges.remove(edge)
            except ValueError:
                pass

        for zero_subsimplex in ZeroSubsimplices:
            vertex = tet.Class[zero_subsimplex]
            if not vertex == None:
                vertex.erase()
            try:
                self.Vertices.remove(vertex)
            except ValueError:
                pass

        return

    def delete_tet(self, tet):
        self.clear_tet(tet)
        tet.erase()
        self.Tetrahedra.remove(tet)

    def new_arrow(self):
        tet = Tetrahedron()
        self.add_tet(tet)
        return Arrow(E01, F3, tet)

    def new_arrows(self, n):
        return [ self.new_arrow() for i in range(n) ]

    def new_tet(self):
        tet = Tetrahedron()
        self.add_tet(tet)
        return tet

    def new_tets(self, n):
        return [ self.new_tet() for i in range(n) ]

    def __len__(self):
        return len(self.Tetrahedra)

    def __getitem__(self, index):
        return self.Tetrahedra[index]

    def info(self, out=sys.stdout):
        try:
            out.write('Mcomplex with %d Tetrahedra\n\n' % len(self))
            for tet in self.Tetrahedra:
                tet.info(out)

            out.write('\nEdges:\n')
            for edge in self.Edges:
                edge.info(out)

        except IOError:
            pass

    def build_edge_classes(self):
        for tet in self.Tetrahedra:
            for one_subsimplex in OneSubsimplices:
                if tet.Class[one_subsimplex] == None:
                    newEdge = Edge()
                    self.Edges.append(newEdge)
                    first_arrow = Arrow(one_subsimplex, RightFace[one_subsimplex], tet)
                    a = first_arrow.copy()
                    sanity_check = 0
                    boundary_hits = 0
                    while 1:
                        if sanity_check > 6 * len(self.Tetrahedra):
                            raise Insanity('Bad gluing data: could not construct edge link.')
                        newEdge._add_corner(a)
                        a.Tetrahedron.Class[a.Edge] = newEdge
                        if a.next() == None:
                            if not boundary_hits == 0:
                                newEdge.RightBdryArrow = a.copy()
                                newEdge.Corners.reverse()
                                break
                            else:
                                boundary_hits = 1
                                newEdge.LeftBdryArrow = a.copy()
                                newEdge.IntOrBdry = 'bdry'
                                a = first_arrow.copy()
                                a.reverse()
                                del newEdge.Corners[0]
                                newEdge.Corners.reverse()
                        elif a == first_arrow:
                            newEdge.IntOrBdry = 'int'
                            break
                        sanity_check = sanity_check + 1

        self.EdgeValences = [ edge.valence() for edge in self.Edges ]
        for i in range(len(self.Edges)):
            self.Edges[i].Index = i

        return

    def build_vertex_classes(self):
        for tet in self.Tetrahedra:
            for zero_subsimplex in ZeroSubsimplices:
                if tet.Class[zero_subsimplex] == None:
                    newVertex = Vertex()
                    self.Vertices.append(newVertex)
                    self.walk_vertex(newVertex, zero_subsimplex, tet)

        for i in range(len(self.Vertices)):
            self.Vertices[i].Index = i

        return

    def walk_vertex(self, vertex, zero_subsimplex, tet):
        if tet.Class[zero_subsimplex] != None:
            return
        else:
            tet.Class[zero_subsimplex] = vertex
            vertex.Corners.append(Corner(tet, zero_subsimplex))
            for two_subsimplex in TwoSubsimplices:
                if is_subset(zero_subsimplex, two_subsimplex) and tet.Gluing[two_subsimplex] != None:
                    self.walk_vertex(vertex, tet.Gluing[two_subsimplex].image(zero_subsimplex), tet.Neighbor[two_subsimplex])

            return

    def build_one_skeleton(self):
        for edge in self.Edges:
            tet = edge.Corners[0].Tetrahedron
            one_subsimplex = edge.Corners[0].Subsimplex
            tail = tet.Class[Tail[one_subsimplex]]
            head = tet.Class[Head[one_subsimplex]]
            edge.Vertices = [tail, head]
            tail.Edges.append(edge)
            head.Edges.append(edge)
            if edge.IntOrBdry == 'bdry':
                tail.IntOrBdry = 'bdry'
                head.IntOrBdry = 'bdry'

        for vertex in self.Vertices:
            if vertex.IntOrBdry == '':
                vertex.IntOrBdry = 'int'

    def build_face_classes(self):
        for tet in self.Tetrahedra:
            for two_subsimplex in TwoSubsimplices:
                if tet.Class[two_subsimplex] == None:
                    newFace = Face()
                    self.Faces.append(newFace)
                    newFace.Corners.append(Corner(tet, two_subsimplex))
                    tet.Class[two_subsimplex] = newFace
                    othertet = tet.Neighbor[two_subsimplex]
                    if othertet:
                        newFace.IntOrBdry = 'int'
                        othersubsimplex = tet.Gluing[two_subsimplex].image(two_subsimplex)
                        newFace.Corners.append(Corner(othertet, othersubsimplex))
                        othertet.Class[othersubsimplex] = newFace
                    else:
                        newFace.IntOrBdry = 'bdry'

        for i in range(len(self.Faces)):
            self.Faces[i].Index = i

        return

    def orient(self):
        for tet in self.Tetrahedra:
            tet.Checked = 0

        self.walk_and_orient(self[0], 1)
        self.rebuild()
        for tet in self.Tetrahedra:
            for two_subsimplex in TwoSubsimplices:
                if not tet.Neighbor[two_subsimplex] == None and tet.Gluing[two_subsimplex].sign() == 0:
                    return 0

        return 1

    def walk_and_orient(self, tet, sign):
        if tet.Checked == 1:
            return
        else:
            tet.Checked = 1
            if sign == 0:
                tet.reverse()
            for ssimp in TwoSubsimplices:
                if not tet.Neighbor[ssimp] == None:
                    self.walk_and_orient(tet.Neighbor[ssimp], tet.Gluing[ssimp].sign())

            return

    def build_matrix(self):
        int_edges = [ edge for edge in self.Edges if edge.IntOrBdry == 'int' ]
        self.QuadMatrix = linalg.Matrix(len(int_edges), 3 * len(self))
        for edge in int_edges:
            for corner in edge.Corners:
                i = int_edges.index(edge)
                j = corner.Tetrahedron.Index
                for k in range(3):
                    self.QuadMatrix[(i, 3 * j + k)] += Shift[corner.Subsimplex][k]

        self.build_vertex_incidences()

    def build_vertex_incidences(self):
        for vertex in self.Vertices:
            vertex.IncidenceVector = linalg.Vector(4 * len(self))
            for corner in vertex.Corners:
                j = corner.Tetrahedron.Index
                vertex.IncidenceVector[4 * j:4 * j + 4] += VertexVector[corner.Subsimplex]

    def find_normal_surfaces(self, modp=0, print_progress=False, algorithm='FXrays'):
        self.NormalSurfaces = []
        self.build_matrix()
        if algorithm == 'FXrays':
            try:
                import FXrays
            except ImportError:
                raise ImportError('You need to install the FXrays moduleif you want to find normal surfaces.')

            coeff_list = FXrays.find_Xrays(self.QuadMatrix.nrows(), self.QuadMatrix.ncols(), self.QuadMatrix.entries(), modp, print_progress=print_progress)
        else:
            if algorithm == 'regina':
                T = self.regina_triangulation()
                import regina
                coeff_list = []
                tets = range(len(self))
                surfaces = regina.NNormalSurfaceList.enumerate(T, regina.NS_QUAD)
                for i in range(surfaces.getNumberOfSurfaces()):
                    S = surfaces.getSurface(i)
                    coeff_vector = [ int(S.getQuadCoord(tet, quad).stringValue()) for tet in tets for quad in (2,
                                                                                                               1,
                                                                                                               0)
                                   ]
                    coeff_list.append(coeff_vector)

            else:
                raise ValueError("Algorithm must be in {'FXrays', 'regina'}")
            for coeff_vector in coeff_list:
                if max(self.LinkGenera) == 0:
                    self.NormalSurfaces.append(ClosedSurface(self, coeff_vector))
                elif self.LinkGenera.count(1) == len(self.LinkGenera):
                    self.NormalSurfaces.append(SpunSurface(self, coeff_vector))
                else:
                    self.NormalSurfaces.append(Surface(self, coeff_vector))

    def normal_surface_info(self, out=sys.stdout):
        try:
            for surface in self.NormalSurfaces:
                out.write('-------------------------------------\n\n')
                surface.info(self, out)
                out.write('\n')

        except IOError:
            pass

    def almost_normal_surface_info(self, out=sys.stdout):
        try:
            for surface in self.AlmostNormalSurfaces:
                out.write('-------------------------------------\n\n')
                surface.info(self, out)
                out.write('\n')

        except IOError:
            pass

    def two_to_three(self, two_subsimplex, tet):
        a = Arrow(PickAnEdge[two_subsimplex], two_subsimplex, tet)
        b = a.glued()
        if b.Tetrahedron == None:
            return 0
        else:
            if a.Tetrahedron == b.Tetrahedron:
                return 0
            new = self.new_arrows(3)
            for i in range(3):
                new[i].glue(new[((i + 1) % 3)])

            a.reverse()
            for c in new:
                c.opposite().glue(a.glued())
                c.reverse().glue(b.glued())
                a.rotate(-1)
                b.rotate(1)

            self.delete_tet(a.Tetrahedron)
            self.delete_tet(b.Tetrahedron)
            self.build_edge_classes()
            if VERBOSE:
                print('2->3')
                print(self.EdgeValences)
            return 1

    def three_to_two(self, edge):
        if not edge.IntOrBdry == 'int':
            return 0
        if edge.valence() != 3 or not edge.distinct():
            return 0
        a = Arrow(edge.Corners[0].Subsimplex, LeftFace[edge.Corners[0].Subsimplex], edge.Corners[0].Tetrahedron)
        b = self.new_arrow()
        c = self.new_arrow()
        b.glue(c)
        b.reverse()
        for i in range(3):
            b.glue(a.opposite().glued())
            c.glue(a.reverse().glued())
            b.rotate(-1)
            c.rotate(1)
            a.reverse().opposite().next()

        for corner in edge.Corners:
            self.delete_tet(corner.Tetrahedron)

        self.build_edge_classes()
        if VERBOSE:
            print('3->2')
            print(self.EdgeValences)
        return 1

    def two_to_zero(self, edge):
        if not edge.IntOrBdry == 'int':
            return 0
        if edge.valence() != 2 or not edge.distinct():
            return 0
        a = Arrow(edge.Corners[0].Subsimplex, LeftFace[edge.Corners[0].Subsimplex], edge.Corners[0].Tetrahedron)
        b = a.glued()
        if a.Tetrahedron.Class[comp(a.Edge)] == b.Tetrahedron.Class[comp(b.Edge)]:
            return 0
        a.opposite().glued().reverse().glue(b.opposite().glued())
        a.reverse().glued().reverse().glue(b.reverse().glued())
        for corner in edge.Corners:
            self.delete_tet(corner.Tetrahedron)

        self.build_edge_classes()
        if VERBOSE:
            print('2->0')
            print(self.EdgeValences)
        return 1

    def zero_to_two(self, arrow1, gap):
        arrow2 = arrow1.copy().reverse()
        count = 0
        while count < gap:
            if arrow2.next() == None:
                return 0
            count = count + 1

        a = arrow1.glued()
        b = arrow2.glued()
        if b.Tetrahedron == arrow1.Tetrahedron:
            return 0
        else:
            c = self.new_arrows(2)
            c[0].glue(c[1])
            c[1].glue(c[0])
            c[0].opposite().glue(a)
            c[0].reverse().glue(b)
            c[1].opposite().glue(arrow1.reverse())
            c[1].reverse().glue(arrow2.reverse())
            self.clear_tet(arrow1.Tetrahedron)
            self.clear_tet(arrow2.Tetrahedron)
            self.build_edge_classes()
            if VERBOSE:
                print('0->2')
                print(self.EdgeValences)
            return 1

    def four_to_four(self, edge_or_arrow):
        if edge_or_arrow.__class__ == Edge:
            edge = edge_or_arrow
            a = Arrow(edge.Corners[0].Subsimplex, LeftFace[edge.Corners[0].Subsimplex], edge.Corners[0].Tetrahedron)
            if random.randint(0, 1) == 0:
                a.reverse()
        if edge_or_arrow.__class__ == Arrow:
            a = edge_or_arrow
            edge = a.Tetrahedron.Class[a.Edge]
        if not edge.IntOrBdry == 'int':
            return 0
        if edge.valence() != 4 or not edge.distinct():
            return 0
        c = self.new_arrows(4)
        for i in range(4):
            c[i].glue(c[((i + 1) % 4)])

        b = a.glued().reverse()
        c[0].opposite().glue(a.rotate(1).glued())
        c[1].opposite().glue(b.rotate(-1).glued())
        c[2].opposite().glue(b.rotate(-1).glued())
        c[3].opposite().glue(a.rotate(1).glued())
        a.rotate(1).reverse().next()
        b.rotate(-1).reverse().next()
        c[0].reverse().glue(a.rotate(-1).glued())
        c[1].reverse().glue(b.rotate(1).glued())
        c[2].reverse().glue(b.rotate(1).glued())
        c[3].reverse().glue(a.rotate(-1).glued())
        for corner in edge.Corners:
            self.delete_tet(corner.Tetrahedron)

        self.build_edge_classes()
        if VERBOSE:
            print('4->4')
            print(self.EdgeValences)
        return 1

    def eliminate_valence_two(self):
        did_simplify = 0
        progress = 1
        while progress:
            progress = 0
            for edge in self.Edges:
                if edge.valence() == 2:
                    if self.two_to_zero(edge):
                        progress, did_simplify = (1, 1)
                        break

        return did_simplify

    def eliminate_valence_three(self):
        did_simplify = 0
        progress = 1
        while progress:
            progress = 0
            for edge in self.Edges:
                if edge.valence() == 3:
                    if self.three_to_two(edge):
                        progress, did_simplify = (1, 1)
                        break

        return did_simplify

    def easy_simplify(self):
        did_simplify = 0
        progress = 1
        while progress:
            progress = 0
            if self.eliminate_valence_two():
                progress, did_simplify = (1, 1)
            if self.eliminate_valence_three():
                progress, did_simplify = (1, 1)

        return did_simplify

    def jiggle(self):
        tries = []
        for edge in self.Edges:
            if edge.valence() == 4 and edge.IntOrBdry == 'int':
                tries.append(edge)

        if len(tries) == 0:
            return 0
        return self.four_to_four(tries[random.randint(0, len(tries) - 1)])

    JIGGLE_LIMIT = 6

    def simplify(self):
        did_simplify = 0
        count = 0
        while count < self.JIGGLE_LIMIT:
            if self.easy_simplify():
                did_simplify = 1
            else:
                count = count + 1
            if self.jiggle() == 0:
                break

        self.eliminate_valence_two()
        return did_simplify

    BLOW_UP_MULTIPLE = 6

    def blowup(self, n):
        for i in range(n):
            rand_tet = self[random.randint(0, len(self) - 1)]
            rand_face = TwoSubsimplices[random.randint(0, 3)]
            self.two_to_three(rand_face, rand_tet)
            self.eliminate_valence_two()

        return len(self)

    def blowup2(self, n):
        for i in range(n):
            rand_edge = self.Edges[random.randint(0, len(self.Edges) - 1)]
            j = random.randint(0, len(rand_edge.Corners) - 1)
            k = random.randint(0, len(rand_edge.Corners) - 1 - j)
            one_subsimplex = rand_edge.Corners[j].Subsimplex
            two_subsimplex = LeftFace[one_subsimplex]
            a = Arrow(one_subsimplex, two_subsimplex, rand_edge.Corners[j].Tetrahedron)
            self.zero_to_two(a, k)
            self.eliminate_valence_three()

        return len(self)

    def randomize(self):
        self.blowup(self.BLOW_UP_MULTIPLE * len(self))
        self.simplify()
        self.rebuild()
        return len(self)

    def bdry_neighbor(self, arrow):
        if arrow.next() != None:
            raise Insanity('That boundary face is not on the boundary!')
        edge = arrow.Tetrahedron.Class[arrow.Edge]
        if edge.LeftBdryArrow == arrow:
            return edge.RightBdryArrow
        else:
            return edge.LeftBdryArrow
            return

    def add_fan(self, edge, n):
        if not edge.IntOrBdry == 'bdry':
            return 0
        a = edge.LeftBdryArrow
        b = edge.RightBdryArrow.reverse()
        if n == 0:
            a.glue(b)
            return 1
        new = self.new_arrows(n)
        a.glue(new[0])
        for j in range(len(new) - 1):
            new[j].glue(new[(j + 1)])

        new[(-1)].glue(b)
        self.rebuild()
        return 1

    def split_star(self, edge):
        if edge.selfadjacent():
            return 0
        garbage = []
        first_arrow = edge.get_arrow().next()
        first_bottom, first_top = self.new_arrows(2)
        a = first_arrow.copy()
        bottom = first_bottom.copy()
        top = first_top.copy()
        while 1:
            garbage.append(a.Tetrahedron)
            bottom.glue(top)
            a.opposite()
            above = a.glued()
            if above.is_null():
                check = a.copy().opposite().reverse()
                new_first = top.copy().opposite().reverse()
                if check == first_top:
                    first_top = new_first
                elif check == first_bottom:
                    first_bottom = new_first
            else:
                top.glue(above)
            bottom.reverse()
            a.reverse()
            below = a.glued()
            if below.is_null():
                check = a.copy().opposite().reverse()
                new_first = bottom.copy().opposite().reverse()
                if check == first_bottom:
                    first_bottom = new_first
                elif check == first_top:
                    first_top = new_first
            else:
                bottom.glue(below)
            bottom.reverse()
            a.reverse()
            a.opposite()
            a.next()
            if a == first_arrow:
                break
            next_bottom, next_top = self.new_arrows(2)
            top.opposite()
            bottom.opposite()
            top.glue(next_top)
            bottom.glue(next_bottom)
            top = next_top.opposite()
            bottom = next_bottom.opposite()

        top.opposite()
        bottom.opposite()
        top.glue(first_top.opposite())
        bottom.glue(first_bottom.opposite())
        for tet in garbage:
            self.delete_tet(tet)

        self.rebuild()
        return first_top

    def smash_star(self, edge):
        if not edge.distinct():
            return 0
        if edge.Vertices[0] == edge.Vertices[1]:
            return 0
        start = edge.get_arrow()
        a = start.copy()
        garbage = []
        while 1:
            garbage.append(a.Tetrahedron)
            top = a.opposite().glued()
            bottom = a.reverse().glued().reverse()
            bottom.glue(top)
            a.reverse().opposite().next()
            if a == start:
                break

        for tet in garbage:
            self.delete_tet(tet)

        self.rebuild()
        return 1

    def replace_star(self, arrow, top_arrows, bottom_arrows):
        edge = arrow.Tetrahedron.Class[arrow.Edge]
        a = arrow.copy().opposite()
        if not edge.IntOrBdry == 'int':
            return None
        else:
            if not edge.distinct():
                return None
            valence = edge.valence()
            if len(top_arrows) != valence or len(bottom_arrows) != valence:
                return None
            for i in range(valence):
                top_arrows[i].glue(a.glued())
                a.reverse()
                bottom_arrows[i].glue(a.glued())
                a.reverse()
                a.opposite()
                a.next()
                a.opposite()

            for corner in edge.Corners:
                self.delete_tet(corner.Tetrahedron)

            self.build_edge_classes()
            self.orient()
            return 1

    def suspension_of_polygon(self, num_sides_of_polygon):
        top_tets = self.new_tets(num_sides_of_polygon - 2)
        bottom_tets = self.new_tets(num_sides_of_polygon - 2)
        n = len(top_tets)
        for i in range(n):
            top_tets[i].attach(F3, bottom_tets[i], (0, 2, 1, 3))

        for i in range(n - 1):
            top_tets[i].attach(F0, top_tets[(i + 1)], (1, 0, 2, 3))
            bottom_tets[i].attach(F0, bottom_tets[(i + 1)], (2, 1, 0, 3))

        top_arrows = [
         Arrow(comp(E13), F1, top_tets[0])]
        bottom_arrows = [Arrow(comp(E23), F2, bottom_tets[0])]
        for i in range(n):
            top_arrows.append(Arrow(comp(E23), F2, top_tets[i]))
            bottom_arrows.append(Arrow(comp(E13), F1, bottom_tets[i]))

        top_arrows.append(Arrow(comp(E03), F0, top_tets[i]))
        bottom_arrows.append(Arrow(comp(E03), F0, bottom_tets[i]))
        return (
         top_arrows, bottom_arrows)

    def save(self, filename, format='snappy'):
        """
       Nontypical example showing saving to a string buffer:

       >>> import io
       >>> buffer = io.StringIO()
       >>> T = Mcomplex('v3551')
       >>> T.save(buffer, 'snappy')
       >>> T.save(buffer, 'geo')
       >>> T.save(buffer, 'spine')
       >>> len(buffer.getvalue())
       1936
       """
        if not hasattr(filename, 'write'):
            file = open(filename, 'w')
            close = True
        else:
            file = filename
            close = False
        if format == 'snappy':
            files.write_SnapPea_file(self, file)
        elif format == 'geo':
            files.write_geo_file(self, file)
        elif format == 'spine':
            files.write_spine_file(self, file)
        if close:
            file.close()

    def _snappea_file_contents(self):
        import StringIO
        data = StringIO.StringIO()
        data.name = 'from_t3m'
        files.write_SnapPea_file(self, data)
        return data.getvalue()

    def snappy_triangulation(self):
        return snappy.Triangulation(self._snappea_file_contents())

    def snappy_manifold(self):
        return self.snappy_triangulation().with_hyperbolic_structure()

    def isosig(self):
        return snappy.Triangulation(self._snappea_file_contents(), remove_finite_vertices=False).triangulation_isosig(decorated=False)

    def regina_triangulation(self):
        try:
            import regina
        except ImportError:
            raise ImportError('Regina module not available')

        data = self._snappea_file_contents()
        return regina.NTriangulation(self.snappy_triangulation()._to_string())

    def boundary_maps(self):
        """
        The boundary maps in the homology chain complex of the 
        underlying cell-complex of a Mcomplex.
        
        >>> M = Mcomplex('o9_12345')
        >>> len(M.boundary_maps()) == 3
        True
        """
        return homology.boundary_maps(self)


def tets_from_data(fake_tets):
    fake_tets = fake_tets
    num_tets = len(fake_tets)
    tets = [ Tetrahedron() for i in range(num_tets) ]
    for i in range(num_tets):
        neighbors, perms = fake_tets[i]
        for k in range(4):
            tets[i].attach(TwoSubsimplices[k], tets[neighbors[k]], perms[k])

    return tets


def read_geo_file(filename):
    return Mcomplex(tets_from_data(files.read_geo_file(filename)))


def read_SnapPea_file(filename):
    return Mcomplex(tets_from_data(files.read_SnapPea_file(filename)))