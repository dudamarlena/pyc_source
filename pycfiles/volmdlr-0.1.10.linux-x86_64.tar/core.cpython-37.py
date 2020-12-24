# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/volmdlr/core.py
# Compiled at: 2020-03-11 05:21:08
# Size of source mod 2**32: 200123 bytes
"""

"""
from packaging import version
import warnings, math, numpy as npy
npy.seterr(divide='raise')
from geomdl import NURBS
import matplotlib.pyplot as plt
import mpl_toolkits
from matplotlib.patches import Arc, FancyArrow, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib import __version__ as _mpl_version
import networkx as nx
from .core_compiled import Vector2D, Vector3D, Point2D, Point3D, O2D, X2D, Y2D, OXY, Basis3D, Frame2D, Frame3D, O3D, X3D, Y3D, Z3D, LineSegment2DPointDistance, PolygonPointBelongs
from scipy.linalg import solve
import volmdlr.geometry as geometry
from volmdlr import plot_data
import triangle, dessia_common as dc
from typing import TypeVar, List, Tuple
from jinja2 import Environment, PackageLoader, select_autoescape
import webbrowser, os, tempfile, subprocess, random

def standardize_knot_vector(knot_vector):
    u0 = knot_vector[0]
    u1 = knot_vector[(-1)]
    standard_u_knots = []
    if u0 != 0 or u1 != 1:
        x = 1 / (u1 - u0)
        y = u0 / (u0 - u1)
        for u in knot_vector:
            standard_u_knots.append(u * x + y)

        return standard_u_knots
    return knot_vector


def find_and_replace(string, find, replace):
    """
    Finds a string in a string and replace it
    """
    index = string.find(find)
    if index != -1:
        try:
            int(string[(index + len(find))])
        except (ValueError, IndexError):
            return string[:index] + replace + string[index + len(find):]
        else:
            return string[:index] + find_and_replace(string[(index + len(find))], find, replace)
    return string


def step_split_arguments(function_arg):
    """
    Split the arguments of a function that doesn't start with '(' but end with ')'
    ex: IN: '#123,#124,#125)'
       OUT: ['#123', '#124', '#125']
    """
    if len(function_arg) > 0:
        if function_arg[(-1)] != ')':
            function_arg += ')'
    arguments = []
    argument = ''
    parenthesis = 1
    for char in function_arg:
        if char == '(':
            parenthesis += 1
        elif char != ',' or parenthesis > 1:
            argument += char
        else:
            arguments.append(argument)
            argument = ''
        if char == ')':
            parenthesis -= 1
            if parenthesis == 0:
                arguments.append(argument[:-1])
                argument = ''
                break

    return arguments


def set_to_list(step_set):
    char_list = step_set.split(',')
    char_list[0] = char_list[0][1:]
    char_list[-1] = char_list[(-1)][:-1]
    return [elem for elem in char_list]


def delete_node_and_predecessors(graph, node):
    predecessors = list(graph.predecessors(node))
    graph.remove_node(node)
    for predecessor in predecessors:
        delete_node_and_predecessors(graph, predecessor)


def delete_node_and_successors(graph, node):
    successors = list(graph.successors(node))
    graph.remove_node(node)
    for successor in successors:
        delete_node_and_successors(graph, successor)


def clockwise_angle(vector1, vector2):
    """
    Return the clockwise angle in radians between vector1 and vector2.
    """
    vector0 = Vector2D((0, 0))
    if vector0 in (vector1, vector2):
        return 0
    dot = vector1.Dot(vector2)
    norm_vec_1 = vector1.Norm()
    norm_vec_2 = vector2.Norm()
    cross = vector1.Cross(vector2)
    inner_angle = math.acos(dot / (norm_vec_1 * norm_vec_2))
    if cross < 0:
        return inner_angle
    return 2 * math.pi - inner_angle


class Primitive2D(dc.DessiaObject):

    def __init__(self, name=''):
        self.name = name


class CompositePrimitive2D(Primitive2D):
    __doc__ = '\n    A collection of simple primitives\n    '

    def __init__(self, primitives, name=''):
        Primitive2D.__init__(self, name)
        self.primitives = primitives

    def Rotation(self, center, angle, copy=True):
        if copy:
            return self.__class__([p.Rotation(center, angle, copy=True) for p in self.primitives])
        for p in self.primitives:
            p.Rotation(center, angle, copy=False)

        self.UpdateBasisPrimitives()

    def Translation(self, offset, copy=True):
        if copy:
            return self.__class__([p.Translation(offset, copy=True) for p in self.primitives])
        for p in self.primitives:
            p.Translation(offset, copy=False)

        self.UpdateBasisPrimitives()

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            return self.__class__([p.frame_mapping(frame, side, copy=True) for p in self.primitives])
        for p in self.primitives:
            p.frame_mapping(frame, side, copy=False)

        self.UpdateBasisPrimitives()

    def To3D(self, plane_origin, x, y, name=None):
        if name is None:
            name = '3D of {}'.format(self.name)
        primitives3D = [p.To3D(plane_origin, x, y) for p in self.primitives]
        return CompositePrimitive3D(primitives3D, name)

    def MPLPlot(self, ax=None, color='k', arrow=False, width=None, plot_points=False):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
        else:
            fig = ax.figure
        for element in self.primitives:
            if element.__class__.__name__ == 'LineSegment2D':
                element.MPLPlot(ax, color, arrow, width, plot_points=plot_points)
            else:
                element.MPLPlot(ax, color=color)

        ax.margins(0.1)
        plt.show()
        return (
         fig, ax)

    def plot_data(self, name, fill=None, color='black', stroke_width=0.2, opacity=1):
        plot_data = {}
        plot_data['fill'] = fill
        plot_data['name'] = name
        plot_data['type'] = 'contour'
        plot_data['plot_data'] = []
        for item in self.primitives:
            plot_data['plot_data'].append(item.plot_data(color=color, stroke_width=stroke_width,
              opacity=opacity))

        return plot_data


class Wire2D(CompositePrimitive2D):
    __doc__ = '\n    A collection of simple primitives, following each other making a wire\n    '

    def __init__(self, primitives, name=''):
        CompositePrimitive2D.__init__(self, primitives, name)

    def Length(self):
        length = 0.0
        for primitive in self.primitives:
            length += primitive.Length()

        return length

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        length = 0.0
        for primitive in self.primitives:
            primitive_length = primitive.Length()
            if length + primitive_length > curvilinear_abscissa:
                return primitive.PointAtCurvilinearAbscissa(curvilinear_abscissa - length)
            length += primitive_length

        return ValueError

    def plot_data(self, name='', fill=None, color='black', stroke_width=1, opacity=1):
        plot_data = {}
        plot_data['name'] = name
        plot_data['type'] = 'wire'
        plot_data['plot_data'] = []
        for item in self.primitives:
            plot_data['plot_data'].append(item.plot_data(color=color, stroke_width=stroke_width,
              opacity=opacity))

        return plot_data

    def line_intersection(self, line):
        intersection_points = []
        for primitive in self.primitives:
            pts = primitive.line_intersection(line)
            if pts is not None:
                if type(pts) is list:
                    intersection_points.extend(pts)
                else:
                    intersection_points.append(pts)

        if intersection_points:
            return intersection_points
        return


class Contour2D(Wire2D):
    __doc__ = '\n    A collection of 2D primitives forming a closed wire2D\n    TODO : CenterOfMass and SecondMomentArea should be changed accordingly to\n    Area considering the triangle drawn by the arcs\n    '
    _non_serializable_attributes = ['internal_arcs', 'external_arcs', 'polygon', 'straight_line_contour_polygon']

    def __init__(self, primitives, name=''):
        Wire2D.__init__(self, primitives, name)
        self._utd_analysis = False

    def _primitives_analysis(self):
        """
        An internal arc is an arc that has his interior point inside the polygon
        """
        arcs = []
        internal_arcs = []
        external_arcs = []
        points_polygon = []
        points_straight_line_contour = []
        for primitive in self.primitives:
            if primitive.__class__.__name__ == 'LineSegment2D':
                points_polygon.extend(primitive.points)
                points_straight_line_contour.extend(primitive.points)
            elif primitive.__class__.__name__ == 'Arc2D':
                points_polygon.append(primitive.start)
                points_polygon.append(primitive.end)
                arcs.append(primitive)
            else:
                if primitive.__class__.__name__ == 'Circle2D':
                    return
                raise NotImplementedError('primitive of type {} is not handled'.format(primitive))

        polygon = Polygon2D(points_polygon)
        straight_line_contour_polygon = Polygon2D(points_straight_line_contour)
        for arc in arcs:
            if polygon.PointBelongs(arc.interior):
                internal_arcs.append(arc)
            else:
                external_arcs.append(arc)

        return (
         internal_arcs, external_arcs, polygon, straight_line_contour_polygon)

    def _get_internal_arcs(self):
        if not self._utd_analysis:
            self._internal_arcs, self._external_arcs, self._polygon, self._straight_line_contour_polygon = self._primitives_analysis()
            self._utd_analysis = True
        return self._internal_arcs

    internal_arcs = property(_get_internal_arcs)

    def _get_external_arcs(self):
        if not self._utd_analysis:
            self._internal_arcs, self._external_arcs, self._polygon, self._straight_line_contour_polygon = self._primitives_analysis()
            self._utd_analysis = True
        return self._internal_arcs

    external_arcs = property(_get_external_arcs)

    def _get_polygon(self):
        if not self._utd_analysis:
            self._internal_arcs, self._external_arcs, self._polygon, self._straight_line_contour_polygon = self._primitives_analysis()
            self._utd_analysis = True
        return self._polygon

    polygon = property(_get_polygon)

    def _get_straight_line_contour_polygon(self):
        if not self._utd_analysis:
            self._internal_arcs, self._external_arcs, self._polygon, self._straight_line_contour_polygon = self._primitives_analysis()
            self._utd_analysis = True
        return self._straight_line_contour_polygon

    straight_line_contour_polygon = property(_get_straight_line_contour_polygon)

    def point_belongs(self, point):
        for arc in self.internal_arcs:
            if arc.point_belongs(point):
                return False

        if self.polygon.PointBelongs(point):
            return True
        for arc in self.external_arcs:
            if arc.point_belongs(point):
                return True

        return False

    def point_distance(self, point):
        min_distance = self.primitives[0].point_distance(point)
        for primitive in self.primitives[1:]:
            distance = primitive.point_distance(point)
            if distance < min_distance:
                min_distance = distance

        return min_distance

    def bounding_points(self):
        points = self.straight_line_contour_polygon.points[:]
        for arc in self.internal_arcs + self.external_arcs:
            points.extend(arc.tessellation_points())

        xmin = min([p[0] for p in points])
        xmax = max([p[0] for p in points])
        ymin = min([p[1] for p in points])
        ymax = max([p[1] for p in points])
        return (Point2D((xmin, ymin)), Point2D((xmax, ymax)))

    def To3D(self, plane_origin, x, y, name=None):
        if name is None:
            name = '3D of {}'.format(self.name)
        primitives3D = [p.To3D(plane_origin, x, y) for p in self.primitives]
        return Contour3D(edges=primitives3D, name=name)

    def Area(self):
        if len(self.primitives) == 1:
            return self.primitives[0].Area()
        A = self.polygon.Area()
        for arc in self.internal_arcs:
            triangle = Polygon2D([arc.start, arc.center, arc.end])
            A = A - arc.Area() + triangle.Area()

        for arc in self.external_arcs:
            triangle = Polygon2D([arc.start, arc.center, arc.end])
            A = A + arc.Area() - triangle.Area()

        return A

    def CenterOfMass(self):
        if len(self.primitives) == 1:
            return self.primitives[0].CenterOfMass()
        else:
            area = self.polygon.Area()
            if area > 0.0:
                c = area * self.polygon.CenterOfMass()
            else:
                c = O2D
        for arc in self.internal_arcs:
            arc_area = arc.Area()
            c -= arc_area * arc.CenterOfMass()
            area -= arc_area

        for arc in self.external_arcs:
            arc_area = arc.Area()
            c += arc_area * arc.CenterOfMass()
            area += arc_area

        return c / area

    def SecondMomentArea(self, point):
        if len(self.primitives) == 1:
            return self.primitives[0].SecondMomentArea(point)
        A = self.polygon.SecondMomentArea(point)
        for arc in self.internal_arcs:
            A -= arc.SecondMomentArea(point)

        for arc in self.external_arcs:
            A += arc.SecondMomentArea(point)

        return A

    def plot_data(self, name='', fill=None, marker=None, color='black', stroke_width=1, dash=False, opacity=1):
        plot_data = {}
        plot_data['fill'] = fill
        plot_data['name'] = name
        plot_data['type'] = 'contour'
        plot_data['plot_data'] = []
        for item in self.primitives:
            plot_data['plot_data'].append(item.plot_data(color=color, stroke_width=stroke_width,
              opacity=opacity))

        return plot_data


class Mesh2D:

    def __init__(self, contours, points_densities, default_density):
        self.contours = contours
        self.points_densities = points_densities
        self.default_density = default_density

    def GeoScript(self, filepath=''):
        s = ''
        ipt = 1
        ipr = 1
        points_index = {}
        for contour in self.contours:
            for primitive in contour.primitives:
                for point in primitive.geo_points:
                    try:
                        points_index[point]
                    except KeyError:
                        points_index[point] = ipt
                        try:
                            d = self.points_densities[point]
                        except KeyError:
                            d = self.default_density

                        s += ('Point({})={{{},{},0.,{}}};\n'.format)(ipt, *point.vector, *(d,))
                        ipt += 1

        contours_indices = []
        for contour in self.contours:
            contour_iprs = []
            for primitive in contour.primitives:
                spr, ipr2 = primitive.GeoScript(ipr, [points_index[p] for p in primitive.geo_points])
                s += spr
                contour_iprs.extend(range(ipr, ipr2))
                ipr = ipr2

            s += 'Line Loop({}) = {{{}}};\n'.format(ipr, str(contour_iprs)[1:-1])
            contours_indices.append(ipr)
            ipr += 1

        s += 'Plane Surface({}) = {{{}}};\n'.format(ipr, str(contours_indices)[1:-1])
        if filepath != '':
            with open(filepath, 'w') as (file):
                file.write(s)
        return s


class Line(dc.DessiaObject):

    def __neg__(self):
        return self.__class__(self.points[::-1])

    def DirectionVector(self, unit=False):
        u = self.points[1] - self.points[0]
        if unit:
            u.Normalize()
        return u

    def NormalVector(self, unit=False):
        return self.DirectionVector(unit).NormalVector()


class Line2D(Primitive2D, Line):
    __doc__ = '\n    Define an infinte line given by two points.\n    '

    def __init__(self, point1, point2, name=''):
        Primitive2D.__init__(self, name=name)
        self.points = [point1, point2]

    def To3D(self, plane_origin, x1, x2):
        p3D = [p.To3D(plane_origin, x1, x2) for p in self.points]
        return Line2D(*p3D, *(self.name,))

    def Rotation(self, center, angle, copy=True):
        if copy:
            return Line2D(*[p.Rotation(center, angle, copy=True) for p in self.points])
        for p in self.points:
            p.Rotation(center, angle, copy=False)

    def Translation(self, offset, copy=True):
        if copy:
            return Line2D(*[p.Translation(offset, copy=True) for p in self.points])
        for p in self.points:
            p.Translation(offset, copy=False)

    def point_distance(self, point, return_other_point=False):
        """
        Computes the distance of a point to line
        """
        p1, p2 = self.points
        u = p2 - p1
        t = (point - p1).Dot(u) / u.Norm() ** 2
        projection = p1 + t * u
        if return_other_point:
            return (
             (point - projection).Norm(), projection)
        return (point - projection).Norm()

    def PointProjection(self, point, curvilinear_abscissa=False):
        p1, p2 = self.points
        u = p2 - p1
        t = (point - p1).Dot(u) / u.Norm() ** 2
        projection = p1 + t * u
        if curvilinear_abscissa:
            return (
             projection, t)
        return projection

    def MPLPlot(self, ax=None, color='k', dashed=True):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
        else:
            fig = ax.figure
        p1, p2 = self.points
        u = p2 - p1
        p3 = p1 - 3 * u
        p4 = p2 + 4 * u
        if dashed:
            ax.plot([p3[0], p4[0]], [p3[1], p4[1]], color=color, dashes=[30, 5, 10, 5])
        else:
            ax.plot([p3[0], p4[0]], [p3[1], p4[1]], color=color)
        return (
         fig, ax)

    def plot_data(self, marker=None, color='black', stroke_width=1, dash=False, opacity=1, arrow=False):
        p1, p2 = self.points
        u = p2 - p1
        p3 = p1 - 3 * u
        p4 = p2 + 4 * u
        return {'type':'line',  'data':[
          p3[0], p3[1],
          p4[0], p4[1]], 
         'color':color, 
         'marker':marker, 
         'size':stroke_width, 
         'dash':dash, 
         'opacity':opacity, 
         'arrow':arrow}

    def CreateTangentCircle(self, point, other_line):
        """
        Computes the two circles that are tangent to 2 lines and intersect
        a point located on one of the two lines.
        """
        if math.isclose((self.point_distance(point)), 0, abs_tol=1e-10):
            I = Vector2D((point[0], point[1]))
            A = Vector2D((self.points[0][0], self.points[0][1]))
            B = Vector2D((self.points[1][0], self.points[1][1]))
            C = Vector2D((other_line.points[0][0], other_line.points[0][1]))
            D = Vector2D((other_line.points[1][0], other_line.points[1][1]))
        else:
            if math.isclose((other_line.point_distance(point)), 0, abs_tol=1e-10):
                I = Vector2D((point[0], point[1]))
                C = Vector2D((self.points[0][0], self.points[0][1]))
                D = Vector2D((self.points[1][0], self.points[1][1]))
                A = Vector2D((other_line.points[0][0], other_line.points[0][1]))
                B = Vector2D((other_line.points[1][0], other_line.points[1][1]))
            else:
                raise AttributeError("The point isn't on any of the two lines")
        new_u = Vector2D(B - A)
        new_u.Normalize()
        new_v = new_u.NormalVector(unit=True)
        new_basis = Frame2D(I, new_u, new_v)
        new_A = new_basis.NewCoordinates(A)
        new_B = new_basis.NewCoordinates(B)
        new_C = new_basis.NewCoordinates(C)
        new_D = new_basis.NewCoordinates(D)
        if new_C[1] == 0:
            if new_D[1] == 0:
                return (None, None)
        if math.isclose((self.DirectionVector(unit=True).Dot(other_line.NormalVector(unit=True))), 0, abs_tol=1e-06):
            segments_distance = abs(new_C[1] - new_A[1])
            r = segments_distance / 2
            new_circle_center = Point2D((0, npy.sign(new_C[1] - new_A[1]) * r))
            circle_center = new_basis.OldCoordinates(new_circle_center)
            circle = Circle2D(circle_center, r)
            return (
             circle, None)
        if math.isclose((self.DirectionVector(unit=True).Dot(other_line.DirectionVector(unit=True))), 0, abs_tol=1e-06):
            line_AB = Line2D(Point2D(new_A), Point2D(new_B))
            line_CD = Line2D(Point2D(new_C), Point2D(new_D))
            new_pt_K = Point2D.LinesIntersection(line_AB, line_CD)
            r = abs(new_pt_K[0])
            new_circle_center1 = Point2D((0, r))
            new_circle_center2 = Point2D((0, -r))
            circle_center1 = new_basis.OldCoordinates(new_circle_center1)
            circle_center2 = new_basis.OldCoordinates(new_circle_center2)
            circle1 = Circle2D(circle_center1, r)
            circle2 = Circle2D(circle_center2, r)
            return (
             circle1, circle2)
        line_AB = Line2D(Point2D(new_A), Point2D(new_B))
        line_CD = Line2D(Point2D(new_C), Point2D(new_D))
        new_pt_K = Point2D.LinesIntersection(line_AB, line_CD)
        pt_K = Point2D(new_basis.OldCoordinates(new_pt_K))
        if pt_K == I:
            return (None, None)
        new_u2 = Vector2D(pt_K - I)
        new_u2.Normalize()
        new_v2 = new_u2.NormalVector(unit=True)
        new_basis2 = Frame2D(I, new_u2, new_v2)
        new_A = new_basis2.NewCoordinates(A)
        new_B = new_basis2.NewCoordinates(B)
        new_C = new_basis2.NewCoordinates(C)
        new_D = new_basis2.NewCoordinates(D)
        new_pt_K = new_basis2.NewCoordinates(pt_K)
        teta1 = math.atan2(new_C[1], new_C[0] - new_pt_K[0])
        teta2 = math.atan2(new_D[1], new_D[0] - new_pt_K[0])
        if teta1 < 0:
            teta1 += math.pi
        elif teta2 < 0:
            teta2 += math.pi
        elif not math.isclose(teta1, teta2, abs_tol=1e-08):
            if math.isclose(teta1, (math.pi), abs_tol=1e-08) or math.isclose(teta1, 0.0, abs_tol=1e-08):
                teta = teta2
            else:
                if math.isclose(teta2, (math.pi), abs_tol=1e-08) or math.isclose(teta2, 0.0, abs_tol=1e-08):
                    teta = teta1
        else:
            teta = teta1
        r1 = new_pt_K[0] * math.sin(teta) / (1 + math.cos(teta))
        r2 = new_pt_K[0] * math.sin(teta) / (1 - math.cos(teta))
        new_circle_center1 = Point2D((0, -r1))
        new_circle_center2 = Point2D((0, r2))
        circle_center1 = new_basis2.OldCoordinates(new_circle_center1)
        circle_center2 = new_basis2.OldCoordinates(new_circle_center2)
        if new_basis.NewCoordinates(circle_center1)[1] > 0:
            circle1 = Circle2D(circle_center1, r1)
            circle2 = Circle2D(circle_center2, r2)
        else:
            circle1 = Circle2D(circle_center2, r2)
            circle2 = Circle2D(circle_center1, r1)
        return (circle1, circle2)


class LineSegment2D(Line2D):
    __doc__ = '\n    Define a line segment limited by two points\n    '

    def __init__(self, point1, point2, name=''):
        Line2D.__init__(self, point1, point2, name=name)

    def to_dict(self):
        dict_ = {}
        dict_['name'] = self.name
        dict_['point1'] = self.points[0].to_dict()
        dict_['point2'] = self.points[1].to_dict()
        dict_['object_class'] = 'volmdlr.core.LineSegment2D'
        return dict_

    @classmethod
    def dict_to_object(cls, dict_):
        return cls(point1=(Point2D.dict_to_object(dict_['point1'])), point2=(Point2D.dict_to_object(dict_['point2'])),
          name=(dict_['name']))

    def _get_geo_points(self):
        return self.points

    geo_points = property(_get_geo_points)

    def Length(self):
        return self.points[1].point_distance(self.points[0])

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        return self.points[0] + self.DirectionVector(unit=True) * curvilinear_abscissa

    def point_distance(self, point, return_other_point=False):
        """
        Computes the distance of a point to segment of line
        """
        if self.points[0] == self.points[1]:
            if return_other_point:
                return (
                 0, Point2D(point))
            return 0
        distance, point = LineSegment2DPointDistance([p.vector for p in self.points], point.vector)
        if return_other_point:
            return (
             distance, Point2D(point))
        return distance

    def PointProjection(self, point, curvilinear_abscissa=False):
        point, curv_abs = Line2D.PointProjection(self, point, True)
        if curv_abs <= 0.0:
            point = self.points[0]
            curv_abs = 0.0
        else:
            if curv_abs >= 1.0:
                point = self.points[1]
                curv_abs = 1.0
        if curvilinear_abscissa:
            return (
             point, curv_abs)
        return point

    def PointProjection2(self, point, curvilinear_abscissa=False):
        """
        If the projection falls outside the LineSegment2D, returns None.
        """
        point, curv_abs = Line2D.PointProjection(self, point, True)
        if curv_abs < 0 or curv_abs > 1:
            if curvilinear_abscissa:
                return (
                 None, curv_abs)
            return
        if curvilinear_abscissa:
            return (
             point, curv_abs)
        return point

    def line_intersection(self, line):
        point = Point2D.LinesIntersection(self, line)
        if point is not None:
            point_projection1 = self.PointProjection2(point)
            if point_projection1 is None:
                return
            if line.__class__ is LineSegment2D:
                point_projection2 = line.PointProjection2(point)
                if point_projection2 is None:
                    return
            return point_projection1
        return

    def MPLPlot(self, ax=None, color='k', arrow=False, width=None, plot_points=False):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
        else:
            fig = ax.figure
        p1, p2 = self.points
        if arrow:
            if plot_points:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, style='o-')
            else:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color)
            length = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
            if width is None:
                width = length / 1000.0
                head_length = length / 20.0
                head_width = head_length / 2.0
            else:
                head_width = 2 * width
                head_length = head_width
            ax.arrow((p1[0]), (p1[1]), ((p2[0] - p1[0]) / length * (length - head_length)), ((p2[1] - p1[1]) / length * (length - head_length)),
              head_width=head_width,
              fc='b',
              linewidth=0,
              head_length=head_length,
              width=width,
              alpha=0.3)
        else:
            if width is None:
                width = 1
            elif plot_points:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, marker='o', linewidth=width)
            else:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=width)
        return (
         fig, ax)

    def To3D(self, plane_origin, x1, x2):
        p3D = [p.To3D(plane_origin, x1, x2) for p in self.points]
        return LineSegment3D(*p3D, *(self.name,))

    def to_line(self):
        return Line2D(*self.points)

    def Rotation(self, center, angle, copy=True):
        if copy:
            return LineSegment2D(*[p.Rotation(center, angle, copy=True) for p in self.points])
        for p in self.points:
            p.Rotation(center, angle, copy=False)

    def Translation(self, offset, copy=True):
        if copy:
            return LineSegment2D(*[p.Translation(offset, copy=True) for p in self.points])
        for p in self.points:
            p.Translation(offset, copy=False)

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if side == 'old':
            if copy:
                return LineSegment2D(*[frame.OldCoordinates(p) for p in self.points])
            self.points = [frame.OldCoordinates(p) for p in self.points]
        if side == 'new':
            if copy:
                return LineSegment2D(*[frame.NewCoordinates(p) for p in self.points])
            self.points = [frame.NewCoordinates(p) for p in self.points]

    def GeoScript(self, primitive_index, points_indices):
        s = ('Line({}) = {{{}, {}}};\n'.format)(primitive_index, *points_indices)
        return (s, primitive_index + 1)

    def plot_data(self, marker=None, color='black', stroke_width=1, dash=False, opacity=1, arrow=False):
        return {'type':'line', 
         'data':[
          self.points[0].vector[0], self.points[0].vector[1],
          self.points[1].vector[0], self.points[1].vector[1]], 
         'color':color, 
         'marker':marker, 
         'size':stroke_width, 
         'dash':dash, 
         'opacity':opacity, 
         'arrow':arrow}

    def CreateTangentCircle(self, point, other_line):
        circle1, circle2 = Line2D.CreateTangentCircle(other_line, point, self)
        if circle1 is not None:
            point_J1, curv_abs1 = Line2D.PointProjection(self, circle1.center, True)
            if curv_abs1 < 0.0 or curv_abs1 > 1.0:
                circle1 = None
        if circle2 is not None:
            point_J2, curv_abs2 = Line2D.PointProjection(self, circle2.center, True)
            if curv_abs2 < 0.0 or curv_abs2 > 1.0:
                circle2 = None
        return (
         circle1, circle2)


class Arc2D(Primitive2D):
    __doc__ = '\n    angle: the angle measure always >= 0\n    '

    def __init__(self, start, interior, end, name=''):
        Primitive2D.__init__(self, name)
        self.interior = interior
        self.start = start
        self.end = end
        xi, yi = interior.vector
        xe, ye = end.vector
        xs, ys = start.vector
        A = npy.array([[2 * (xs - xi), 2 * (ys - yi)],
         [
          2 * (xs - xe), 2 * (ys - ye)]])
        b = -npy.array([xi ** 2 + yi ** 2 - xs ** 2 - ys ** 2,
         xe ** 2 + ye ** 2 - xs ** 2 - ys ** 2])
        self.center = Point2D(solve(A, b))
        r1 = self.start - self.center
        r2 = self.end - self.center
        ri = self.interior - self.center
        self.radius = r1.Norm()
        angle1 = math.atan2(r1.vector[1], r1.vector[0])
        anglei = math.atan2(ri.vector[1], ri.vector[0])
        angle2 = math.atan2(r2.vector[1], r2.vector[0])
        if anglei < angle1:
            trigowise_path = anglei + 2 * math.pi - angle1
            clockwise_path = angle1 - anglei
        else:
            trigowise_path = anglei - angle1
            clockwise_path = angle1 - anglei + 2 * math.pi
        if angle2 < anglei:
            trigowise_path += angle2 + 2 * math.pi - anglei
            clockwise_path += anglei - angle2
        else:
            trigowise_path += angle2 - anglei
            clockwise_path += anglei - angle2 + 2 * math.pi
        if clockwise_path > trigowise_path:
            self.is_trigo = True
            self.angle1 = angle1
            self.angle2 = angle2
            self.angle = trigowise_path
        else:
            self.is_trigo = False
            self.angle1 = angle2
            self.angle2 = angle1
            self.angle = clockwise_path

    def _get_points(self):
        return [
         self.start, self.interior, self.end]

    points = property(_get_points)

    def _get_geo_points(self):
        return [
         self.start, self.interior, self.end]

    geo_points = property(_get_geo_points)

    def tessellation_points(self, resolution_for_circle=40):
        number_points_tesselation = math.ceil(resolution_for_circle * abs(self.angle) / 2 / math.pi)
        if number_points_tesselation == 1:
            number_points_tesselation += 1
        l = self.Length()
        return [self.PointAtCurvilinearAbscissa(i / (number_points_tesselation - 1) * l) for i in range(number_points_tesselation)]

    def point_belongs(self, point):
        """
        Computes if the point belongs to the pizza slice drawn by the arc and its center
        """
        circle = Circle2D(self.center, self.radius)
        if not circle.point_belongs(point):
            return False
        vector_start = self.start - self.center
        vector_point = point - self.center
        vector_end = self.end - self.center
        if self.is_trigo:
            vector_start, vector_end = vector_end, vector_start
        arc_angle = clockwise_angle(vector_start, vector_end)
        point_angle = clockwise_angle(vector_start, vector_point)
        if point_angle <= arc_angle:
            return True

    def point_distance(self, point):
        vector_start = self.start - self.center
        vector_point = point - self.center
        vector_end = self.end - self.center
        if self.is_trigo:
            vector_start, vector_end = vector_end, vector_start
        arc_angle = clockwise_angle(vector_start, vector_end)
        point_angle = clockwise_angle(vector_start, vector_point)
        if point_angle <= arc_angle:
            return abs(LineSegment2D(point, self.center).Length() - self.radius)
        return min(LineSegment2D(point, self.start).Length(), LineSegment2D(point, self.end).Length())

    def line_intersection(self, line):
        points = self.tessellation_points()
        segments = []
        intersection_points = []
        for pt1, pt2 in zip(points[:-1], points[1:]):
            segments.append(LineSegment2D(pt1, pt2))

        for segment in segments:
            intersection_point = segment.line_intersection(line)
            if intersection_point is not None:
                intersection_points.append(intersection_point)

        return intersection_points

    def Length(self):
        return self.radius * abs(self.angle)

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        if self.is_trigo:
            return self.start.Rotation(self.center, curvilinear_abscissa / self.radius)
        return self.start.Rotation(self.center, -curvilinear_abscissa / self.radius)

    def MiddlePoint(self):
        l = self.Length()
        return self.PointAtCurvilinearAbscissa(0.5 * l)

    def GeoScript(self, primitive_index, points_indices):
        s = ('Circle({}) = {{{}, {}, {}}};\n'.format)(primitive_index, *points_indices)
        return (s, primitive_index + 1)

    def Area(self):
        if self.angle2 < self.angle1:
            angle = self.angle2 + 2 * math.pi - self.angle1
        else:
            angle = self.angle2 - self.angle1
        return self.radius ** 2 * angle / 2

    def CenterOfMass(self):
        u = self.MiddlePoint() - self.center
        u.Normalize()
        alpha = abs(self.angle)
        return self.center + 4 / (3 * alpha) * self.radius * math.sin(alpha * 0.5) * u

    def MPLPlot(self, ax=None, color='k'):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
        else:
            fig = ax.figure
        pc = self.center.vector
        ax.add_patch(Arc(pc, (2 * self.radius), (2 * self.radius), angle=0, theta1=(self.angle1 * 0.5 / math.pi * 360),
          theta2=(self.angle2 * 0.5 / math.pi * 360),
          color=color))
        return (
         fig, ax)

    def To3D(self, plane_origin, x, y):
        ps = self.start.To3D(plane_origin, x, y)
        pi = self.interior.To3D(plane_origin, x, y)
        pe = self.end.To3D(plane_origin, x, y)
        return Arc3D(ps, pi, pe, self.name)

    def Rotation(self, center, angle, copy=True):
        if copy:
            return Arc2D(*[p.Rotation(center, angle, copy=True) for p in [self.start, self.interior, self.end]])
        (self.__init__)(*[p.Rotation(center, angle, copy=True) for p in [self.start, self.interior, self.end]])

    def Translation(self, offset, copy=True):
        if copy:
            return Arc2D(*[p.Translation(offset, copy=True) for p in [self.start, self.interior, self.end]])
        (self.__init__)(*[p.Translation(offset, copy=True) for p in [self.start, self.interior, self.end]])

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            return Arc2D(*[p.frame_mapping(frame, side, copy=True) for p in [self.start, self.interior, self.end]])
        (self.__init__)(*[p.frame_mapping(frame, side, copy=True) for p in [self.start, self.interior, self.end]])

    def SecondMomentArea(self, point):
        """
        Second moment area of part of disk
        """
        if self.angle2 < self.angle1:
            angle2 = self.angle2 + 2 * math.pi
        else:
            angle2 = self.angle2
        angle1 = self.angle1
        Ix = self.radius ** 4 / 8 * (angle2 - angle1 + 0.5 * (math.sin(2 * angle1) - math.sin(2 * angle2)))
        Iy = self.radius ** 4 / 8 * (angle2 - angle1 + 0.5 * (math.sin(2 * angle2) - math.sin(2 * angle1)))
        Ixy = self.radius ** 4 / 8 * (math.cos(angle1) ** 2 - math.cos(angle2) ** 2)
        Ic = npy.array([[Ix, Ixy], [Ixy, Iy]])
        return geometry.Huygens2D(Ic, self.Area(), self.center, point)

    def Discretise(self, num=10):
        list_node = []
        if self.angle1 < 0 and self.angle2 > 0:
            delta_angle = -self.angle1 + self.angle2
        else:
            if self.angle1 > 0 and self.angle2 < 0:
                delta_angle = 2 * npy.pi + self.angle2 - self.angle1
            else:
                delta_angle = self.angle2 - self.angle1
        for angle in npy.arange(self.angle1, self.angle1 + delta_angle, delta_angle / (num * 1.0)):
            list_node.append(Point2D(self.center + self.radius * Vector2D((npy.cos(angle), npy.sin(angle)))))

        list_node.append(Point2D(self.center + self.radius * Vector2D((npy.cos(self.angle1 + delta_angle), npy.sin(self.angle1 + delta_angle)))))
        if list_node[0] == self.start:
            return list_node
        return list_node[::-1]

    def plot_data(self, marker=None, color='black', stroke_width=1, dash=False, opacity=1):
        list_node = self.Discretise()
        data = []
        for nd in list_node:
            data.append({'x':nd.vector[0],  'y':nd.vector[1]})

        return {'type':'arc', 
         'cx':self.center.vector[0], 
         'cy':self.center.vector[1], 
         'data':data, 
         'r':self.radius, 
         'color':color, 
         'opacity':opacity, 
         'size':stroke_width, 
         'dash':None, 
         'marker':marker, 
         'angle1':self.angle1, 
         'angle2':self.angle2}


class Circle2D(Contour2D):
    _non_serializable_attributes = [
     'internal_arcs', 'external_arcs', 'polygon', 'straight_line_contour_polygon', 'primitives']

    def __init__(self, center, radius, name=''):
        self.center = center
        self.radius = radius
        self.utd_geo_points = False
        Contour2D.__init__(self, [self], name=name)

    def _get_geo_points(self):
        if not self.utd_geo_points:
            self._geo_start = self.center + self.radius * Point2D((1, 0))
            self.utd_geo_points = True
        return [
         self._geo_start, self.center, self._geo_start]

    geo_points = property(_get_geo_points)

    def tessellation_points(self, resolution=40):
        return [self.center + self.radius * math.cos(teta) * Vector2D((1, 0)) + self.radius * math.sin(teta) * Vector2D((0,
                                                                                                                         1)) for teta in npy.linspace(0, 2 * math.pi, resolution + 1)][:-1]

    def point_belongs(self, point):
        return point.point_distance(self.center) <= self.radius

    def Length(self):
        return 2 * math.pi * self.radius

    def GeoScript(self, primitive_index, points_indices):
        s = ('Circle({}) = {{{}, {}, {}}};\n'.format)(primitive_index, *points_indices)
        return (s, primitive_index + 1)

    def MPLPlot(self, ax, linestyle='-', color='k', linewidth=1):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
        else:
            fig = ax.figure
        pc = self.center.vector
        if self.radius > 0:
            ax.add_patch(Arc(pc, (2 * self.radius),
              (2 * self.radius),
              angle=0,
              theta1=0,
              theta2=360,
              color=color,
              linestyle=linestyle,
              linewidth=linewidth))
        return (
         fig, ax)

    def To3D(self, plane_origin, x, y):
        normal = x.Cross(y)
        pc = self.center.To3D(plane_origin, x, y)
        return Circle3D(pc, self.radius, normal, self.name)

    def Rotation(self, center, angle, copy=True):
        if copy:
            return Circle2D(self.center.Rotation(center, angle, copy=True), self.radius)
        self.center.Rotation(center, angle, copy=False)
        self.utd_geo_points = False

    def Translation(self, offset, copy=True):
        if copy:
            return Circle2D(self.center.Translation(offset, copy=True), self.radius)
        self.center.Translation(offset, copy=False)
        self.utd_geo_points = False

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if side == 'old':
            if copy:
                return Circle2D(frame.OldCoordinates(self.center), self.radius)
            self.center = frame.OldCoordinates(self.center)
        if side == 'new':
            if copy:
                return Circle2D(frame.NewCoordinates(self.center), self.radius)
            self.points = frame.NewCoordinates(self.center)

    def Area(self):
        return math.pi * self.radius ** 2

    def SecondMomentArea(self, point):
        """
        Second moment area of part of disk
        """
        I = math.pi * self.radius ** 4 / 4
        Ic = npy.array([[I, 0], [0, I]])
        return geometry.Huygens2D(Ic, self.Area(), self.center, point)

    def CenterOfMass(self):
        return self.center

    def point_symmetric(self, point):
        center = 2 * point - self.center
        return Circle2D(center, self.radius)

    def plot_data(self, marker=None, color='black', stroke_width=1, opacity=1, fill=None):
        return {'type':'circle', 
         'cx':self.center.vector[0], 
         'cy':self.center.vector[1], 
         'r':self.radius, 
         'color':color, 
         'opacity':opacity, 
         'size':stroke_width, 
         'dash':None, 
         'fill':fill}


class Polygon2D(Contour2D):

    def __init__(self, points, name=''):
        self.points = points
        self.line_segments = self._LineSegments()
        Contour2D.__init__(self, self.line_segments, name)

    def copy(self):
        points = [p.copy() for p in self.points]
        return Polygon2D(points, self.name)

    def __hash__(self):
        return sum([hash(p) for p in self.points])

    def __eq__(self, other_):
        equal = True
        for point, other_point in zip(self.points, other_.points):
            equal = equal and point == other_point

        return equal

    def Area(self):
        x = [point.vector[0] for point in self.points]
        y = [point.vector[1] for point in self.points]
        return 0.5 * npy.abs(npy.dot(x, npy.roll(y, 1)) - npy.dot(y, npy.roll(x, 1)))

    def CenterOfMass(self):
        x = [point.vector[0] for point in self.points]
        y = [point.vector[1] for point in self.points]
        xi_xi1 = x + npy.roll(x, -1)
        yi_yi1 = y + npy.roll(y, -1)
        xi_yi1 = npy.multiply(x, npy.roll(y, -1))
        xi1_yi = npy.multiply(npy.roll(x, -1), y)
        a = 0.5 * npy.sum(xi_yi1 - xi1_yi)
        if not math.isclose(a, 0, abs_tol=1e-08):
            cx = npy.sum(npy.multiply(xi_xi1, xi_yi1 - xi1_yi)) / 6.0 / a
            cy = npy.sum(npy.multiply(yi_yi1, xi_yi1 - xi1_yi)) / 6.0 / a
            return Point2D((cx, cy))
        raise NotImplementedError

    def PointBelongs(self, point):
        """
        Ray casting algorithm copied from internet...
        """
        return PolygonPointBelongs(point.vector, [p.vector for p in self.points])

    def SecondMomentArea(self, point):
        Ix, Iy, Ixy = (0, 0, 0)
        for pi, pj in zip(self.points, self.points[1:] + [self.points[0]]):
            xi, yi = pi.vector - point.vector
            xj, yj = pj.vector - point.vector
            Ix += (yi ** 2 + yi * yj + yj ** 2) * (xi * yj - xj * yi)
            Iy += (xi ** 2 + xi * xj + xj ** 2) * (xi * yj - xj * yi)
            Ixy += (xi * yj + 2 * xi * yi + 2 * xj * yj + xj * yi) * (xi * yj - xj * yi)

        if Ix < 0:
            Ix = -Ix
            Iy = -Iy
            Ixy = -Ixy
        return npy.array([[Ix / 12.0, Ixy / 24.0], [Ixy / 24.0, Iy / 12.0]])

    def _LineSegments(self):
        lines = []
        for p1, p2 in zip(self.points, self.points[1:] + [self.points[0]]):
            lines.append(LineSegment2D(p1, p2))

        return lines

    def Rotation(self, center, angle, copy=True):
        if copy:
            return Polygon2D([p.Rotation(center, angle, copy=True) for p in self.points])
        for p in self.points:
            p.Rotation(center, angle, copy=False)

    def Translation(self, offset, copy=True):
        if copy:
            return Polygon2D([p.Translation(offset, copy=True) for p in self.points])
        for p in self.points:
            p.Translation(offset, copy=False)

    def PointBorderDistance(self, point, return_other_point=False):
        """
        Compute the distance to the border distance of polygon
        Output is always positive, even if the point belongs to the polygon
        """
        d_min, other_point_min = self.line_segments[0].point_distance(point, return_other_point=True)
        for line in self.line_segments[1:]:
            d, other_point = line.point_distance(point, return_other_point=True)
            if d < d_min:
                d_min = d
                other_point_min = other_point

        if return_other_point:
            return (
             d_min, other_point_min)
        return d_min

    def SelfIntersect(self):
        epsilon = 0
        sorted_index = sorted((range(len(self.points))), key=(lambda p: (self.points[p][0], self.points[p][1])))
        nb = len(sorted_index)
        segments = []
        deleted = []
        while len(sorted_index) != 0:
            if sorted_index[0] - 1 < 0:
                segments.append((sorted_index[0], nb - 1))
            else:
                segments.append((sorted_index[0], sorted_index[0] - 1))
            if sorted_index[0] >= len(self.points) - 1:
                segments.append((sorted_index[0], 0))
            else:
                segments.append((sorted_index[0], sorted_index[0] + 1))
            to_del = []
            for index in deleted:
                if abs(index - sorted_index[0]) == 1 or abs(index - sorted_index[0]) == nb - 1:
                    to_del.append((index, sorted_index[0]))
                    to_del.append((sorted_index[0], index))

            deleted.append(sorted_index[0])
            sorted_index.pop(0)
            index_to_del = []
            for i, segment in enumerate(segments):
                for seg_to_del in to_del:
                    if segment == seg_to_del:
                        index_to_del.append(i)

            for index in index_to_del[::-1]:
                segments.pop(index)

            for segment1 in segments:
                for segment2 in segments:
                    if segment1[0] != segment2[0] and segment1[1] != segment2[1] and segment1[0] != segment2[1] and segment1[1] != segment2[0]:
                        line1 = LineSegment2D(Point2D(self.points[segment1[0]]), Point2D(self.points[segment1[1]]))
                        line2 = LineSegment2D(Point2D(self.points[segment2[0]]), Point2D(self.points[segment2[1]]))
                        p, a, b = Point2D.LinesIntersection(line1, line2, True)
                        if p is not None and a >= 0 + epsilon and a <= 1 - epsilon and b >= 0 + epsilon and b <= 1 - epsilon:
                            return (
                             True, line1, line2)

        return (False, None, None)

    def plot_data(self, marker=None, color='black', stroke_width=1, opacity=1):
        data = []
        for nd in self.points:
            data.append({'x':nd.vector[0],  'y':nd.vector[1]})

        return {'type':'path', 
         'data':data, 
         'color':color, 
         'size':stroke_width, 
         'dash':None, 
         'marker':marker, 
         'opacity':opacity}


class Primitive3D(dc.DessiaObject):

    def __init__(self, basis_primitives=None, name=''):
        self.name = name
        self.primitives = basis_primitives
        if basis_primitives is None:
            self.primitives = []


class Plane3D(Primitive3D):

    def __init__(self, origin, vector1, vector2, name=''):
        self.origin = Point3D(origin.vector)
        vector1 = Vector3D(vector1.vector)
        vector1.Normalize()
        vector2 = Vector3D(vector2.vector)
        vector2.Normalize()
        self.vectors = [vector1, vector2]
        self.name = name
        self.normal = self.vectors[0].Cross(self.vectors[1])
        self.normal.Normalize()

    def __hash__(self):
        return sum([hash(v) for v in self.vectors]) + hash(self.origin)

    def __eq__(self, other_):
        equal = self.origin == other_.origin and self.vectors[0] == other_.vectors[0] and self.vectors[1] == other_.vectors[1]
        return equal

    def to_dict(self):
        dict_ = dc.DessiaObject.base_dict(self)
        dict_['vector1'] = self.vectors[0].to_dict()
        dict_['vector2'] = self.vectors[1].to_dict()
        dict_['origin'] = self.origin.to_dict()
        dict_['name'] = self.name
        dict_['object_class'] = 'volmdlr.core.Plane3D'
        return dict_

    @classmethod
    def from_step(cls, arguments, object_dict):
        frame3d = object_dict[arguments[1]]
        origin = frame3d.origin
        vector1 = frame3d.u
        vector2 = frame3d.v
        return cls(origin, vector1, vector2, arguments[0][1:-1])

    @classmethod
    def from_3_points(cls, point1, point2, point3):
        vector1 = point2 - point1
        vector2 = point3 - point1
        vector1.Normalize()
        vector2.Normalize()
        normal = vector1.Cross(vector2)
        normal.Normalize()
        vector = normal.Cross(vector1)
        return cls(point1.copy(), vector1.copy(), vector.copy())

    @classmethod
    def from_normal(cls, point, normal):
        v1 = normal.DeterministicUnitNormalVector()
        v2 = v1.Cross(normal)
        return cls(point, v1, v2)

    @classmethod
    def from_points(cls, points):
        if len(points) < 3:
            raise ValueError
        else:
            if len(points) == 3:
                return cls.from_3_points(Point3D(points[0].vector), Vector3D(points[1].vector), Vector3D(points[2].vector))
            points = [p.copy() for p in points]
            indexes_to_del = []
            for i, point in enumerate(points[1:]):
                if point == points[0]:
                    indexes_to_del.append(i)

            for index in indexes_to_del[::-1]:
                del points[index + 1]

            origin = Point3D(points[0].vector)
            vector1 = Vector3D(points[1] - origin)
            vector1.Normalize()
            vector2_min = Vector3D(points[2] - origin)
            vector2_min.Normalize()
            dot_min = abs(vector1.Dot(vector2_min))
            for point in points[3:]:
                vector2 = Vector3D(point - origin)
                vector2.Normalize()
                dot = abs(vector1.Dot(vector2))
                if dot < dot_min:
                    vector2_min = vector2
                    dot_min = dot

            return cls.from_3_points(origin, vector1 + origin, vector2_min + origin)

    def point_on_plane(self, point):
        if math.isclose((self.normal.Dot(point - self.origin)), 0, abs_tol=1e-06):
            return True
        return False

    def line_intersection(self, line):
        u = line.points[1] - line.points[0]
        w = line.points[0] - self.origin
        if math.isclose((self.normal.Dot(u)), 0, abs_tol=1e-08):
            return
        intersection_abscissea = -self.normal.Dot(w) / self.normal.Dot(u)
        return line.points[0] + intersection_abscissea * u

    def linesegment_intersection(self, linesegment, abscissea=False):
        u = linesegment.points[1] - linesegment.points[0]
        w = linesegment.points[0] - self.origin
        normalDotu = self.normal.Dot(u)
        if math.isclose(normalDotu, 0, abs_tol=1e-08):
            if abscissea:
                return (None, None)
            return
        intersection_abscissea = -self.normal.Dot(w) / normalDotu
        if intersection_abscissea < 0 or intersection_abscissea > 1:
            if abscissea:
                return (None, None)
            return
        if abscissea:
            return (
             linesegment.points[0] + intersection_abscissea * u, intersection_abscissea)
        return linesegment.points[0] + intersection_abscissea * u

    def equation_coefficients(self):
        """
        returns the a,b,c,d coefficient from equation ax+by+cz+d = 0
        """
        a, b, c = self.normal.vector
        d = -self.origin.Dot(self.normal)
        return (a, b, c, d)

    def plane_intersection(self, other_plane):
        line_direction = self.normal.Cross(other_plane.normal)
        if line_direction.Norm() < 1e-06:
            return
        a1, b1, c1, d1 = self.equation_coefficients()
        a2, b2, c2, d2 = other_plane.equation_coefficients()
        if a1 * b2 - a2 * b1 != 0.0:
            x0 = (b1 * d2 - b2 * d1) / (a1 * b2 - a2 * b1)
            y0 = (a2 * d1 - a1 * d2) / (a1 * b2 - a2 * b1)
            point1 = Point3D((x0, y0, 0))
        else:
            y0 = (b2 * d2 - c2 * d1) / (b1 * c2 - c1 * b2)
            z0 = (c1 * d1 - b1 * d2) / (b1 * c2 - c1 * b2)
            point1 = Point3D((0, y0, z0))
        point2 = point1 + line_direction
        return Line3D(point1, point2)

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            new_origin = self.origin.Rotation(center, axis, angle, True)
            new_vector1 = self.vectors[0].Rotation(center, axis, angle, True)
            new_vector2 = self.vectors[1].Rotation(center, axis, angle, True)
            return Plane3D(new_origin, new_vector1, new_vector2, self.name)
        self.origin.Rotation(center, axis, angle, True)
        self.vectors[0].Rotation(center, axis, angle, True)
        self.vectors[1].Rotation(center, axis, angle, True)

    def Translation(self, offset, copy=True):
        if copy:
            new_origin = self.origin.Translation(offset, True)
            return Plane3D(new_origin, self.vectors[0], self.vectors[1], self.name)
        self.origin.Translation(offset, False)

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if side == 'old':
            new_origin = frame.OldCoordinates(self.origin)
            new_vector1 = frame.Basis().OldCoordinates(self.vectors[0])
            new_vector2 = frame.Basis().OldCoordinates(self.vectors[1])
            if copy:
                return Plane3D(new_origin, new_vector1, new_vector2, self.name)
            self.origin = new_origin
            self.vectors = [new_vector1, new_vector2]
            self.normal = frame.Basis().OldCoordinates(self.normal)
            self.normal.Normalize()
        if side == 'new':
            new_origin = frame.NewCoordinates(self.origin)
            new_vector1 = frame.Basis().NewCoordinates(self.vectors[0])
            new_vector2 = frame.Basis().NewCoordinates(self.vectors[1])
            if copy:
                return Plane3D(new_origin, new_vector1, new_vector2, self.name)
            self.origin = new_origin
            self.vectors = [new_vector1, new_vector2]
            self.normal = frame.Basis().NewCoordinates(self.normal)
            self.normal.Normalize()

    def copy(self):
        new_origin = self.origin.Copy()
        new_vector1 = self.vectors[0].Copy()
        new_vector2 = self.vectors[1].Copy()
        return Plane3D(new_origin, new_vector1, new_vector2, self.name)

    def MPLPlot(self, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.figure
        self.origin.MPLPlot(ax)
        self.vectors[0].MPLPlot(ax, starting_point=(self.origin), color='r')
        self.vectors[1].MPLPlot(ax, starting_point=(self.origin), color='g')
        return (fig, ax)

    def Babylon(self):
        s = 'var myPlane = BABYLON.MeshBuilder.CreatePlane("myPlane", {width: 0.5, height: 0.5, sideOrientation: BABYLON.Mesh.DOUBLESIDE}, scene);\n'
        s += 'myPlane.setPositionWithLocalVector(new BABYLON.Vector3({},{},{}));\n'.format(self.origin[0], self.origin[1], self.origin[2])
        s += 'var axis1 = new BABYLON.Vector3({}, {}, {});\n'.format(self.vectors[0][0], self.vectors[0][1], self.vectors[0][2])
        s += 'var axis2 = new BABYLON.Vector3({}, {}, {});\n'.format(self.vectors[1][0], self.vectors[1][1], self.vectors[1][2])
        s += 'var axis3 = new BABYLON.Vector3({}, {}, {});\n'.format(self.normal[0], self.normal[1], self.normal[2])
        s += 'var orientation = BABYLON.Vector3.RotationFromAxis(axis1, axis2, axis3);\n'
        s += 'myPlane.rotation = orientation;\n'
        s += 'var planemat = new BABYLON.StandardMaterial("planemat", scene);\n'
        s += 'planemat.alpha = 0.4;\n'
        s += 'myPlane.material = planemat;\n'
        return s


PLANE3D_OXY = Plane3D(O3D, X3D, Y3D)
PLANE3D_OYZ = Plane3D(O3D, Y3D, Z3D)
PLANE3D_OZX = Plane3D(O3D, Z3D, X3D)
XYZ = Basis3D(X3D, Y3D, Z3D)
YZX = Basis3D(Y3D, Z3D, X3D)
ZXY = Basis3D(Z3D, X3D, Y3D)
OXYZ = Frame3D(O3D, X3D, Y3D, Z3D)
OYZX = Frame3D(O3D, Y3D, Z3D, X3D)
OZXY = Frame3D(O3D, Z3D, X3D, Y3D)

class Line3D(Primitive3D, Line):
    _non_eq_attributes = [
     'name', 'basis_primitives', 'bounding_box']

    def __init__(self, point1, point2, name=''):
        Primitive3D.__init__(self, basis_primitives=[point1, point2], name=name)
        self.points = [point1, point2]
        self.bounding_box = self._bounding_box()

    def __hash__(self):
        return sum([hash(p) for p in self.points]) + hash(self.bounding_box)

    def to_dict(self):
        dict_ = {}
        dict_['name'] = self.name
        dict_['point1'] = self.points[0].to_dict()
        dict_['point2'] = self.points[1].to_dict()
        return dict_

    def _bounding_box(self):
        points = self.points
        xmin = min([pt[0] for pt in points])
        xmax = max([pt[0] for pt in points])
        ymin = min([pt[1] for pt in points])
        ymax = max([pt[1] for pt in points])
        zmin = min([pt[2] for pt in points])
        zmax = max([pt[2] for pt in points])
        return BoundingBox(xmin, xmax, ymin, ymax, zmin, zmax)

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        return self.points[0] + (self.points[1] - self.points[0]) * curvilinear_abscissa

    def MPLPlot(self, ax=None, color='k', dashed=True):
        if ax is None:
            fig = plt.figure()
            ax = Axes3D(fig)
        else:
            fig = ax.figure
        x = [p.vector[0] for p in self.points]
        y = [p.vector[1] for p in self.points]
        z = [p.vector[2] for p in self.points]
        ax.plot(x, y, z, 'ok')
        u = self.points[1] - self.points[0]
        x1, y1, z1 = (self.points[0] - 3 * u).vector
        x2, y2, z2 = (self.points[1] + 3 * u).vector
        if dashed:
            ax.plot([x1, x2], [y1, y2], [z1, z2], color=color, dashes=[30, 5, 10, 5])
        else:
            ax.plot([x1, x2], [y1, y2], [z1, z2], color=color)
        return (
         fig, ax)

    def PlaneProjection2D(self, x, y):
        return Line2D(self.points[0].PlaneProjection2D(x, y), self.points[1].PlaneProjection2D(x, y))

    def MinimumDistancePoints(self, other_line):
        """
        Returns the points on this line and the other line that are the closest
        of lines
        """
        u = self.points[1] - self.points[0]
        v = other_line.points[1] - other_line.points[0]
        w = self.points[0] - other_line.points[0]
        a = u.Dot(u)
        b = u.Dot(v)
        c = v.Dot(v)
        d = u.Dot(w)
        e = v.Dot(w)
        s = (b * e - c * d) / (a * c - b ** 2)
        t = (a * e - b * d) / (a * c - b ** 2)
        p1 = self.points[0] + s * u
        p2 = other_line.points[0] + t * v
        return (p1, p2)

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            return Line3D(*[p.Rotation(center, axis, angle, copy=True) for p in self.points])
        for p in self.points:
            p.Rotation(center, axis, angle, copy=False)

    def Translation(self, offset, copy=True):
        if copy:
            return Line3D(*[p.Translation(offset, copy=True) for p in self.points])
        for p in self.points:
            p.Translation(offset, copy=False)

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if side == 'old':
            if copy:
                return Line3D(*[frame.OldCoordinates(p) for p in self.points])
            for p in self.points:
                self.points = [frame.OldCoordinates(p) for p in self.points]

        if side == 'new':
            if copy:
                return Line3D(*[frame.NewCoordinates(p) for p in self.points])
            for p in self.points:
                self.points = [frame.NewCoordinates(p) for p in self.points]

    def copy(self):
        return Line3D(*[p.Copy() for p in self.points])

    @classmethod
    def from_step(cls, arguments, object_dict):
        point1 = object_dict[arguments[1]]
        direction = object_dict[arguments[2]]
        point2 = point1 + direction
        return cls(point1, point2, arguments[0][1:-1])


class BSplineCurve3D(Primitive3D):

    def __init__(self, degree, control_points, knot_multiplicities, knots, weights=None, periodic=False, name=''):
        Primitive3D.__init__(self, basis_primitives=control_points, name=name)
        self.control_points = control_points
        self.degree = degree
        knots = standardize_knot_vector(knots)
        self.knots = knots
        self.knot_multiplicities = knot_multiplicities
        self.weights = weights
        self.periodic = periodic
        self.name = name
        curve = NURBS.Curve()
        curve.degree = degree
        if weights is None:
            P = [(control_points[i][0], control_points[i][1], control_points[i][2]) for i in range(len(control_points))]
            curve.ctrlpts = P
        else:
            Pw = [(control_points[i][0] * weights[i], control_points[i][1] * weights[i], control_points[i][2] * weights[i], weights[i]) for i in range(len(control_points))]
            curve.ctrlptsw = Pw
        knot_vector = []
        for i, knot in enumerate(knots):
            knot_vector.extend([knot] * knot_multiplicities[i])

        curve.knotvector = knot_vector
        curve.delta = 0.01
        curve_points = curve.evalpts
        self.curve = curve
        self.points = [Point3D((p[0], p[1], p[2])) for p in curve_points]

    def FreeCADExport(self, ip, ndigits=3):
        name = 'primitive{}'.format(ip)
        points = '['
        for i in range(len(self.control_points)):
            point = 'fc.Vector({},{},{}),'.format(self.control_points[i][0], self.control_points[i][1], self.control_points[i][2])
            points += point

        points = points[:-1]
        points += ']'
        return '{} = Part.BSplineCurve({},{},{},{},{},{},{})\n'.format(name, points, self.knot_multiplicities, self.knots, self.periodic, self.degree, self.weights, False)

    @classmethod
    def from_step(cls, arguments, object_dict):
        name = arguments[0][1:-1]
        degree = int(arguments[1])
        points = [object_dict[int(i[1:])] for i in arguments[2]]
        curve_form = arguments[3]
        if arguments[4] == '.F.':
            closed_curve = False
        else:
            if arguments[4] == '.T.':
                closed_curve = True
            else:
                raise ValueError
        self_intersect = arguments[5]
        knot_multiplicities = [int(i) for i in arguments[6][1:-1].split(',')]
        knots = [float(i) for i in arguments[7][1:-1].split(',')]
        knot_spec = arguments[8]
        knot_vector = []
        for i, knot in enumerate(knots):
            knot_vector.extend([knot] * knot_multiplicities[i])

        if 9 in range(len(arguments)):
            weight_data = [float(i) for i in arguments[9][1:-1].split(',')]
        else:
            weight_data = None
        closed_curve = False
        return cls(degree, points, knot_multiplicities, knots, weight_data, closed_curve, name)

    def point_distance(self, pt1):
        distances = []
        for point in self.points:
            distances.append(pt1.point_distance(point))

        return min(distances)

    def Rotation(self, center, axis, angle, copy=True):
        new_control_points = [p.Rotation(center, axis, angle, True) for p in self.control_points]
        new_BSplineCurve3D = BSplineCurve3D(self.degree, new_control_points, self.knot_multiplicities, self.knots, self.weights, self.periodic, self.name)
        if copy:
            return new_BSplineCurve3D
        self.control_points = new_control_points
        self.curve = new_BSplineCurve3D.curve
        self.points = new_BSplineCurve3D.points

    def Translation(self, offset, copy=True):
        new_control_points = [p.Translation(offset, True) for p in self.control_points]
        new_BSplineCurve3D = BSplineCurve3D(self.degree, new_control_points, self.knot_multiplicities, self.knots, self.weights, self.periodic, self.name)
        if copy:
            return new_BSplineCurve3D
        self.control_points = new_control_points
        self.curve = new_BSplineCurve3D.curve
        self.points = new_BSplineCurve3D.points


class Arc3D(Primitive3D):
    __doc__ = '\n    An arc is defined by a starting point, an end point and an interior point\n    '

    def __init__(self, start, interior, end, name=''):
        self.start = start
        self.interior = interior
        self.end = end
        u1 = self.interior - self.start
        u2 = self.interior - self.end
        u1.Normalize()
        u2.Normalize()
        n = u2.Cross(u1)
        n.Normalize()
        self.normal = n
        v1 = n.Cross(u1)
        v2 = n.Cross(u2)
        p11 = 0.5 * (start + interior)
        p12 = p11 + v1
        p21 = 0.5 * (end + interior)
        p22 = p21 + v2
        l1 = Line3D(p11, p12)
        l2 = Line3D(p21, p22)
        c1, _ = l1.MinimumDistancePoints(l2)
        self.center = c1
        self.radius = (self.center - self.start).Norm()
        r1 = self.start.To2D(self.center, u1, v1)
        r2 = self.end.To2D(self.center, u1, v1)
        ri = self.interior.To2D(self.center, u1, v1)
        angle1 = math.atan2(r1.vector[1], r1.vector[0])
        anglei = math.atan2(ri.vector[1], ri.vector[0])
        angle2 = math.atan2(r2.vector[1], r2.vector[0])
        if anglei < angle1:
            trigowise_path = anglei + 2 * math.pi - angle1
            clockwise_path = angle1 - anglei
        else:
            trigowise_path = anglei - angle1
            clockwise_path = angle1 - anglei + 2 * math.pi
        if angle2 < anglei:
            trigowise_path += angle2 + 2 * math.pi - anglei
            clockwise_path += anglei - angle2
        else:
            trigowise_path += angle2 - anglei
            clockwise_path += anglei - angle2 + 2 * math.pi
        if clockwise_path > trigowise_path:
            self.is_trigo = True
            self.angle = trigowise_path
        else:
            self.is_trigo = False
            self.angle = clockwise_path
        Primitive3D.__init__(self, basis_primitives=(self.tessellation_points()), name=name)

    def _get_points(self):
        return self.tessellation_points()

    points = property(_get_points)

    def tessellation_points(self, resolution_for_circle=40):
        number_points_tesselation = math.ceil(resolution_for_circle * abs(0.5 * self.angle / math.pi))
        l = self.Length()
        tessellation_points_3D = [self.PointAtCurvilinearAbscissa(l * i / number_points_tesselation) for i in range(number_points_tesselation + 1)]
        return tessellation_points_3D

    def Length(self):
        return self.radius * abs(self.angle)

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        return self.start.Rotation(self.center, self.normal, curvilinear_abscissa / self.radius)

    def Rotation(self, rot_center, axis, angle, copy=True):
        if copy:
            new_start = self.start.Rotation(rot_center, axis, angle, True)
            new_interior = self.interior.Rotation(rot_center, axis, angle, True)
            new_end = self.end.Rotation(rot_center, axis, angle, True)
            return Arc3D(new_start, new_interior, new_end, self.name)
        self.center.Rotation(rot_center, axis, angle, False)
        self.start.Rotation(rot_center, axis, angle, False)
        self.interior.Rotation(rot_center, axis, angle, False)
        self.end.Rotation(rot_center, axis, angle, False)
        [p.Rotation(rot_center, axis, angle, False) for p in self.primitives]

    def Translation(self, offset, copy=True):
        if copy:
            new_start = self.start.Translation(offset, True)
            new_interior = self.interior.Translation(offset, True)
            new_end = self.end.Translation(offset, True)
            return Arc3D(new_start, new_interior, new_end, self.name)
        self.center.Translation(offset, False)
        self.start.Translation(offset, False)
        self.interior.Translation(offset, False)
        self.end.Translation(offset, False)
        [p.Translation(offset, False) for p in self.primitives]

    def MPLPlot(self, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = Axes3D(fig)
        else:
            fig = None
        ax.plot([self.interior[0]], [self.interior[1]], [self.interior[2]], color='b')
        ax.plot([self.start[0]], [self.start[1]], [self.start[2]], c='r')
        ax.plot([self.end[0]], [self.end[1]], [self.end[2]], c='r')
        ax.plot([self.interior[0]], [self.interior[1]], [self.interior[2]], c='g')
        x = []
        y = []
        z = []
        for px, py, pz in self.tessellation_points():
            x.append(px)
            y.append(py)
            z.append(pz)

        ax.plot(x, y, z, 'k')
        return (fig, ax)

    def MPLPlot2D(self, x3d, y3D, ax, color='k'):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.figure
        l = self.Length()
        x = []
        y = []
        for i in range(30):
            p = self.PointAtCurvilinearAbscissa(i / 29.0 * l)
            xi, yi = p.PlaneProjection2D(X3D, Y3D)
            x.append(xi)
            y.append(yi)

        ax.plot(x, y, color=color)
        return (
         fig, ax)

    def FreeCADExport(self, name, ndigits=6):
        xs, ys, zs = round(1000 * self.start, ndigits).vector
        xi, yi, zi = round(1000 * self.interior, ndigits).vector
        xe, ye, ze = round(1000 * self.end, ndigits).vector
        return '{} = Part.Arc(fc.Vector({},{},{}),fc.Vector({},{},{}),fc.Vector({},{},{}))\n'.format(name, xs, ys, zs, xi, yi, zi, xe, ye, ze)


class BSplineSurface3D(Primitive3D):

    def __init__(self, degree_u, degree_v, control_points, nb_u, nb_v, u_multiplicities, v_multiplicities, u_knots, v_knots, weights=None, name=''):
        Primitive3D.__init__(self, basis_primitives=control_points, name=name)
        self.control_points = control_points
        self.degree_u = degree_u
        self.degree_v = degree_v
        self.nb_u = nb_u
        self.nb_v = nb_v
        u_knots = standardize_knot_vector(u_knots)
        v_knots = standardize_knot_vector(v_knots)
        self.u_knots = u_knots
        self.v_knots = v_knots
        self.u_multiplicities = u_multiplicities
        self.v_multiplicities = v_multiplicities
        self.weights = weights
        self.control_points_table = []
        points_row = []
        i = 1
        for pt in control_points:
            points_row.append(pt)
            if i == nb_v:
                self.control_points_table.append(points_row)
                points_row = []
                i = 1
            else:
                i += 1

        surface = NURBS.Surface()
        surface.degree_u = degree_u
        surface.degree_v = degree_v
        if weights is None:
            P = [(control_points[i][0], control_points[i][1], control_points[i][2]) for i in range(len(control_points))]
            surface.set_ctrlpts(P, nb_u, nb_v)
        else:
            Pw = [(control_points[i][0] * weights[i], control_points[i][1] * weights[i], control_points[i][2] * weights[i], weights[i]) for i in range(len(control_points))]
            surface.set_ctrlpts(Pw, nb_u, nb_v)
        knot_vector_u = []
        for i, u_knot in enumerate(u_knots):
            knot_vector_u.extend([u_knot] * u_multiplicities[i])

        knot_vector_v = []
        for i, v_knot in enumerate(v_knots):
            knot_vector_v.extend([v_knot] * v_multiplicities[i])

        surface.knotvector_u = knot_vector_u
        surface.knotvector_v = knot_vector_v
        surface.delta = 0.01
        surface_points = surface.evalpts
        self.surface = surface
        self.points = [Point3D((p[0], p[1], p[2])) for p in surface_points]

    def FreeCADExport(self, ip, ndigits=3):
        name = 'primitive{}'.format(ip)
        script = ''
        points = '['
        for i, pts_row in enumerate(self.control_points_table):
            pts = '['
            for j, pt in enumerate(pts_row):
                point = 'fc.Vector({},{},{}),'.format(pt[0], pt[1], pt[2])
                pts += point

            pts = pts[:-1] + '],'
            points += pts

        points = points[:-1] + ']'
        script += '{} = Part.BSplineSurface()\n'.format(name)
        if self.weights is None:
            script += '{}.buildFromPolesMultsKnots({},{},{},udegree={},vdegree={},uknots={},vknots={})\n'.format(name, points, self.u_multiplicities, self.v_multiplicities, self.degree_u, self.degree_v, self.u_knots, self.v_knots)
        else:
            script += '{}.buildFromPolesMultsKnots({},{},{},udegree={},vdegree={},uknots={},vknots={},weights={})\n'.format(name, points, self.u_multiplicities, self.v_multiplicities, self.degree_u, self.degree_v, self.u_knots, self.v_knots, self.weights)
        return script

    @classmethod
    def from_step(cls, arguments, object_dict):
        name = arguments[0][1:-1]
        degree_u = int(arguments[1])
        degree_v = int(arguments[2])
        points_sets = arguments[3][1:-1].split('),')
        points_sets = [elem + ')' for elem in points_sets[:-1]] + [points_sets[(-1)]]
        control_points = []
        for points_set in points_sets:
            points = [object_dict[int(i[1:])] for i in points_set[1:-1].split(',')]
            nb_v = len(points)
            control_points.extend(points)

        nb_u = int(len(control_points) / nb_v)
        surface_form = arguments[4]
        if arguments[5] == '.F.':
            u_closed = False
        else:
            if arguments[5] == '.T.':
                u_closed = True
            else:
                raise ValueError
        if arguments[6] == '.F.':
            v_closed = False
        else:
            if arguments[6] == '.T.':
                v_closed = True
            else:
                raise ValueError
        self_intersect = arguments[7]
        u_multiplicities = [int(i) for i in arguments[8][1:-1].split(',')]
        v_multiplicities = [int(i) for i in arguments[9][1:-1].split(',')]
        u_knots = [float(i) for i in arguments[10][1:-1].split(',')]
        v_knots = [float(i) for i in arguments[11][1:-1].split(',')]
        knot_spec = arguments[12]
        if 13 in range(len(arguments)):
            weight_data = [float(i) for i in arguments[13][1:-1].replace('(', '').replace(')', '').split(',')]
        else:
            weight_data = None
        return cls(degree_u, degree_v, control_points, nb_u, nb_v, u_multiplicities, v_multiplicities, u_knots, v_knots, weight_data, name)

    def Rotation(self, center, axis, angle, copy=True):
        new_control_points = [p.Rotation(center, axis, angle, True) for p in self.control_points]
        new_BSplineSurface3D = BSplineSurface3D(self.degree_u, self.degree_v, new_control_points, self.nb_u, self.nb_v, self.u_multiplicities, self.v_multiplicities, self.u_knots, self.v_knots, self.weights, self.name)
        if copy:
            return new_BSplineSurface3D
        self.control_points = new_control_points
        self.curve = new_BSplineSurface3D.curve
        self.points = new_BSplineSurface3D.points

    def Translation(self, offset, copy=True):
        new_control_points = [p.Translation(offset, True) for p in self.control_points]
        new_BSplineSurface3D = BSplineSurface3D(self.degree_u, self.degree_v, new_control_points, self.nb_u, self.nb_v, self.u_multiplicities, self.v_multiplicities, self.u_knots, self.v_knots, self.weights, self.name)
        if copy:
            return new_BSplineSurface3D
        self.control_points = new_control_points
        self.curve = new_BSplineSurface3D.curve
        self.points = new_BSplineSurface3D.points


class CompositePrimitive3D(Primitive3D):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = ['basis_primitives']
    _non_eq_attributes = ['name', 'basis_primitives']
    _non_hash_attributes = []

    def __init__(self, primitives, name=''):
        self.primitives = primitives
        basis_primitives = []
        for primitive in primitives:
            if hasattr(primitive, 'basis_primitives'):
                basis_primitives.extend(primitive.primitives)
            else:
                basis_primitives.append(primitive)

        Primitive3D.__init__(self, basis_primitives=basis_primitives, name=name)

    def UpdateBasisPrimitives(self):
        basis_primitives = []
        for primitive in self.primitives:
            if hasattr(primitive, 'basis_primitives'):
                basis_primitives.extend(primitive.primitives)
            else:
                basis_primitives.append(primitive)

        self.primitives = basis_primitives

    def MPLPlot(self, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = Axes3D(fig)
        else:
            fig = None
        for primitive in self.edges:
            primitive.MPLPlot(ax)

        return (
         fig, ax)


class Wire3D(CompositePrimitive3D):
    __doc__ = '\n    A collection of simple primitives, following each other making a wire\n    '

    def __init__(self, primitives, name=''):
        CompositePrimitive3D.__init__(self, primitives, name)

    def Length(self):
        length = 0.0
        for primitive in self.primitives:
            length += primitive.Length()

        return length

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        length = 0.0
        for primitive in self.primitives:
            primitive_length = primitive.Length()
            if length + primitive_length > curvilinear_abscissa:
                return primitive.PointAtCurvilinearAbscissa(curvilinear_abscissa - length)
            length += primitive_length

        raise ValueError

    def FreeCADExport(self, ip):
        name = 'primitive' + str(ip)
        s = 'E = []\n'
        for ip, primitive in enumerate(self.primitives):
            s += primitive.FreeCADExport('L{}'.format(ip))
            s += 'E.append(Part.Edge(L{}))\n'.format(ip)

        s += '{} = Part.Wire(E[:])\n'.format(name)
        return s


class Edge3D(Primitive3D):

    def __init__(self, edge_start, edge_end, name=''):
        Primitive3D.__init__(self, basis_primitives=[edge_start, edge_end], name=name)
        self.points = [edge_start, edge_end]

    def __hash__(self):
        return sum([hash(p) for p in self.points])

    def __eq__(self, other_):
        equal = True
        for point, other_point in zip(self.points, other_.points):
            equal = equal and point == other_point

        return equal

    def to_dict(self):
        dict_ = dc.DessiaObject.base_dict(self)
        dict_['edge_start'] = self.points[0]
        dict_['edge_end'] = self.points[1]
        return dict_

    @classmethod
    def from_step(cls, arguments, object_dict):
        return LineSegment3D(object_dict[arguments[1]], object_dict[arguments[2]], arguments[0][1:-1])

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            new_edge_start = self.points[0].Rotation(center, axis, angle, copy=True)
            new_edge_end = self.points[1].Rotation(center, axis, angle, copy=True)
            return Edge3D(new_edge_start, new_edge_end)
        self.points[0].Rotation(center, axis, angle, copy=False)
        self.points[1].Rotation(center, axis, angle, copy=False)

    def Translation(self, offset, copy=True):
        if copy:
            new_edge_start = self.points[0].Translation(offset, copy=True)
            new_edge_end = self.points[1].Translation(offset, copy=True)
            return Edge3D(new_edge_start, new_edge_end)
        self.points[0].Translation(offset, copy=False)
        self.points[1].Translation(offset, copy=False)

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            new_edge_start = self.points[0].frame_mapping(frame, side, copy=True)
            new_edge_end = self.points[1].frame_mapping(frame, side, copy=True)
            return Edge3D(new_edge_start, new_edge_end)
        self.points[0].frame_mapping(frame, side, copy=False)
        self.points[1].frame_mapping(frame, side, copy=False)

    def copy(self):
        new_edge_start = self.points[0].Copy()
        new_edge_end = self.points[1].Copy()
        return Edge3D(new_edge_start, new_edge_end)


class LineSegment3D(Edge3D):
    __doc__ = '\n    Define a line segment limited by two points\n    '

    def __init__(self, point1, point2, name=''):
        Edge3D.__init__(self, point1, point2, name='')
        self.bounding_box = self._bounding_box()

    def __hash__(self):
        return hash(self.points[0]) + hash(self.points[1])

    def to_dict(self):
        dict_ = dc.DessiaObject.base_dict(self)
        dict_['point1'] = self.points[0].to_dict()
        dict_['point2'] = self.points[1].to_dict()
        dict_['object_class'] = 'volmdlr.core.LineSegment3D'
        return dict_

    @classmethod
    def dict_to_object(cls, dict_):
        return cls(point1=(Point3D.dict_to_object(dict_['point1'])), point2=(Point3D.dict_to_object(dict_['point2'])),
          name=(dict_['name']))

    def _bounding_box(self):
        points = self.points
        xmin = min([pt[0] for pt in points])
        xmax = max([pt[0] for pt in points])
        ymin = min([pt[1] for pt in points])
        ymax = max([pt[1] for pt in points])
        zmin = min([pt[2] for pt in points])
        zmax = max([pt[2] for pt in points])
        return BoundingBox(xmin, xmax, ymin, ymax, zmin, zmax)

    def Length(self):
        return self.points[1].point_distance(self.points[0])

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        return self.points[0] + curvilinear_abscissa * (self.points[1] - self.points[0]) / self.Length()

    def PlaneProjection2D(self, x, y):
        return LineSegment2D(self.points[0].PlaneProjection2D(x, y), self.points[1].PlaneProjection2D(x, y))

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            return LineSegment3D(*[p.Rotation(center, axis, angle, copy=True) for p in self.points])
        Edge3D.Rotation(self, center, axis, angle, copy=False)
        self.bounding_box = self._bounding_box()

    def Translation(self, offset, copy=True):
        if copy:
            return LineSegment3D(*[p.Translation(offset, copy=True) for p in self.points])
        Edge3D.Translation(self, offset, copy=False)
        self.bounding_box = self._bounding_box()

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if side == 'old':
            if copy:
                return LineSegment3D(*[frame.OldCoordinates(p) for p in self.points])
            Edge3D.frame_mapping(self, frame, side, copy=False)
            self.bounding_box = self._bounding_box()
        if side == 'new':
            if copy:
                return LineSegment3D(*[frame.NewCoordinates(p) for p in self.points])
            Edge3D.frame_mapping(self, frame, side, copy=False)
            self.bounding_box = self._bounding_box()

    def copy(self):
        return LineSegment3D(*[p.Copy() for p in self.points])

    def MPLPlot(self, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.figure
        x = [p.vector[0] for p in self.points]
        y = [p.vector[1] for p in self.points]
        z = [p.vector[2] for p in self.points]
        ax.plot(x, y, z, 'o-k')
        return (fig, ax)

    def MPLPlot2D(self, x_3D, y_3D, ax=None, color='k', width=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.figure
        edge2D = self.PlaneProjection2D(x_3D, y_3D)
        edge2D.MPLPlot(ax=ax, color=color, width=width)
        return (fig, ax)

    def plot_data(self, x_3D, y_3D, marker=None, color='black', stroke_width=1, dash=False, opacity=1, arrow=False):
        edge2D = self.PlaneProjection2D(x_3D, y_3D)
        return edge2D.plot_data(marker, color, stroke_width, dash, opacity, arrow)

    def FreeCADExport(self, name, ndigits=6):
        x1, y1, z1 = round(1000 * self.points[0], ndigits).vector
        x2, y2, z2 = round(1000 * self.points[1], ndigits).vector
        return '{} = Part.LineSegment(fc.Vector({},{},{}),fc.Vector({},{},{}))\n'.format(name, x1, y1, z1, x2, y2, z2)

    def to_line(self):
        return Line3D(*self.points)

    def babylon_script(self, color=(1, 1, 1), name='line', type_='line', parent=None):
        if type_ == 'line' or type_ == 'dashed':
            s = 'var myPoints = [];\n'
            s += ('var point1 = new BABYLON.Vector3({},{},{});\n'.format)(*self.points[0])
            s += 'myPoints.push(point1);\n'
            s += ('var point2 = new BABYLON.Vector3({},{},{});\n'.format)(*self.points[1])
            s += 'myPoints.push(point2);\n'
            if type_ == 'line':
                s += 'var {} = BABYLON.MeshBuilder.CreateLines("lines", {{points: myPoints}}, scene);\n'.format(name)
            else:
                if type_ == 'dashed':
                    s += 'var {} = BABYLON.MeshBuilder.CreateDashedLines("lines", {{points: myPoints, dashNb:20}}, scene);'.format(name)
            s += '{}.color = new BABYLON.Color3{};\n'.format(name, tuple(color))
        else:
            if type_ == 'tube':
                radius = 0.03 * self.points[0].point_distance(self.points[1])
                s = ('var points = [new BABYLON.Vector3({},{},{}), new BABYLON.Vector3({},{},{})];\n'.format)(*self.points[0], *self.points[1])
                s += 'var {} = BABYLON.MeshBuilder.CreateTube("frame_U", {{path: points, radius: {}}}, {});'.format(name, radius, parent)
            else:
                raise NotImplementedError
        if parent is not None:
            s += '{}.parent = {};\n'.format(name, parent)
        return s


class Contour3D(Wire3D):
    _non_serializable_attributes = [
     'points']
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['points', 'name']
    _generic_eq = True

    def __init__(self, edges, point_inside_contour=None, name=''):
        """
        Faire un choix : soit edges c'est un CompositePrimitives3D
        ou alors un ensemble de primitives
        ou alors un ensemble de basis_primtives (qui sont des points pour le moment)
        """
        self.name = name
        self.point_inside_contour = point_inside_contour
        edges_primitives = []
        for edge in edges:
            if edge.__class__ == CompositePrimitive3D:
                edges_primitives.extend(edge.primitives)
            else:
                edges_primitives.append(edge)

        self.edges = edges_primitives
        if self.edges[0].__class__.__name__ == 'Contour3D':
            raise ValueError
        self.points = self.clean_points()

    def __hash__(self):
        return sum([hash(e) for e in self.edges]) + sum([hash(p) for p in self.points])

    def __eq__(self, other_):
        equal = True
        for edge, other_edge in zip(self.edges, other_.edges):
            equal = equal and edge == other_edge

        return equal

    @classmethod
    def from_step(cls, arguments, object_dict):
        edges = []
        for edge in arguments[1]:
            edges.append(object_dict[int(edge[1:])])

        return cls(edges, point_inside_contour=None, name=(arguments[0][1:-1]))

    def clean_points(self):
        """
        TODO : verifier si le dernier point est toujours le meme que le premier point
        lors d'un import step par exemple
        """
        if hasattr(self.edges[0], 'points'):
            points = self.edges[0].points[:]
        else:
            points = self.edges[0].tessellation_points()
        for edge in self.edges[1:]:
            if hasattr(edge, 'points'):
                points_to_add = edge.points[:]
                if points_to_add[0] == points[(-1)]:
                    points.extend(points_to_add[1:])
                else:
                    if points_to_add[(-1)] == points[(-1)]:
                        points.extend(points_to_add[-2::-1])
                    else:
                        if points_to_add[0] == points[0]:
                            points = points[::-1]
                            points.extend(points_to_add[1:])
                        else:
                            if points_to_add[(-1)] == points[0]:
                                points = points[::-1]
                                points.extend(points_to_add[-2::-1])
                            else:
                                raise NotImplementedError
            else:
                raise NotImplementedError

        if len(points) > 1:
            if points[0] == points[(-1)]:
                points.pop()
        return points

    def average_center_point(self):
        nb = len(self.points)
        x = npy.sum([p[0] for p in self.points]) / nb
        y = npy.sum([p[1] for p in self.points]) / nb
        z = npy.sum([p[2] for p in self.points]) / nb
        return Point3D((x, y, z))

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            new_edges = [edge.Rotation(center, axis, angle, copy=True) for edge in self.edges]
            return Contour3D(new_edges, None, self.name)
        for edge in self.edges:
            edge.Rotation(center, axis, angle, copy=False)

        for point in self.points:
            point.Rotation(center, axis, angle, copy=False)

    def Translation(self, offset, copy=True):
        if copy:
            new_edges = [edge.Translation(offset, copy=True) for edge in self.edges]
            return Contour3D(new_edges, None, self.name)
        for edge in self.edges:
            edge.Translation(offset, copy=False)

        for point in self.points:
            point.Translation(offset, copy=False)

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            new_edges = [edge.frame_mapping(frame, side, copy=True) for edge in self.edges]
            return Contour3D(new_edges, None, self.name)
        for edge in self.edges:
            edge.frame_mapping(frame, side, copy=False)

        for point in self.points:
            point.frame_mapping(frame, side, copy=False)

    def copy(self):
        new_edges = [edge.copy() for edge in self.edges]
        if self.point_inside_contour is not None:
            new_point_inside_contour = self.point_inside_contour.Copy()
        else:
            new_point_inside_contour = None
        return Contour3D(new_edges, new_point_inside_contour, self.name)

    def Length(self):
        length = 0.0
        for edge in self.edges:
            length += edge.Length()

        return length

    def PointAtCurvilinearAbscissa(self, curvilinear_abscissa):
        length = 0.0
        for primitive in self.edges:
            primitive_length = primitive.Length()
            if length + primitive_length > curvilinear_abscissa:
                return primitive.PointAtCurvilinearAbscissa(curvilinear_abscissa - length)
            length += primitive_length

        raise ValueError


class Circle3D(Contour3D):
    _non_serializable_attributes = [
     'point', 'edges', 'point_inside_contour']
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']
    _generic_eq = True

    def __init__(self, center, radius, normal, name=''):
        self.center = center
        self.radius = radius
        self.normal = normal
        Contour3D.__init__(self, [self], name=name)

    def tessellation_points(self, resolution=20):
        plane = Plane3D.from_normal(self.center, self.normal)
        tessellation_points_3D = [self.center + self.radius * math.cos(teta) * plane.vectors[0] + self.radius * math.sin(teta) * plane.vectors[1] for teta in npy.linspace(0, 2 * math.pi, resolution + 1)][:-1]
        return tessellation_points_3D

    def Length(self):
        return 2 * math.pi * self.radius

    def FreeCADExport(self, name, ndigits=3):
        xc, yc, zc = round(1000 * self.center, ndigits)
        xn, yn, zn = round(self.normal, ndigits)
        return '{} = Part.Circle(fc.Vector({},{},{}),fc.Vector({},{},{}),{})\n'.format(name, xc, yc, zc, xn, yn, zn, 1000 * self.radius)

    def Rotation(self, rot_center, axis, angle, copy=True):
        new_center = self.center.Rotation(rot_center, axis, angle, True)
        new_normal = self.normal.Rotation(rot_center, axis, angle, True)
        if copy:
            return Circle3D(new_center, self.radius, new_normal, self.name)
        self.center = new_center
        self.normal = new_normal

    def Translation(self, offset, copy=True):
        new_center = self.center.Translation(offset, True)
        new_normal = self.normal.Translation(offset, True)
        if copy:
            return Circle3D(new_center, self.radius, new_normal, self.name)
        self.center = new_center
        self.normal = new_normal

    @classmethod
    def from_step(cls, arguments, object_dict):
        center = object_dict[arguments[1]].origin
        radius = float(arguments[2]) / 1000
        normal = object_dict[arguments[1]].w
        return cls(center, radius, normal, arguments[0][1:-1])


class Ellipse3D(Contour3D):

    def __init__(self, major_axis, minor_axis, center, normal, major_dir, name=''):
        self.major_axis = major_axis
        self.minor_axis = minor_axis
        self.center = center
        self.normal = normal
        major_dir.Normalize()
        self.major_dir = major_dir
        Contour3D.__init__(self, [self], name=name)

    def FreeCADExport(self, ip, ndigits=3):
        name = 'primitive{}'.format(ip)
        xc, yc, zc = npy.round(1000 * self.center.vector, ndigits)
        major_vector = self.center + self.major_axis / 2 * self.major_dir
        xmaj, ymaj, zmaj = npy.round(1000 * major_vector.vector, ndigits)
        minor_vector = self.center + self.minor_axis / 2 * self.normal.Cross(self.major_dir)
        xmin, ymin, zmin = npy.round(1000 * minor_vector.vector, ndigits)
        return '{} = Part.Ellipse(fc.Vector({},{},{}), fc.Vector({},{},{}), fc.Vector({},{},{}))\n'.format(name, xmaj, ymaj, zmaj, xmin, ymin, zmin, xc, yc, zc)

    def Rotation(self, rot_center, axis, angle, copy=True):
        new_center = self.center.Rotation(rot_center, axis, angle, True)
        new_normal = self.normal.Rotation(rot_center, axis, angle, True)
        new_major_dir = self.major_dir.Rotation(rot_center, axis, angle, True)
        if copy:
            return Ellipse3D(self.major_axis, self.minor_axis, new_center, new_normal, new_major_dir, self.name)
        self.center = new_center
        self.normal = new_normal
        self.major_dir = new_major_dir

    def Translation(self, offset, copy=True):
        new_center = self.center.Translation(offset, True)
        new_normal = self.normal.Translation(offset, True)
        new_major_dir = self.major_dir.Translation(offset, True)
        if copy:
            return Ellipse3D(self.major_axis, self.minor_axis, new_center, new_normal, new_major_dir, self.name)
        self.center = new_center
        self.normal = new_normal
        self.major_dir = new_major_dir

    @classmethod
    def from_step(cls, arguments, object_dict):
        center = object_dict[arguments[1]].origin
        normal = object_dict[arguments[1]].w
        major_dir = object_dict[arguments[1]].u
        major_axis = float(arguments[2]) / 1000
        minor_axis = float(arguments[3]) / 1000
        return cls(major_axis, minor_axis, center, normal, major_dir, arguments[0][1:-1])


class Face3D(Primitive3D):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = ['bounding_box', 'polygon2D']
    _non_eq_attributes = ['name', 'bounding_box']
    _non_hash_attributes = []

    def __init__(self, contours, plane=None, points=None, polygon2D=None, name=''):
        self.contours = contours
        self.plane = plane
        self.points = points
        self.polygon2D = polygon2D
        self.name = name
        contour_points = [p.copy() for p in self.contours[0].points[:]]
        if plane is None:
            self.plane = Plane3D.from_points(contour_points)
        if points is None or polygon2D is None:
            self.points, self.polygon2D = self._repair_points_and_polygon2d(contour_points, self.plane)
            self.contours[0].points = [p.copy() for p in self.points]
        self.bounding_box = self._bounding_box()
        for pt in self.points:
            if not self.plane.point_on_plane(pt):
                print('WARNING', pt, 'not on', self.plane.__dict__)
                print('dot =', self.plane.normal.Dot(pt - self.plane.origin))
                raise ValueError

    def __hash__(self):
        return hash(self.plane) + sum([hash(p) for p in self.points])

    def __eq__(self, other_):
        equal = self.plane == other_.plane and self.polygon2D == other_.polygon2D
        for contour, other_contour in zip(self.contours, other_.contours):
            equal = equal and contour == other_contour

        for point, other_point in zip(self.points, other_.points):
            equal = equal and point == other_point

        return equal

    @classmethod
    def from_step(cls, arguments, object_dict):
        contours = []
        contours.append(object_dict[int(arguments[1][0][1:])])
        plane = Plane3D.from_points(contours[0].points)
        contours[0].points, polygon2D = cls._repair_points_and_polygon2d(contours[0].points, plane)
        points = [p.copy() for p in contours[0].points[:]]
        return cls(contours, plane=plane, points=points, polygon2D=polygon2D, name=(arguments[0][1:-1]))

    @classmethod
    def _repair_points_and_polygon2d(cls, points, plane):
        if points[0] == points[(-1)]:
            points = points[:-1]
        polygon_points = [p.To2D(plane.origin, plane.vectors[0], plane.vectors[1]) for p in points]
        repaired_points = [p.copy() for p in points]
        polygon2D = Polygon2D(polygon_points)
        if polygon2D.SelfIntersect()[0]:
            repaired_points = [
             repaired_points[1]] + [repaired_points[0]] + repaired_points[2:]
            polygon_points = [polygon_points[1]] + [polygon_points[0]] + polygon_points[2:]
            if polygon_points[0] == polygon_points[(-1)]:
                repaired_points = repaired_points[:-1]
                polygon_points = polygon_points[:-1]
            polygon2D = Polygon2D(polygon_points)
        return (
         repaired_points, polygon2D)

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            new_contour = [subcontour.Rotation(center, axis, angle, copy=True) for subcontour in self.contour]
            new_plane = self.plane.Rotation(center, axis, angle, copy=True)
            new_points = [p.Rotation(center, axis, angle, copy=True) for p in self.points]
            return Face3D(new_contour, new_plane, new_points, self.polygon2D, self.name)
        for contour in self.contours:
            contour.Rotation(center, axis, angle, copy=False)

        for point in self.points:
            point.Rotation(center, axis, angle, copy=False)

        self.plane.Rotation(center, axis, angle, copy=False)
        self.bounding_box = self._bounding_box()

    def Translation(self, offset, copy=True):
        if copy:
            new_contour = [subcontour.Translation(offset, copy=True) for subcontour in self.contours]
            new_plane = self.plane.Translation(offset, copy=True)
            new_points = [p.Translation(offset, copy=True) for p in self.points]
            return Face3D(new_contour, new_plane, new_points, self.polygon2D, self.name)
        for contour in self.contours:
            contour.Translation(offset, copy=False)

        for point in self.points:
            point.Translation(offset, copy=False)

        self.plane.Translation(offset, copy=False)
        self.bounding_box = self._bounding_box()

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            new_contour = [subcontour.frame_mapping(frame, side, copy=True) for subcontour in self.contours]
            new_plane = self.plane.frame_mapping(frame, side, copy=True)
            new_points = [p.frame_mapping(frame, side, copy=True) for p in self.points]
            return Face3D(new_contour, new_plane, new_points, None, self.name)
        for contour in self.contours:
            contour.frame_mapping(frame, side, copy=False)

        for point in self.points:
            point.frame_mapping(frame, side, copy=False)

        self.plane.frame_mapping(frame, side, copy=False)
        self.bounding_box = self._bounding_box()

    def copy(self):
        new_contours = [contour.copy() for contour in self.contours]
        new_plane = self.plane.copy()
        new_points = [p.Copy() for p in self.points]
        return Face3D(new_contours, new_plane, new_points, self.polygon2D.copy(), self.name)

    def average_center_point(self):
        """
        excluding holes
        """
        points = self.points
        nb = len(points)
        x = npy.sum([p[0] for p in points]) / nb
        y = npy.sum([p[1] for p in points]) / nb
        z = npy.sum([p[2] for p in points]) / nb
        return Point3D((x, y, z))

    def triangulation(self):
        points_3D = []
        vertices = []
        segments = []
        holes = []
        total_len = 0
        for i, contour in enumerate(self.contours):
            points_2D = [p.To2D(self.plane.origin, self.plane.vectors[0], self.plane.vectors[1]) for p in contour.points]
            vertices.extend([tuple(p.vector) for p in points_2D])
            if len(vertices) != len(set(vertices)):
                return (None, None)
            len_points = len(contour.points)
            segments += [[a + total_len, a + total_len + 1] for a in range(len_points - 1)] + [[len_points + total_len - 1, 0 + total_len]]
            total_len += len_points
            points_3D.extend(contour.points)
            if i > 0:
                if contour.point_inside_contour is not None:
                    holes.append(contour.point_inside_contour)
                else:
                    polygon2D = Polygon2D(points_2D)
                    mid_point_3D = contour.average_center_point()
                    mid_point_2D = mid_point_3D.To2D(self.plane.origin, self.plane.vectors[0], self.plane.vectors[1])
                    holes.append(mid_point_2D.vector)
                    polygon2D.PointBelongs(mid_point_2D) or warnings.warn('average_center_point is not included inside its contour.')

        if holes:
            tri = {'vertices':vertices, 
             'segments':segments,  'holes':holes}
        else:
            tri = {'vertices':vertices, 
             'segments':segments}
        t = triangle.triangulate(tri, 'p')
        if 'triangles' in t:
            triangles = t['triangles'].tolist()
            return (points_3D, triangles)
        return (None, None)

    def _bounding_box(self):
        points = self.points
        xmin = min([pt[0] for pt in points])
        xmax = max([pt[0] for pt in points])
        ymin = min([pt[1] for pt in points])
        ymax = max([pt[1] for pt in points])
        zmin = min([pt[2] for pt in points])
        zmax = max([pt[2] for pt in points])
        return BoundingBox(xmin, xmax, ymin, ymax, zmin, zmax)

    def distance_to_point(self, point, return_other_point=False):
        """
        Only works if the surface is planar
        TODO : this function does not take into account if Face has holes
        """
        projected_pt = point.PlaneProjection3D(self.plane.origin, self.plane.vectors[0], self.plane.vectors[1])
        projection_distance = point.point_distance(projected_pt)
        if self.point_on_face(projected_pt):
            if return_other_point:
                return (
                 projection_distance, projected_pt)
            return projection_distance
        point_2D = point.To2D(self.plane.origin, self.plane.vectors[0], self.plane.vectors[1])
        border_distance, other_point = self.polygon2D.PointBorderDistance(point_2D, return_other_point=True)
        other_point = other_point.To3D(self.plane.origin, self.plane.vectors[0], self.plane.vectors[1])
        if return_other_point:
            return (
             (projection_distance ** 2 + border_distance ** 2) ** 0.5, other_point)
        return (projection_distance ** 2 + border_distance ** 2) ** 0.5

    def distance_to_face(self, face2, return_points=False):
        """
        Only works if the surface is planar
        TODO : this function does not take into account if Face has holes
        TODO : TRAITER LE CAS OU LA DISTANCE LA PLUS COURTE N'EST PAS D'UN SOMMET
        """
        if self.face_intersection(face2) is not None:
            return (0, None, None)
        else:
            polygon1_points_3D = [Point3D(p.vector) for p in self.points]
            polygon2_points_3D = [Point3D(p.vector) for p in face2.points]
            distances = []
            d_min = return_points or face2.distance_to_point(polygon1_points_3D[0])
            for point1 in polygon1_points_3D[1:]:
                d = face2.distance_to_point(point1)
                if d < d_min:
                    d_min = d

            for point2 in polygon2_points_3D:
                d = self.distance_to_point(point2)
                if d < d_min:
                    d_min = d

            return d_min
        for point1 in polygon1_points_3D:
            d, other_point = face2.distance_to_point(point1, return_other_point=True)
            distances.append((d, point1, other_point))

        for point2 in polygon2_points_3D:
            d, other_point = self.distance_to_point(point2, return_other_point=True)
            distances.append((d, point2, other_point))

        d_min, point_min, other_point_min = distances[0]
        for distance in distances[1:]:
            if distance[0] < d_min:
                d_min = distance[0]
                point_min = distance[1]
                other_point_min = distance[2]

        return (
         d_min, point_min, other_point_min)

    def point_on_face(self, point):
        """
        Only works if the surface is planar
        TODO : this function does not take into account if Face has holes

        Tells you if a point is on the 3D face and inside its contour
        """
        point_on_plane = self.plane.point_on_plane(point)
        if not point_on_plane:
            print('point not on plane so not on face')
            return False
        else:
            point_2D = point.To2D(self.plane.origin, self.plane.vectors[0], self.plane.vectors[1])
            return self.polygon2D.PointBelongs(point_2D) or False
        return True

    def edge_intersection(self, edge):
        linesegment = LineSegment3D(*edge.points)
        intersection_point = self.plane.linesegment_intersection(linesegment)
        if intersection_point is None:
            return
        else:
            point_on_face_boo = self.point_on_face(intersection_point)
            return point_on_face_boo or None
        return intersection_point

    def linesegment_intersection(self, linesegment, abscissea=False):
        if abscissea:
            intersection_point, intersection_abscissea = self.plane.linesegment_intersection(linesegment, True)
        else:
            intersection_point = self.plane.linesegment_intersection(linesegment)
        if intersection_point is None:
            if abscissea:
                return (None, None)
            return
        point_on_face_boo = self.point_on_face(intersection_point)
        if not point_on_face_boo:
            if abscissea:
                return (None, None)
            return
        if abscissea:
            return (
             intersection_point, intersection_abscissea)
        return intersection_point

    def face_intersection(self, face2):
        """
        Only works if the surface is planar
        TODO : this function does not take into account if Face has holes
        """
        bbox1 = self.bounding_box
        bbox2 = face2.bounding_box
        if not bbox1.bbox_intersection(bbox2):
            return
        else:
            intersection_points = []
            for edge2 in face2.contours[0].edges:
                intersection_point = self.edge_intersection(edge2)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)

            for edge1 in self.contours[0].edges:
                intersection_point = face2.edge_intersection(edge1)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)

            return intersection_points or None
        return intersection_points

    def plot(self, ax=None):
        fig = plt.figure()
        if ax is None:
            ax = fig.add_subplot(111, projection='3d')
        x = [p[0] for p in self.contours[0].points]
        y = [p[1] for p in self.contours[0].points]
        z = [p[2] for p in self.contours[0].points]
        ax.scatter(x, y, z)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        for edge in self.contours[0].edges:
            for point1, point2 in (edge.points, edge.points[1:] + [edge.points[0]]):
                xs = [
                 point1[0], point2[0]]
                ys = [point1[1], point2[1]]
                zs = [point1[2], point2[2]]
                line = mpl_toolkits.mplot3d.art3d.Line3D(xs, ys, zs)
                ax.add_line(line)

        plt.show()
        return ax


class Shell3D(CompositePrimitive3D):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = ['bounding_box']
    _non_eq_attributes = ['name', 'color', 'alphabounding_box', 'contours']
    _non_hash_attributes = []

    def __init__(self, faces, *, color=None, alpha=1.0, name=''):
        self.faces = faces
        self.name = name
        self.color = color
        self.alpha = alpha
        self.bounding_box = self._bounding_box()

    def __hash__(self):
        return sum([hash(f) for f in self.faces])

    def __eq__(self, other_):
        if self.__class__ != other_.__class__:
            return False
        equal = True
        for face, other_face in zip(self.faces, other_.faces):
            equal = equal and face == other_face

        return equal

    @classmethod
    def from_step(cls, arguments, object_dict):
        faces = []
        for face in arguments[1]:
            faces.append(object_dict[int(face[1:])])

        return cls(faces, name=(arguments[0][1:-1]))

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            new_faces = [face.Rotation(center, axis, angle, copy=True) for face in self.faces]
            return Shell3D(new_faces, name=(self.name))
        for face in self.faces:
            face.Rotation(center, axis, angle, copy=False)

        self.bounding_box = self._bounding_box()

    def Translation(self, offset, copy=True):
        if copy:
            new_faces = [face.Translation(offset, copy=True) for face in self.faces]
            return Shell3D(new_faces, name=(self.name))
        for face in self.faces:
            face.Translation(offset, copy=False)

        self.bounding_box = self._bounding_box()

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            new_faces = [face.frame_mapping(frame, side, copy=True) for face in self.faces]
            return Shell3D(new_faces, name=(self.name))
        for face in self.faces:
            face.frame_mapping(frame, side, copy=False)

        self.bounding_box = self._bounding_box()

    def copy(self):
        new_faces = [face.copy() for face in self.faces]
        return Shell3D(new_faces, name=(self.name))

    def union(self, shell2):
        new_faces = [face for face in self.faces + shell2.faces]
        new_name = self.name + ' union ' + shell2.name
        new_color = self.color
        return Shell3D(new_faces, name=new_name, color=new_color)

    def _bounding_box(self):
        """
        Returns the boundary box
        """
        points = []
        for face in self.faces:
            points.extend(face.bounding_box.points)

        xmin = min([pt[0] for pt in points])
        xmax = max([pt[0] for pt in points])
        ymin = min([pt[1] for pt in points])
        ymax = max([pt[1] for pt in points])
        zmin = min([pt[2] for pt in points])
        zmax = max([pt[2] for pt in points])
        return BoundingBox(xmin, xmax, ymin, ymax, zmin, zmax, self.name)

    def point_belongs(self, point):
        """
        Ray Casting algorithm
        Returns True if the point is inside the Shell, False otherwise
        """
        epsilon = 1
        bbox = self.bounding_box
        if point[0] < bbox.xmin or point[0] > bbox.xmax:
            return False
        if point[1] < bbox.ymin or point[1] > bbox.ymax:
            return False
        if point[2] < bbox.zmin or point[2] > bbox.zmax:
            return False
        rays = []
        rays.append(LineSegment3D(point, Point3D((bbox.xmin - random.uniform(0, 1) * epsilon, bbox.ymin - random.uniform(0, 1) * epsilon, bbox.zmin - random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmax + random.uniform(0, 1) * epsilon, bbox.ymin - random.uniform(0, 1) * epsilon, bbox.zmin - random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmin - random.uniform(0, 1) * epsilon, bbox.ymax + random.uniform(0, 1) * epsilon, bbox.zmin - random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmin - random.uniform(0, 1) * epsilon, bbox.ymin - random.uniform(0, 1) * epsilon, bbox.zmax + random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmax + random.uniform(0, 1) * epsilon, bbox.ymax + random.uniform(0, 1) * epsilon, bbox.zmax + random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmax + random.uniform(0, 1) * epsilon, bbox.ymax + random.uniform(0, 1) * epsilon, bbox.zmin - random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmax + random.uniform(0, 1) * epsilon, bbox.ymin - random.uniform(0, 1) * epsilon, bbox.zmax + random.uniform(0, 1) * epsilon))))
        rays.append(LineSegment3D(point, Point3D((bbox.xmin - random.uniform(0, 1) * epsilon, bbox.ymax + random.uniform(0, 1) * epsilon, bbox.zmax + random.uniform(0, 1) * epsilon))))
        rays = sorted(rays, key=(lambda ray: ray.Length()))
        rays_intersections = []
        tests = []
        for ray in rays[:3]:
            count = 0
            ray_intersection = []
            is_inside = True
            for face in self.faces:
                intersection_point = face.linesegment_intersection(ray)
                if intersection_point is not None:
                    ray_intersection.append(intersection_point)
                    count += 1

            if count % 2 == 0:
                is_inside = False
            tests.append(is_inside)
            rays_intersections.append(ray_intersection)

        if sum(tests) == 0 or sum(tests) == 3:
            return tests[0]
        return sum(tests) > 1

    def is_inside_shell(self, shell2):
        """
        Returns True if all the points of self are inside shell2 and no face         are intersecting
        """
        bbox1 = self.bounding_box
        bbox2 = shell2.bounding_box
        if not bbox1.is_inside_bbox(bbox2):
            return False
        points = []
        for face in self.faces:
            points.extend(face.contours[0].points)

        for point in points:
            if not shell2.point_belongs(point):
                return False

        for face1 in self.faces:
            for face2 in shell2.faces:
                intersection_points = face1.face_intersection(face2)
                if intersection_points is not None:
                    return False

        return True

    def shell_intersection(self, shell2):
        """
        Return None if disjointed
        Return (1, 0) or (0, 1) if one is inside the other
        Return (n1, n2) if intersection

        4 cases :
            (n1, n2) with face intersection             => (n1, n2)
            (0, 0) with face intersection               => (0, 0)
            (0, 0) with no face intersection            => None
            (1, 0) or (0, 1) with no face intersection  => 1
        """
        bbox1 = self.bounding_box
        bbox2 = shell2.bounding_box
        if not bbox1.bbox_intersection(bbox2):
            return
        points1 = []
        for face in self.faces:
            points1.extend(face.contours[0].points)

        points2 = []
        for face in shell2.faces:
            points2.extend(face.contours[0].points)

        nb_pts1 = len(points1)
        nb_pts2 = len(points2)
        compteur1 = 0
        compteur2 = 0
        for point1 in points1:
            if shell2.point_belongs(point1):
                compteur1 += 1

        for point2 in points2:
            if self.point_belongs(point2):
                compteur2 += 1

        inter1 = compteur1 / nb_pts1
        inter2 = compteur2 / nb_pts2
        for face1 in self.faces:
            for face2 in shell2.faces:
                intersection_points = face1.face_intersection(face2)
                if intersection_points is not None:
                    return (
                     inter1, inter2)

        if (
         inter1, inter2) == (0, 0):
            return
        return 1

    def distance_to_shell(self, shell2, add_to_volumemodel=None):
        """
        Returns a Mesure object if the distance is not zero, otherwise returns None
        """
        if self.shell_intersection(shell2) is not None:
            if self.shell_intersection(shell2) != 1:
                return
        distance_min, point1_min, point2_min = self.faces[0].distance_to_face((shell2.faces[0]), return_points=True)
        for face1 in self.faces:
            bbox1 = face1.bounding_box
            for face2 in shell2.faces:
                bbox2 = face2.bounding_box
                bbox_distance = bbox1.distance_to_bbox(bbox2)
                if bbox_distance < distance_min:
                    distance, point1, point2 = face1.distance_to_face(face2, return_points=True)
                    if distance == 0:
                        return
                    if distance < distance_min:
                        distance_min, point1_min, point2_min = distance, point1, point2

        mesure = Measure3D(point1_min, point2_min)
        if add_to_volumemodel is not None:
            add_to_volumemodel.primitives.append(mesure)
        return mesure

    def distance_to_point(self, point, add_to_volumemodel=None):
        """
        Computes the distance of a point to a Shell3D, whether it is inside or outside the Shell3D
        """
        distance_min, point1_min, point2_min = self.faces[0].distance_to_point(point, return_other_point=True)
        for face in self.faces[1:]:
            bbox_distance = self.bounding_box.distance_to_point(point)
            if bbox_distance < distance_min:
                distance, point1, point2 = face.distance_to_point(point, return_other_point=True)
                if distance < distance_min:
                    distance_min, point1_min, point2_min = distance, point1, point2

        mesure = Measure3D(point1_min, point2_min)
        if add_to_volumemodel is not None:
            add_to_volumemodel.primitives.append(mesure)
        return mesure

    def intersection_internal_aabb_volume(self, shell2):
        """
        aabb made of the intersection points and the points of self internal to shell2
        """
        intersections_points = []
        for face1 in self.faces:
            for face2 in shell2.faces:
                intersection_points = face1.face_intersection(face2)
                if intersection_points is not None:
                    intersections_points.extend(intersection_points)

        shell1_points_inside_shell2 = []
        for face in self.faces:
            for point in face.points:
                if shell2.point_belongs(point):
                    shell1_points_inside_shell2.append(point)

        if len(intersections_points + shell1_points_inside_shell2) == 0:
            return 0
        bbox = BoundingBox.from_points(intersections_points + shell1_points_inside_shell2)
        return bbox.volume()

    def intersection_external_aabb_volume(self, shell2):
        """
        aabb made of the intersection points and the points of self external to shell2
        """
        intersections_points = []
        for face1 in self.faces:
            for face2 in shell2.faces:
                intersection_points = face1.face_intersection(face2)
                if intersection_points is not None:
                    intersections_points.extend(intersection_points)

        shell1_points_outside_shell2 = []
        for face in self.faces:
            for point in face.points:
                if not shell2.point_belongs(point):
                    shell1_points_outside_shell2.append(point)

        if len(intersections_points + shell1_points_outside_shell2) == 0:
            return 0
        bbox = BoundingBox.from_points(intersections_points + shell1_points_outside_shell2)
        return bbox.volume()

    def babylon_meshes(self):
        positions = []
        indices = []
        nb_points = 0
        for i, face in enumerate(self.faces):
            points_3D, triangles_indexes = face.triangulation()
            if points_3D is not None:
                for point in points_3D:
                    positions.extend([i for i in round(point, 6)])

                for j, indexes in enumerate(triangles_indexes):
                    indices.extend([i + nb_points for i in indexes])

                nb_points += len(points_3D)

        babylon_mesh = {'positions':positions, 
         'indices':indices, 
         'name':self.name, 
         'alpha':self.alpha, 
         'name':self.name}
        if self.color is None:
            babylon_mesh['color'] = [
             0.8, 0.8, 0.8]
        else:
            babylon_mesh['color'] = list(self.color)
        return [babylon_mesh]

    def babylon_script(self, name='primitive_mesh'):
        s = 'var {} = new BABYLON.Mesh("{}", scene);\n'.format(name, name)
        mesh = self.babylon_meshes()[0]
        s += 'var positions = {};\n'.format(mesh['positions'])
        s += 'var indices = {};\n'.format(mesh['indices'])
        s += 'var normals = [];\n'
        s += 'var vertexData = new BABYLON.VertexData();\n'
        s += 'BABYLON.VertexData.ComputeNormals(positions, indices, normals);\n'
        s += 'vertexData.positions = positions;\n'
        s += 'vertexData.indices = indices;\n'
        s += 'vertexData.normals = normals;\n'
        s += 'vertexData.applyToMesh({});\n'.format(name)
        s += '{}.enableEdgesRendering(0.9);\n'.format(name)
        s += '{}.edgesWidth = 0.1;\n'.format(name)
        s += '{}.edgesColor = new BABYLON.Color4(0, 0, 0, 0.6);\n'.format(name)
        s += 'var mat = new BABYLON.StandardMaterial("mat", scene);\n'
        s += 'mat.backFaceCulling = false;\n'
        s += 'mat.alpha = {};\n'.format(self.alpha)
        s += '{}.material = mat;\n'.format(name)
        if self.color is not None:
            s += ('mat.diffuseColor = new BABYLON.Color3({}, {}, {});\n'.format)(*self.color)
        return s


class BoundingBox(dc.DessiaObject):
    __doc__ = '\n    An axis aligned boundary box\n    '

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, name=''):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        self.points = [Point3D((self.xmin, self.ymin, self.zmin)),
         Point3D((self.xmax, self.ymin, self.zmin)),
         Point3D((self.xmax, self.ymax, self.zmin)),
         Point3D((self.xmin, self.ymax, self.zmin)),
         Point3D((self.xmin, self.ymin, self.zmax)),
         Point3D((self.xmax, self.ymin, self.zmax)),
         Point3D((self.xmax, self.ymax, self.zmax)),
         Point3D((self.xmin, self.ymax, self.zmax))]
        self.center = (self.points[0] + self.points[(-2)]) / 2
        self.name = name

    def __hash__(self):
        return sum([hash(p) for p in self.points])

    def plot(self, ax=None, color=''):
        fig = plt.figure()
        if ax is None:
            ax = fig.add_subplot(111, projection='3d')
        bbox_edges = [[self.points[0], self.points[1]], [self.points[0], self.points[3]],
         [
          self.points[0], self.points[4]], [self.points[1], self.points[2]],
         [
          self.points[1], self.points[5]], [self.points[2], self.points[3]],
         [
          self.points[2], self.points[6]], [self.points[3], self.points[7]],
         [
          self.points[4], self.points[5]], [self.points[5], self.points[6]],
         [
          self.points[6], self.points[7]], [self.points[7], self.points[4]]]
        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]
        z = [p[2] for p in self.points]
        ax.scatter(x, y, z)
        for edge in bbox_edges:
            ax.plot3D([edge[0][0], edge[1][0]], [
             edge[0][1], edge[1][1]], [
             edge[0][2], edge[1][2]], 'gray')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()
        return ax

    @classmethod
    def from_points(cls, points):
        xmin = min([pt[0] for pt in points])
        xmax = max([pt[0] for pt in points])
        ymin = min([pt[1] for pt in points])
        ymax = max([pt[1] for pt in points])
        zmin = min([pt[2] for pt in points])
        zmax = max([pt[2] for pt in points])
        return cls(xmin, xmax, ymin, ymax, zmin, zmax)

    def volume(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin) * (self.zmax - self.zmin)

    def bbox_intersection(self, bbox2):
        return self.xmin < bbox2.xmax and self.xmax > bbox2.xmin and self.ymin < bbox2.ymax and self.ymax > bbox2.ymin and self.zmin < bbox2.zmax and self.zmax > bbox2.zmin

    def is_inside_bbox(self, bbox2):
        return self.xmin > bbox2.xmin and self.xmax < bbox2.xmax and self.ymin > bbox2.ymin and self.ymax < bbox2.ymax and self.zmin > bbox2.zmin and self.zmax < bbox2.zmax

    def intersection_volume(self, bbox2):
        if not self.bbox_intersection(bbox2):
            return 0
        permute_bbox1 = self
        permute_bbox2 = bbox2
        if permute_bbox2.xmin < permute_bbox1.xmin:
            permute_bbox1, permute_bbox2 = permute_bbox2, permute_bbox1
        lx = permute_bbox1.xmax - permute_bbox2.xmin
        if permute_bbox2.ymin < permute_bbox1.ymin:
            permute_bbox1, permute_bbox2 = permute_bbox2, permute_bbox1
        ly = permute_bbox1.ymax - permute_bbox2.ymin
        if permute_bbox2.zmin < permute_bbox1.zmin:
            permute_bbox1, permute_bbox2 = permute_bbox2, permute_bbox1
        lz = permute_bbox1.zmax - permute_bbox2.zmin
        return lx * ly * lz

    def distance_to_bbox(self, bbox2):
        if self.bbox_intersection(bbox2):
            return 0
        permute_bbox1 = self
        permute_bbox2 = bbox2
        if permute_bbox2.xmin < permute_bbox1.xmin:
            permute_bbox1, permute_bbox2 = permute_bbox2, permute_bbox1
        dx = permute_bbox2.xmin - permute_bbox1.xmax
        if dx < 0:
            dx = 0
        if permute_bbox2.ymin < permute_bbox1.ymin:
            permute_bbox1, permute_bbox2 = permute_bbox2, permute_bbox1
        dy = permute_bbox2.ymin - permute_bbox1.ymax
        if dy < 0:
            dy = 0
        if permute_bbox2.zmin < permute_bbox1.zmin:
            permute_bbox1, permute_bbox2 = permute_bbox2, permute_bbox1
        dz = permute_bbox2.zmin - permute_bbox1.zmax
        if dz < 0:
            dz = 0
        return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

    def point_belongs(self, point):
        return self.xmin < point[0] and point[0] < self.xmax and self.ymin < point[1] and point[1] < self.ymax and self.zmin < point[2] and point[2] < self.zmax

    def distance_to_point(self, point):
        if self.point_belongs(point):
            return min([self.xmax - point[0], point[0] - self.xmin,
             self.ymax - point[1], point[1] - self.ymin,
             self.zmax - point[2], point[2] - self.zmin])
        else:
            if point[0] < self.xmin:
                dx = self.xmin - point[0]
            else:
                if self.xmax < point[0]:
                    dx = point[0] - self.xmax
                else:
                    dx = 0
            if point[1] < self.ymin:
                dy = self.ymin - point[1]
            else:
                if self.ymax < point[1]:
                    dy = point[1] - self.ymax
                else:
                    dy = 0
            if point[2] < self.zmin:
                dz = self.zmin - point[2]
            else:
                if self.zmax < point[2]:
                    dz = point[2] - self.zmax
                else:
                    dz = 0
        return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

    def distance_between_two_points_on_bbox(self, point1, point2):
        if math.isclose((point1[0]), (self.xmin), abs_tol=1e-08):
            face_point1 = 5
        else:
            if math.isclose((point1[0]), (self.xmax), abs_tol=1e-08):
                face_point1 = 3
            else:
                if math.isclose((point1[1]), (self.ymin), abs_tol=1e-08):
                    face_point1 = 4
                else:
                    if math.isclose((point1[1]), (self.ymax), abs_tol=1e-08):
                        face_point1 = 2
                    else:
                        if math.isclose((point1[2]), (self.zmin), abs_tol=1e-08):
                            face_point1 = 6
                        else:
                            if math.isclose((point1[2]), (self.zmax), abs_tol=1e-08):
                                face_point1 = 1
                            else:
                                raise NotImplementedError
        if math.isclose((point2[0]), (self.xmin), abs_tol=1e-08):
            face_point2 = 5
        else:
            if math.isclose((point2[0]), (self.xmax), abs_tol=1e-08):
                face_point2 = 3
            else:
                if math.isclose((point2[1]), (self.ymin), abs_tol=1e-08):
                    face_point2 = 4
                else:
                    if math.isclose((point2[1]), (self.ymax), abs_tol=1e-08):
                        face_point2 = 2
                    else:
                        if math.isclose((point2[2]), (self.zmin), abs_tol=1e-08):
                            face_point2 = 6
                        else:
                            if math.isclose((point2[2]), (self.zmax), abs_tol=1e-08):
                                face_point2 = 1
                            else:
                                raise NotImplementedError
        point1_copy = point1.copy()
        point2_copy = point2.copy()
        if face_point1 > face_point2:
            point1, point2 = point2, point1
            face_point1, face_point2 = face_point2, face_point1
        elif face_point1 == face_point2:
            return point1.point_distance(point2)
            deltax = self.xmax - self.xmin
            deltay = self.ymax - self.ymin
            deltaz = self.zmax - self.zmin
            point1_2d_coordinate_dict = {1:Point2D((point1[0] - self.xmin - deltax / 2, point1[1] - self.ymin - deltay / 2)), 
             2:Point2D((point1[2] - self.zmin - deltaz / 2, point1[0] - self.xmin - deltax / 2)), 
             3:Point2D((point1[1] - self.ymin - deltay / 2, point1[2] - self.zmin - deltaz / 2)), 
             4:Point2D((point1[0] - self.xmin - deltax / 2, point1[2] - self.zmin - deltaz / 2)), 
             5:Point2D((point1[2] - self.zmin - deltaz / 2, point1[1] - self.ymin - deltay / 2)), 
             6:Point2D((point1[1] - self.ymin - deltay / 2, point1[0] - self.xmin - deltax / 2))}
            point2_2d_coordinate_dict = {1:Point2D((point2[0] - self.xmin - deltax / 2, point2[1] - self.ymin - deltay / 2)), 
             2:Point2D((point2[2] - self.zmin - deltaz / 2, point2[0] - self.xmin - deltax / 2)), 
             3:Point2D((point2[1] - self.ymin - deltay / 2, point2[2] - self.zmin - deltaz / 2)), 
             4:Point2D((point2[0] - self.xmin - deltax / 2, point2[2] - self.zmin - deltaz / 2)), 
             5:Point2D((point2[2] - self.zmin - deltaz / 2, point2[1] - self.ymin - deltay / 2)), 
             6:Point2D((point2[1] - self.ymin - deltay / 2, point2[0] - self.xmin - deltax / 2))}
            vertex_2d_coordinate_dict = {1:[
              Point2D((self.xmin - self.xmin - deltax / 2, self.ymin - self.ymin - deltay / 2)), Point2D((self.xmin - self.xmin - deltax / 2, self.ymax - self.ymin - deltay / 2)), Point2D((self.xmax - self.xmin - deltax / 2, self.ymax - self.ymin - deltay / 2)), Point2D((self.xmax - self.xmin - deltax / 2, self.ymin - self.ymin - deltay / 2))], 
             2:[
              Point2D((self.zmin - self.zmin - deltaz / 2, self.xmin - self.xmin - deltax / 2)), Point2D((self.zmin - self.zmin - deltaz / 2, self.xmax - self.xmin - deltax / 2)), Point2D((self.zmax - self.zmin - deltaz / 2, self.xmax - self.xmin - deltax / 2)), Point2D((self.zmax - self.zmin - deltaz / 2, self.xmin - self.xmin - deltax / 2))], 
             3:[
              Point2D((self.ymin - self.ymin - deltay / 2, self.zmin - self.zmin - deltaz / 2)), Point2D((self.ymin - self.ymin - deltay / 2, self.zmax - self.zmin - deltaz / 2)), Point2D((self.ymax - self.ymin - deltay / 2, self.zmax - self.zmin - deltaz / 2)), Point2D((self.ymax - self.ymin - deltay / 2, self.zmin - self.zmin - deltaz / 2))], 
             4:[
              Point2D((self.xmin - self.xmin - deltax / 2, self.zmin - self.zmin - deltaz / 2)), Point2D((self.xmin - self.xmin - deltax / 2, self.zmax - self.zmin - deltaz / 2)), Point2D((self.xmax - self.xmin - deltax / 2, self.zmax - self.zmin - deltaz / 2)), Point2D((self.xmax - self.xmin - deltax / 2, self.zmin - self.zmin - deltaz / 2))], 
             5:[
              Point2D((self.zmin - self.zmin - deltaz / 2, self.ymin - self.ymin - deltay / 2)), Point2D((self.zmin - self.zmin - deltaz / 2, self.ymax - self.ymin - deltay / 2)), Point2D((self.zmax - self.zmin - deltaz / 2, self.ymax - self.ymin - deltay / 2)), Point2D((self.zmax - self.zmin - deltaz / 2, self.ymin - self.ymin - deltay / 2))], 
             6:[
              Point2D((self.ymin - self.ymin - deltay / 2, self.xmin - self.xmin - deltax / 2)), Point2D((self.ymin - self.ymin - deltay / 2, self.xmax - self.xmin - deltax / 2)), Point2D((self.ymax - self.ymin - deltay / 2, self.xmax - self.xmin - deltax / 2)), Point2D((self.ymax - self.ymin - deltay / 2, self.xmin - self.xmin - deltax / 2))]}
            vertex_to_3d_dict = {1:(
              2, self.zmax, 0, 1), 
             2:(
              1, self.ymax, 2, 0), 
             3:(
              0, self.xmax, 1, 2), 
             4:(
              1, self.ymin, 0, 2), 
             5:(
              0, self.xmin, 2, 1), 
             6:(
              2, self.zmin, 1, 0)}
            offset_dict = {0:self.xmin + deltax / 2, 
             1:self.ymin + deltay / 2, 
             2:self.zmin + deltaz / 2}
            opposite_face_dict = {1:6, 
             2:4,  3:5,  4:2,  5:3,  6:1}
            combination_dict = {(1, 2):Frame2D(Point2D((0, deltay / 2 + deltaz / 2)), Vector2D((0, -1)), Vector2D((1, 0))), 
             (2, 1):Frame2D(Point2D((deltay / 2 + deltaz / 2, 0)), Vector2D((0, 1)), Vector2D((-1, 0))), 
             (1, 3):Frame2D(Point2D((deltax / 2 + deltaz / 2, 0)), Vector2D((0, 1)), Vector2D((-1, 0))), 
             (3, 1):Frame2D(Point2D((0, deltax / 2 + deltaz / 2)), Vector2D((0, -1)), Vector2D((1, 0))), 
             (1, 4):Frame2D(Point2D((0, -deltay / 2 - deltaz / 2)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (4, 1):Frame2D(Point2D((-deltay / 2 - deltaz / 2, 0)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (1, 5):Frame2D(Point2D((-deltax / 2 - deltaz / 2, 0)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (5, 1):Frame2D(Point2D((0, -deltax / 2 - deltaz / 2)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (2, 3):Frame2D(Point2D((0, deltax / 2 + deltay / 2)), Vector2D((0, -1)), Vector2D((1, 0))), 
             (3, 2):Frame2D(Point2D((deltax / 2 + deltay / 2, 0)), Vector2D((0, 1)), Vector2D((-1, 0))), 
             (2, 5):Frame2D(Point2D((0, -deltax / 2 - deltay / 2)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (5, 2):Frame2D(Point2D((-deltax / 2 - deltay / 2, 0)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (2, 6):Frame2D(Point2D((-deltaz / 2 - deltay / 2, 0)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (6, 2):Frame2D(Point2D((0, -deltaz / 2 - deltay / 2)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (3, 4):Frame2D(Point2D((-deltay / 2 - deltax / 2, 0)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (4, 3):Frame2D(Point2D((0, -deltay / 2 - deltax / 2)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (3, 6):Frame2D(Point2D((0, -deltaz / 2 - deltax / 2)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (6, 3):Frame2D(Point2D((-deltaz / 2 - deltax / 2, 0)), Vector2D((1, 0)), Vector2D((0, 1))), 
             (4, 5):Frame2D(Point2D((-deltax / 2 - deltay / 2, 0)), Vector2D((0, 1)), Vector2D((-1, 0))), 
             (5, 4):Frame2D(Point2D((0, -deltax / 2 - deltay / 2)), Vector2D((0, -1)), Vector2D((1, 0))), 
             (4, 6):Frame2D(Point2D((0, -deltaz / 2 - deltay / 2)), Vector2D((0, -1)), Vector2D((1, 0))), 
             (6, 4):Frame2D(Point2D((-deltaz / 2 - deltay / 2, 0)), Vector2D((0, 1)), Vector2D((-1, 0))), 
             (5, 6):Frame2D(Point2D((-deltaz / 2 - deltax / 2, 0)), Vector2D((0, 1)), Vector2D((-1, 0))), 
             (6, 5):Frame2D(Point2D((0, -deltaz / 2 - deltax / 2)), Vector2D((0, -1)), Vector2D((1, 0)))}
            point1_2d = point1_2d_coordinate_dict[face_point1]
            point2_2d = point2_2d_coordinate_dict[face_point2]
            if opposite_face_dict[face_point1] != face_point2:
                frame = combination_dict[(face_point1, face_point2)]
                net_point2 = frame.OldCoordinates(point2_2d)
                net_line = LineSegment2D(point1_2d, net_point2)
                vertex_points = vertex_2d_coordinate_dict[face_point1]
                edge_lines = [LineSegment2D(p1, p2) for p1, p2 in zip(vertex_points, vertex_points[1:] + [vertex_points[0]])]
                for line in edge_lines:
                    edge_intersection_point, a, b = Point2D.LinesIntersection(net_line, line, curvilinear_abscissa=True)
                    if edge_intersection_point is not None and a > 0 and a < 1 and b > 0 and b < 1:
                        break

                offset_indice, offset, indice1, indice2 = vertex_to_3d_dict[face_point1]
                disordered_coordinate = [(indice1, edge_intersection_point[0] + offset_dict[indice1]),
                 (
                  indice2, edge_intersection_point[1] + offset_dict[indice2]),
                 (
                  offset_indice, offset)]
                disordered_coordinate = sorted(disordered_coordinate, key=(lambda a: a[0]))
                intersection_point_3d = Point3D(tuple([p[1] for p in disordered_coordinate]))
                mesures = [
                 Measure3D(point1_copy, intersection_point_3d),
                 Measure3D(intersection_point_3d, point2_copy)]
                return mesures
            net_points2_and_frame = []
            faces_number = [
             1, 2, 3, 4, 5, 6]
            faces_number.remove(face_point1)
            faces_number.remove(face_point2)
            pathes = []
            for face_nb in faces_number:
                path = [
                 (
                  face_point1, face_nb), (face_nb, face_point2)]
                pathes.append(path)

            for path in pathes:
                frame1 = combination_dict[(path[0][0], path[0][1])]
                frame2 = combination_dict[(path[1][0], path[1][1])]
                frame = frame1 + frame2
                net_points2_and_frame.append((Point2D(frame.OldCoordinates(point2_2d).vector), frame))

            net_point2, frame = min(net_points2_and_frame, key=(lambda pt: pt[0].point_distance(point1_2d)))
            net_line = LineSegment2D(point1_2d, net_point2)
            vertex_points = vertex_2d_coordinate_dict[face_point1]
            edge_lines = [LineSegment2D(p1, p2) for p1, p2 in zip(vertex_points, vertex_points[1:] + [vertex_points[0]])]
            for line in edge_lines:
                edge_intersection_point1, a, b = Point2D.LinesIntersection(net_line, line, curvilinear_abscissa=True)
                if edge_intersection_point1 is not None and a > 0 and a < 1 and b > 0 and b < 1:
                    break

            offset_indice, offset, indice1, indice2 = vertex_to_3d_dict[face_point1]
            disordered_coordinate = [(indice1, edge_intersection_point1[0] + offset_dict[indice1]),
             (
              indice2, edge_intersection_point1[1] + offset_dict[indice2]),
             (
              offset_indice, offset)]
            disordered_coordinate = sorted(disordered_coordinate, key=(lambda a: a[0]))
            intersection_point1_3d = Point3D(tuple([p[1] for p in disordered_coordinate]))
            vertex_points = [frame.OldCoordinates(p) for p in vertex_2d_coordinate_dict[face_point2]]
            edge_lines = [LineSegment2D(p1, p2) for p1, p2 in zip(vertex_points, vertex_points[1:] + [vertex_points[0]])]
            for line in edge_lines:
                edge_intersection_point2, a, b = Point2D.LinesIntersection(net_line, line, curvilinear_abscissa=True)
                if edge_intersection_point2 is not None and a > 0 and a < 1 and b > 0 and b < 1:
                    break

            edge_intersection_point2 = Point2D(frame.NewCoordinates(edge_intersection_point2))
            offset_indice, offset, indice1, indice2 = vertex_to_3d_dict[face_point2]
            disordered_coordinate = [(indice1, edge_intersection_point2[0] + offset_dict[indice1]),
             (
              indice2, edge_intersection_point2[1] + offset_dict[indice2]),
             (
              offset_indice, offset)]
            disordered_coordinate = sorted(disordered_coordinate, key=(lambda a: a[0]))
            intersection_point2_3d = Point3D(tuple([p[1] for p in disordered_coordinate]))
            if point1 == point1_copy:
                mesures = [
                 Measure3D(point1, intersection_point1_3d),
                 Measure3D(intersection_point1_3d, intersection_point2_3d),
                 Measure3D(intersection_point2_3d, point2)]
        else:
            mesures = [
             Measure3D(point2, intersection_point2_3d),
             Measure3D(intersection_point2_3d, intersection_point1_3d),
             Measure3D(intersection_point1_3d, point1)]
        return mesures

    def babylon_script(self):
        height = self.ymax - self.ymin
        width = self.xmax - self.xmin
        depth = self.zmax - self.zmin
        s = 'var box = BABYLON.MeshBuilder.CreateBox("box", {{height: {}, width: {}, depth: {}}}, scene);\n'.format(height, width, depth)
        s += 'box.setPositionWithLocalVector(new BABYLON.Vector3({},{},{}));\n'.format(self.center[0], self.center[1], self.center[2])
        s += 'var bboxmat = new BABYLON.StandardMaterial("bboxmat", scene);\n'
        s += 'bboxmat.alpha = 0.4;\n'
        s += 'var DTWidth = {};\n'.format(width * 60)
        s += 'var DTHeight = {};\n'.format(height * 60)
        s += 'var font_type = "Arial";\n'
        s += 'var text = "{}";\n'.format(self.name)
        s += 'var dynamicTexture = new BABYLON.DynamicTexture("DynamicTexture", {width:DTWidth, height:DTHeight}, scene);\n'
        s += 'var ctx = dynamicTexture.getContext();\n'
        s += 'var size = 0.8;\n'
        s += 'ctx.font = size + "px " + font_type;\n'
        s += 'var textWidth = ctx.measureText(text).width;\n'
        s += 'var ratio = textWidth/size;\n'
        s += 'var font_size = Math.floor(DTWidth / ratio);\n'
        s += 'var font = font_size + "px " + font_type;\n'
        s += 'dynamicTexture.drawText(text, null, null, font, "#000000", "#ffffff", false);\n'
        s += 'bboxmat.diffuseTexture = dynamicTexture;\n'
        s += 'box.material = bboxmat;\n'
        return s


class Measure2D(LineSegment2D):

    def __init__(self, point1, point2, label='', unit='mm', type_='distance'):
        """
        :param unit: 'mm', 'm' or None. If None, the distance won't be in the label

        """
        LineSegment2D.__init__(self, point1, point2)
        self.label = label
        self.unit = unit
        self.type_ = type_

    def MPLPlot(self, ax, ndigits=6):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        xm, ym = 0.5 * (self.points[0] + self.points[1])
        distance = self.points[1].point_distance(self.points[0])
        if self.label != '':
            label = '{}: '.format(self.label)
        else:
            label = ''
        if self.unit == 'mm':
            label += '{} mm'.format(round(distance * 1000, ndigits))
        else:
            label += '{} m'.format(round(distance, ndigits))
        if self.type_ == 'distance':
            arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='<|-|>,head_length=10,head_width=5',
              shrinkA=0,
              shrinkB=0,
              color='k')
        else:
            if self.type_ == 'radius':
                arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>,head_length=10,head_width=5',
                  shrinkA=0,
                  shrinkB=0,
                  color='k')
            else:
                ax.add_patch(arrow)
                if x2 - x1 == 0.0:
                    theta = 90.0
                else:
                    theta = math.degrees(math.atan((y2 - y1) / (x2 - x1)))
            ax.text(xm, ym, label, va='bottom', ha='center', rotation=theta)


class Measure3D(Line3D):

    def __init__(self, point1, point2, color=(1, 0, 0)):
        self.points = [
         point1, point2]
        self.color = color
        self.distance = Vector3D(self.points[0] - self.points[1]).Norm()
        self.bounding_box = self._bounding_box()

    def __hash__(self):
        return sum([hash(p) for p in self.points])

    def babylon_script(self):
        s = 'var myPoints = [];\n'
        s += 'var point1 = new BABYLON.Vector3({},{},{});\n'.format(self.points[0][0], self.points[0][1], self.points[0][2])
        s += 'myPoints.push(point1);\n'
        s += 'var point2 = new BABYLON.Vector3({},{},{});\n'.format(self.points[1][0], self.points[1][1], self.points[1][2])
        s += 'myPoints.push(point2);\n'
        s += 'var line = BABYLON.MeshBuilder.CreateLines("lines", {points: myPoints}, scene);\n'
        s += 'line.color = new BABYLON.Color3({}, {}, {});\n'.format(self.color[0], self.color[1], self.color[2])
        return s


class Group:

    def __init__(self, primitives, name):
        self.primitives = primitives
        self.name = name


class StepFunction:

    def __init__(self, function_id, function_name, function_arg):
        self.id = function_id
        self.name = function_name
        self.arg = function_arg
        if self.name == '':
            if self.arg[1][0] == 'B_SPLINE_SURFACE':
                self.simplify('B_SPLINE_SURFACE')
            if self.arg[1][0] == 'B_SPLINE_CURVE':
                self.simplify('B_SPLINE_CURVE')

    def simplify(self, new_name):
        args = [subfun[1] for i, subfun in enumerate(self.arg) if not len(subfun[1]) != 0 if i == 0]
        arguments = []
        for arg in args:
            if arg == []:
                arguments.append('')
            else:
                arguments.extend(arg)

        arguments.pop()
        self.name = new_name
        self.arg = arguments


class Step:

    def __init__(self, stepfile):
        self.stepfile = stepfile
        self.functions, self.all_connections = self.read_functions()
        self.graph = self.create_graph()

    def read_functions(self):
        f = open((self.stepfile), 'r', encoding='ISO-8859-1')
        all_connections = []
        previous_line = ''
        functions = {}
        for line in f:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            if not line:
                continue
            if line[(-1)] != ';':
                previous_line = previous_line + line
                continue
            line = previous_line + line
            if line[0] != '#':
                previous_line = str()
                continue
            function = line.split('=')
            function_id = int(function[0][1:])
            function_name_arg = function[1].split('(', 1)
            function_name = function_name_arg[0]
            function_arg = function_name_arg[1].split('#')
            function_connections = []
            for connec in function_arg[1:]:
                connec = connec.split(',')
                connec = connec[0].split(')')
                function_connection = int(connec[0])
                function_connections.append((function_id, function_connection))

            all_connections.extend(function_connections)
            previous_line = str()
            function_arg = function_name_arg[1]
            arguments = step_split_arguments(function_arg)
            if function_name == '':
                arguments = self.step_subfunctions(arguments)
            for i, argument in enumerate(arguments):
                if argument[:2] == '(#' and argument[(-1)] == ')':
                    arg_list = set_to_list(argument)
                    arguments[i] = arg_list

            function = StepFunction(function_id, function_name, arguments)
            functions[function_id] = function

        f.close()
        return (
         functions, all_connections)

    def create_graph(self, draw=False, html=False):
        G = nx.Graph()
        F = nx.DiGraph()
        labels = {}
        for function in self.functions.values():
            if function.name in step_to_volmdlr_primitive:
                G.add_node(function.id)
                F.add_node(function.id)
                labels[function.id] = str(function.id) + ' ' + function.name

        node_list = list(F.nodes())
        delete_connection = []
        for connection in self.all_connections:
            if connection[0] not in node_list or connection[1] not in node_list:
                delete_connection.append(connection)

        for delete in delete_connection:
            self.all_connections.remove(delete)

        G.add_edges_from(self.all_connections)
        F.add_edges_from(self.all_connections)
        delete_nodes = []
        for node in F.nodes:
            if F.degree(node) == 0:
                delete_nodes.append(node)

        for node in delete_nodes:
            F.remove_node(node)
            G.remove_node(node)

        if draw:
            pos = nx.kamada_kawai_layout(G)
            plt.figure()
            nx.draw_networkx_nodes(F, pos)
            nx.draw_networkx_edges(F, pos)
            nx.draw_networkx_labels(F, pos, labels)
        if html:
            env = Environment(loader=(PackageLoader('powertransmission', 'templates')), autoescape=(select_autoescape(['html', 'xml'])))
            template = env.get_template('graph_visJS.html')
            nodes = []
            edges = []
            for label in list(labels.values()):
                nodes.append({'name':label,  'shape':'circular'})

            for edge in G.edges:
                edge_dict = {}
                edge_dict['inode1'] = int(edge[0]) - 1
                edge_dict['inode2'] = int(edge[1]) - 1
                edges.append(edge_dict)

            options = {}
            s = template.render(name=(self.stepfile),
              nodes=nodes,
              edges=edges,
              options=options)
            with open('graph_visJS.html', 'wb') as (file):
                file.write(s.encode('utf-8'))
            webbrowser.open('file://' + os.path.realpath('graph_visJS.html'))
        return F

    def draw_graph(self):
        labels = {}
        for id_nb, function in self.functions.items():
            labels[id_nb] = str(id_nb) + ' ' + function.name

        pos = nx.kamada_kawai_layout(self.graph)
        plt.figure()
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos, labels)

    def step_subfunctions(self, subfunctions):
        subfunctions = subfunctions[0]
        parenthesis_count = 0
        subfunction_names = []
        subfunction_args = []
        subfunction_name = ''
        subfunction_arg = ''
        for char in subfunctions:
            if char == '(':
                parenthesis_count += 1
                if parenthesis_count == 1:
                    subfunction_names.append(subfunction_name)
                    subfunction_name = ''
                else:
                    subfunction_arg += char
                    continue
            if char == ')':
                parenthesis_count -= 1
                if parenthesis_count == 0:
                    subfunction_args.append(subfunction_arg)
                    subfunction_arg = ''
                else:
                    subfunction_arg += char
                    continue
                    subfunction_name += char
            else:
                subfunction_arg += char

        return [(subfunction_names[i], step_split_arguments(subfunction_args[i])) for i in range(len(subfunction_names))]

    def instanciate(self, instanciate_id, object_dict, primitives):
        """
        Returns None if the object was instanciate
        """
        name = self.functions[instanciate_id].name
        arguments = self.functions[instanciate_id].arg[:]
        for i, arg in enumerate(arguments):
            if type(arg) == str and arg[0] == '#':
                arguments[i] = int(arg[1:])

        if name == 'VERTEX_POINT':
            object_dict[instanciate_id] = object_dict[arguments[1]]
        else:
            if name == 'ORIENTED_EDGE':
                object_dict[instanciate_id] = object_dict[arguments[3]]
            else:
                if name == 'FACE_OUTER_BOUND':
                    object_dict[instanciate_id] = object_dict[arguments[1]]
                else:
                    if name == 'FACE_BOUND':
                        object_dict[instanciate_id] = object_dict[arguments[1]]
                    else:
                        if name == 'SURFACE_CURVE':
                            pass
                        else:
                            if name in step_to_volmdlr_primitive:
                                if hasattr(step_to_volmdlr_primitive[name], 'from_step'):
                                    volmdlr_object = step_to_volmdlr_primitive[name].from_step(arguments, object_dict)
                                    object_dict[instanciate_id] = volmdlr_object
                                    if hasattr(volmdlr_object, 'primitive'):
                                        primitives.append(volmdlr_object.primitive)
                            return (
                             None, object_dict, primitives)

    def to_shells3d(self, name):
        object_dict = {}
        primitives = []
        self.graph.add_node('#0')
        for node in self.graph.nodes:
            if node != '#0' and self.functions[node].name == 'CLOSED_SHELL':
                self.graph.add_edge('#0', node)

        edges = list(nx.algorithms.traversal.breadth_first_search.bfs_edges(self.graph, '#0'))[::-1]
        for edge_nb, edge in enumerate(edges):
            instanciate_id = edge[1]
            res, object_dict, primitives = self.instanciate(instanciate_id, object_dict, primitives)
            if res is not None:
                raise NotImplementedError

        shells = []
        for node in list(self.graph.nodes):
            if node != '#0' and self.functions[node].name == 'CLOSED_SHELL':
                shells.append(object_dict[node])

        return shells


class VolumeModel(dc.DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = ['shells', 'bounding_box']
    _non_eq_attributes = ['name', 'shells', 'bounding_box', 'contours', 'faces']
    _non_hash_attributes = []

    def __init__(self, primitives, name=''):
        self.primitives = primitives
        self.name = name
        if self.primitives:
            self.shells = self._extract_shells()
        if self.shells:
            self.bounding_box = self._bounding_box()

    def _extract_shells(self):
        shells = []
        for primitive in self.primitives:
            if isinstance(primitive, Shell3D):
                shells.append(primitive)

        return shells

    def Volume(self):
        volume = 0
        for primitive in self.primitives:
            volume += primitive.Volume()

        return volume

    def Rotation(self, center, axis, angle, copy=True):
        if copy:
            new_primitives = [primitive.Rotation(center, axis, angle, copy=True) for primitive in self.primitives]
            return VolumeModel(new_primitives, self.name)
        for primitives in self.primitives:
            primitives.Translation(center, axis, angle, copy=False)

        self.bounding_box = self._bounding_box()

    def Translation(self, offset, copy=True):
        if copy:
            new_primitives = [primitive.Translation(offset, copy=True) for primitive in self.primitives]
            return VolumeModel(new_primitives, self.name)
        for primitives in self.primitives:
            primitives.Translation(offset, copy=False)

        self.bounding_box = self._bounding_box()

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            new_primitives = [primitive.frame_mapping(frame, side, copy=True) for primitive in self.primitives]
            return VolumeModel(new_primitives, self.name)
        for primitives in self.primitives:
            primitives.frame_mapping(frame, side, copy=False)

        self.bounding_box = self._bounding_box()

    def copy(self):
        new_primitives = [primitive.copy() for primitive in self.primitives]
        return VolumeModel(new_primitives, self.name)

    def _bounding_box(self):
        bboxes = []
        for primitive in self.primitives:
            if hasattr(primitive, 'bounding_box'):
                bboxes.append(primitive.bounding_box)

        xmin = min([box.xmin for box in bboxes])
        xmax = max([box.xmax for box in bboxes])
        ymin = min([box.ymin for box in bboxes])
        ymax = max([box.ymax for box in bboxes])
        zmin = min([box.zmin for box in bboxes])
        zmax = max([box.zmax for box in bboxes])
        return BoundingBox(xmin, xmax, ymin, ymax, zmin, zmax)

    def plot(self, ax=None, color=None):
        fig = plt.figure()
        if ax is None:
            ax = fig.add_subplot(111, projection='3d')
        for i, shell in enumerate(self.shells):
            bbox = shell.bbox()
            bbox.plot(ax, color[i])

        return ax

    def MPLPlot(self):
        """
        Matplotlib plot of model.
        To use for debug.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d', adjustable='box')
        for primitive in self.primitives:
            primitive.MPLPlot(ax)

        ax.set_aspect('equal')
        ax.margins(0.1)
        return (fig, ax)

    def FreeCADScript--- This code section failed: ---

 L.4591         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              abspath
                6  LOAD_FAST                'fcstd_filepath'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'fcstd_filepath'

 L.4592        12  LOAD_FAST                'fcstd_filepath'
               14  LOAD_METHOD              replace
               16  LOAD_STR                 '\\'
               18  LOAD_STR                 '\\\\'
               20  CALL_METHOD_2         2  '2 positional arguments'
               22  STORE_FAST               'fcstd_filepath'

 L.4593        24  LOAD_FAST                'freecad_lib_path'
               26  LOAD_METHOD              replace
               28  LOAD_STR                 '\\'
               30  LOAD_STR                 '\\\\'
               32  CALL_METHOD_2         2  '2 positional arguments'
               34  STORE_FAST               'freecad_lib_path'

 L.4595        36  LOAD_STR                 '# -*- coding: utf-8 -*-\n'
               38  STORE_FAST               's'

 L.4596        40  LOAD_FAST                'freecad_lib_path'
               42  LOAD_STR                 ''
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    64  'to 64'

 L.4597        48  LOAD_FAST                's'
               50  LOAD_STR                 "import sys\nsys.path.append('"
               52  LOAD_FAST                'freecad_lib_path'
               54  BINARY_ADD       
               56  LOAD_STR                 "')\n"
               58  BINARY_ADD       
               60  INPLACE_ADD      
               62  STORE_FAST               's'
             64_0  COME_FROM            46  '46'

 L.4599        64  LOAD_FAST                's'
               66  LOAD_STR                 "import math\nimport FreeCAD as fc\nimport Part\n\ndoc=fc.newDocument('doc')\n\n"
               68  INPLACE_ADD      
               70  STORE_FAST               's'

 L.4600        72  SETUP_LOOP          284  'to 284'
               74  LOAD_GLOBAL              enumerate
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                primitives
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  GET_ITER         
             84_0  COME_FROM           168  '168'
             84_1  COME_FROM           150  '150'
               84  FOR_ITER            282  'to 282'
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'ip'
               90  STORE_FAST               'primitive'

 L.4601        92  LOAD_FAST                'primitive'
               94  LOAD_ATTR                name
               96  LOAD_STR                 ''
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   114  'to 114'

 L.4602       102  LOAD_STR                 'Primitive_{}'
              104  LOAD_METHOD              format
              106  LOAD_FAST                'ip'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  STORE_FAST               'primitive_name'
              112  JUMP_FORWARD        128  'to 128'
            114_0  COME_FROM           100  '100'

 L.4604       114  LOAD_STR                 'Primitive_{}_{}'
              116  LOAD_METHOD              format
              118  LOAD_FAST                'ip'
              120  LOAD_FAST                'primitive'
              122  LOAD_ATTR                name
              124  CALL_METHOD_2         2  '2 positional arguments'
              126  STORE_FAST               'primitive_name'
            128_0  COME_FROM           112  '112'

 L.4605       128  LOAD_FAST                's'
              130  LOAD_STR                 "part = doc.addObject('App::Part','{}')\n"
              132  LOAD_METHOD              format
              134  LOAD_FAST                'primitive_name'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  INPLACE_ADD      
              140  STORE_FAST               's'

 L.4606       142  LOAD_GLOBAL              hasattr
              144  LOAD_FAST                'primitive'
              146  LOAD_STR                 'FreeCADExport'
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  POP_JUMP_IF_FALSE    84  'to 84'

 L.4607       152  LOAD_FAST                'primitive'
              154  LOAD_METHOD              FreeCADExport
              156  LOAD_FAST                'ip'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  STORE_FAST               'sp'

 L.4608       162  LOAD_FAST                'sp'
              164  LOAD_STR                 ''
              166  COMPARE_OP               !=
              168  POP_JUMP_IF_FALSE    84  'to 84'

 L.4610       170  LOAD_FAST                's'
              172  LOAD_FAST                'sp'
              174  INPLACE_ADD      
              176  STORE_FAST               's'

 L.4611       178  LOAD_FAST                's'
              180  LOAD_STR                 'shapeobj = doc.addObject("Part::Feature","{}")\n'
              182  LOAD_METHOD              format
              184  LOAD_FAST                'primitive_name'
              186  CALL_METHOD_1         1  '1 positional argument'
              188  INPLACE_ADD      
              190  STORE_FAST               's'

 L.4612       192  LOAD_GLOBAL              isinstance
              194  LOAD_FAST                'primitive'
              196  LOAD_GLOBAL              BSplineCurve3D
              198  CALL_FUNCTION_2       2  '2 positional arguments'
              200  POP_JUMP_IF_TRUE    232  'to 232'

 L.4613       202  LOAD_GLOBAL              isinstance
              204  LOAD_FAST                'primitive'
              206  LOAD_GLOBAL              BSplineSurface3D
              208  CALL_FUNCTION_2       2  '2 positional arguments'
              210  POP_JUMP_IF_TRUE    232  'to 232'

 L.4614       212  LOAD_GLOBAL              isinstance
              214  LOAD_FAST                'primitive'
              216  LOAD_GLOBAL              Circle3D
              218  CALL_FUNCTION_2       2  '2 positional arguments'
              220  POP_JUMP_IF_TRUE    232  'to 232'

 L.4615       222  LOAD_GLOBAL              isinstance
              224  LOAD_FAST                'primitive'
              226  LOAD_GLOBAL              Ellipse3D
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  POP_JUMP_IF_FALSE   248  'to 248'
            232_0  COME_FROM           220  '220'
            232_1  COME_FROM           210  '210'
            232_2  COME_FROM           200  '200'

 L.4619       232  LOAD_FAST                's'
              234  LOAD_STR                 'shapeobj.Shape = primitive{}.toShape()\n'
              236  LOAD_METHOD              format
              238  LOAD_FAST                'ip'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  INPLACE_ADD      
              244  STORE_FAST               's'
              246  JUMP_FORWARD        262  'to 262'
            248_0  COME_FROM           230  '230'

 L.4621       248  LOAD_FAST                's'
              250  LOAD_STR                 'shapeobj.Shape = primitive{}\n'
              252  LOAD_METHOD              format
              254  LOAD_FAST                'ip'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  INPLACE_ADD      
              260  STORE_FAST               's'
            262_0  COME_FROM           246  '246'

 L.4622       262  LOAD_FAST                's'
              264  LOAD_STR                 'part.addObject(shapeobj)\n\n'
              266  LOAD_METHOD              format
              268  LOAD_FAST                'ip'
              270  LOAD_FAST                'primitive'
              272  LOAD_ATTR                name
              274  CALL_METHOD_2         2  '2 positional arguments'
              276  INPLACE_ADD      
              278  STORE_FAST               's'
              280  JUMP_BACK            84  'to 84'
              282  POP_BLOCK        
            284_0  COME_FROM_LOOP       72  '72'

 L.4628       284  LOAD_FAST                's'
              286  LOAD_STR                 'doc.recompute()\n'
              288  INPLACE_ADD      
              290  STORE_FAST               's'

 L.4629       292  LOAD_STR                 'fcstd'
              294  LOAD_FAST                'export_types'
              296  COMPARE_OP               in
          298_300  POP_JUMP_IF_FALSE   318  'to 318'

 L.4630       302  LOAD_FAST                's'
              304  LOAD_STR                 "doc.saveAs('"
              306  LOAD_FAST                'fcstd_filepath'
              308  BINARY_ADD       
              310  LOAD_STR                 ".fcstd')\n\n"
              312  BINARY_ADD       
              314  INPLACE_ADD      
              316  STORE_FAST               's'
            318_0  COME_FROM           298  '298'

 L.4631       318  LOAD_STR                 'stl'
              320  LOAD_FAST                'export_types'
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   344  'to 344'

 L.4632       328  LOAD_FAST                's'
              330  LOAD_STR                 "import Mesh\nMesh.export(doc.Objects,'{}.stl', tolerance={})\n"
              332  LOAD_METHOD              format
              334  LOAD_FAST                'fcstd_filepath'
              336  LOAD_FAST                'tolerance'
              338  CALL_METHOD_2         2  '2 positional arguments'
              340  INPLACE_ADD      
              342  STORE_FAST               's'
            344_0  COME_FROM           324  '324'

 L.4633       344  LOAD_STR                 'step'
              346  LOAD_FAST                'export_types'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   368  'to 368'

 L.4634       354  LOAD_FAST                's'
              356  LOAD_STR                 "Part.export(doc.Objects,'{}.step')\n"
              358  LOAD_METHOD              format
              360  LOAD_FAST                'fcstd_filepath'
              362  CALL_METHOD_1         1  '1 positional argument'
              364  INPLACE_ADD      
              366  STORE_FAST               's'
            368_0  COME_FROM           350  '350'

 L.4637       368  LOAD_FAST                'save_to'
              370  LOAD_STR                 ''
              372  COMPARE_OP               !=
          374_376  POP_JUMP_IF_FALSE   418  'to 418'

 L.4638       378  LOAD_GLOBAL              open
              380  LOAD_GLOBAL              os
              382  LOAD_ATTR                path
              384  LOAD_METHOD              abspath
              386  LOAD_FAST                'save_to'
              388  CALL_METHOD_1         1  '1 positional argument'
              390  LOAD_STR                 'w'
              392  CALL_FUNCTION_2       2  '2 positional arguments'
              394  SETUP_WITH          412  'to 412'
              396  STORE_FAST               'file'

 L.4639       398  LOAD_FAST                'file'
              400  LOAD_METHOD              write
              402  LOAD_FAST                's'
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          
              408  POP_BLOCK        
              410  LOAD_CONST               None
            412_0  COME_FROM_WITH      394  '394'
              412  WITH_CLEANUP_START
              414  WITH_CLEANUP_FINISH
              416  END_FINALLY      
            418_0  COME_FROM           374  '374'

 L.4640       418  LOAD_FAST                's'
              420  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 246

    def FreeCADExport(self, fcstd_filepath, python_path='python', freecad_lib_path='/usr/lib/freecad/lib', export_types=('fcstd',), tolerance=0.0001):
        r"""
        Export model to .fcstd FreeCAD standard

        :param python_path: path of python binded to freecad

            * on windows: something like C:\\Program Files\\FreeCAD X.XX\\bin\\python
            * on linux: python if installed by a dstribution package
        :param filepath: path of fcstd file (without extension)
        :param freecad_lib_path: FreeCAD.so lib path (/usr/lib/freecad/lib in general)
        :param tolerance: the tolerance of tesselation for mesh exports

        """
        fcstd_filepath = os.path.abspath(fcstd_filepath)
        s = self.FreeCADScript(fcstd_filepath, freecad_lib_path=freecad_lib_path,
          export_types=export_types,
          tolerance=tolerance)
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as (f):
            f.write(bytes(s, 'utf8'))
        arg = f.name
        output = subprocess.call([python_path, arg])
        f.close()
        os.remove(f.name)
        return output

    def babylon_script(self, use_cdn=True, debug=False):
        env = Environment(loader=(PackageLoader('volmdlr', 'templates')), autoescape=(select_autoescape(['html', 'xml'])))
        template = env.get_template('babylon.html')
        bbox = self._bounding_box()
        center = bbox.center
        max_length = max([bbox.xmax - bbox.xmin,
         bbox.ymax - bbox.ymin,
         bbox.zmax - bbox.zmin])
        primitives_strings = []
        for primitive in self.primitives:
            if hasattr(primitive, 'babylon_script'):
                print(primitive)
                primitives_strings.append(primitive.babylon_script())

        return template.render(name=(self.name), center=(tuple(center)),
          length=(2 * max_length),
          primitives_strings=primitives_strings,
          use_cdn=use_cdn,
          debug=debug)

    def babylonjs_from_script(self, page_name=None, use_cdn=True, debug=False):
        script = self.babylon_script(use_cdn=use_cdn, debug=debug)
        if page_name is None:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as (file):
                file.write(bytes(script, 'utf8'))
            page_name = file.name
        else:
            page_name += '.html'
            with open(page_name, 'w') as (file):
                file.write(script)
        webbrowser.open('file://' + os.path.realpath(page_name))

    def babylon_data(self):
        meshes = []
        for primitive in self.primitives:
            if hasattr(primitive, 'babylon_meshes'):
                meshes.extend(primitive.babylon_meshes())

        bbox = self._bounding_box()
        center = bbox.center
        max_length = max([bbox.xmax - bbox.xmin,
         bbox.ymax - bbox.ymin,
         bbox.zmax - bbox.zmin])
        babylon_data = {'meshes':meshes, 
         'max_length':max_length, 
         'center':list(center)}
        return babylon_data

    @classmethod
    def babylonjs_from_babylon_data(cls, babylon_data, page_name=None, use_cdn=True, debug=False):
        env = Environment(loader=(PackageLoader('volmdlr', 'templates')), autoescape=(select_autoescape(['html', 'xml'])))
        template = env.get_template('babylon_unpacker.html')
        script = template.render(babylon_data=babylon_data, use_cdn=use_cdn,
          debug=debug)
        if page_name is None:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as (file):
                file.write(bytes(script, 'utf8'))
            page_name = file.name
        else:
            page_name += '.html'
            with open(page_name, 'w') as (file):
                file.write(script)
        webbrowser.open('file://' + os.path.realpath(page_name))

    def babylonjs(self, page_name=None, use_cdn=True, debug=False):
        babylon_data = self.babylon_data()
        self.babylonjs_from_babylon_data(babylon_data, page_name=page_name, use_cdn=use_cdn,
          debug=debug)


class MovingVolumeModel(VolumeModel):

    def __init__(self, primitives, step_frames, name=''):
        VolumeModel.__init__(self, primitives=primitives, name=name)
        self.step_frames = step_frames
        if not self.is_consistent():
            raise dc.ConsistencyError

    def is_consistent(self):
        n_primitives = len(self.primitives)
        for frames in self.step_frames:
            if len(frames) != n_primitives:
                return False

        return True

    def step_volume_model(self, istep):
        primitives = []
        for primitive, frame in zip(self.primitives, self.step_frames[istep]):
            primitives.append(primitive.frame_mapping(frame, side='old', copy=True))

        return VolumeModel(primitives)

    def babylon_script(self, use_cdn=True, debug=False):
        env = Environment(loader=(PackageLoader('volmdlr', 'templates')), autoescape=(select_autoescape(['html', 'xml'])))
        template = env.get_template('babylon.html')
        bbox = self._bounding_box()
        center = bbox.center
        max_length = max([bbox.xmax - bbox.xmin,
         bbox.ymax - bbox.ymin,
         bbox.zmax - bbox.zmin])
        primitives_strings = []
        for primitive in self.primitives:
            if hasattr(primitive, 'babylon_script'):
                primitives_strings.append(primitive.babylon_script())

        positions = []
        orientations = []
        for step in self.step_frames:
            step_positions = []
            step_orientations = []
            for frame in step:
                step_positions.append(list(frame.origin))
                step_orientations.append([list(frame.u),
                 list(frame.v),
                 list(frame.w)])

            positions.append(step_positions)
            orientations.append(step_orientations)

        return template.render(name=(self.name), center=(tuple(center)),
          length=(2 * max_length),
          primitives_strings=primitives_strings,
          positions=positions,
          orientations=orientations,
          use_cdn=use_cdn,
          debug=debug)

    def babylon_data(self):
        meshes = []
        primitives_to_meshes = []
        for ip, primitive in enumerate(self.primitives):
            if hasattr(primitive, 'babylon_meshes'):
                meshes.extend(primitive.babylon_meshes())
                primitives_to_meshes.append(ip)

        bbox = self._bounding_box()
        center = bbox.center
        max_length = max([bbox.xmax - bbox.xmin,
         bbox.ymax - bbox.ymin,
         bbox.zmax - bbox.zmin])
        steps = []
        for istep, frames in enumerate(self.step_frames):
            step = {'time': istep}
            for iframe, frame in enumerate(frames):
                if iframe in primitives_to_meshes:
                    imesh = primitives_to_meshes.index(iframe)
                    step[imesh] = {}
                    step[imesh]['position'] = list(round(frame.origin, 6))
                    step[imesh]['orientations'] = [list(round(frame.u, 6)),
                     list(round(frame.v, 6)),
                     list(round(frame.w, 6))]

            steps.append(step)

        babylon_data = {'meshes':meshes,  'max_length':max_length, 
         'center':list(center), 
         'steps':steps}
        return babylon_data


class Routing:

    def __init__(self, point1, point2, volumemodel):
        self.points = [
         point1, point2]
        self.volumemodel = volumemodel

    def straight_line(self):
        """
        Returns 2 distances :
            - no collision distance
            - collision distance
        """
        line = LineSegment3D(self.points[0], self.points[1])
        intersection_points = []
        abscissea_list = []
        for shell in self.volumemodel.shells:
            for face in shell.faces:
                intersection_point, intersection_abscissea = face.linesegment_intersection(line, abscissea=True)
                if intersection_point is not None and intersection_abscissea != 0 and intersection_abscissea != 1:
                    not_in_abscissea_list = True
                    for abscissea in abscissea_list:
                        if math.isclose(abscissea, intersection_abscissea, abs_tol=1e-08):
                            not_in_abscissea_list = False

                    if not_in_abscissea_list:
                        intersection_points.append((intersection_point, intersection_abscissea))
                        abscissea_list.append(intersection_abscissea)

        if len(intersection_points) % 2 != 0:
            raise NotImplementedError
        intersection_points = sorted(intersection_points, key=(lambda abscissea: abscissea[1]))
        all_points_abscissea = [(self.points[0], 0)] + intersection_points[:] + [(self.points[1], 1)]
        all_points = [p[0] for p in all_points_abscissea]
        no_collision_mesures = []
        collision_mesures = []
        i = 0
        for pt1, pt2 in zip(all_points[:-1], all_points[1:]):
            if i % 2 == 0:
                no_collision_mesures.append(Measure3D(pt1, pt2, color=(0, 0, 1)))
            else:
                collision_mesures.append(Measure3D(pt1, pt2, color=(1, 0, 0)))
            i += 1

        return (no_collision_mesures, collision_mesures)

    def straight_line2(self):
        """
        Returns the distance of the line going around each shell's bbox encountered along the path
        """
        line = LineSegment3D(self.points[0], self.points[1])
        all_mesures_abscissea = []
        intersection_points = []
        for shell in self.volumemodel.shells:
            shell_intersection_points = []
            bbox = shell.bounding_box
            for face in shell.faces:
                intersection_point, intersection_abscissea = face.linesegment_intersection(line, abscissea=True)
                if intersection_point is not None and intersection_abscissea != 0 and intersection_abscissea != 1:
                    intersection_points.append((intersection_point, intersection_abscissea))
                    shell_intersection_points.append((intersection_point, intersection_abscissea))

            if len(shell_intersection_points) == 2:
                shell_intersection_points = sorted(shell_intersection_points, key=(lambda abscissea: abscissea[1]))
                abscissea1 = shell_intersection_points[0][1]
                abscissea2 = shell_intersection_points[1][1]
                shell_intersection_points = [p[0] for p in shell_intersection_points]
                around_bbox_mesures = bbox.distance_between_two_points_on_bbox(shell_intersection_points[0], shell_intersection_points[1])
                all_mesures_abscissea.append((around_bbox_mesures, abscissea1, abscissea2))
            elif len(shell_intersection_points) > 2 or len(shell_intersection_points) == 1:
                raise NotImplementedError

        intersection_points = sorted(intersection_points, key=(lambda abscissea: abscissea[1]))
        all_mesures_abscissea = sorted(all_mesures_abscissea, key=(lambda abscissea: abscissea[1]))
        all_points_abscissea = [(self.points[0], 0)] + intersection_points[:] + [(self.points[1], 1)]
        all_points = [p[0] for p in all_points_abscissea]
        no_collision_mesures = []
        i = 0
        for pt1, pt2 in zip(all_points[:-1], all_points[1:]):
            if i % 2 == 0:
                no_collision_mesures.append(Measure3D(pt1, pt2, color=(0, 0, 1)))
            else:
                no_collision_mesures.extend(all_mesures_abscissea[(i // 2)][0])
            i += 1

        return no_collision_mesures


class ViewIso:

    def __init__(self, component, frame, size):
        self.component = component
        self.frame = frame
        self.size = size
        self.plot_datas = self.plot_data()

    def plot_data(self, detail=True):
        wide = min(self.size) / 2
        plot_datas = []
        plot_datas.extend(self.component.plot_data((self.frame), detail=detail))
        plot_datas.extend(self.component.plot_data((Frame3D(self.frame.origin + Point3D((0, self.size[1] / 2 + self.size[2] / 2 + wide, 0)), self.frame.u, self.frame.w, self.frame.v)), detail=detail))
        plot_datas.extend(self.component.plot_data((Frame3D(self.frame.origin + Point3D((self.size[0] / 2 + self.size[2] / 2 + wide, 0, 0)), self.frame.w, self.frame.v, self.frame.u)), detail=detail))
        return plot_datas

    def plot(self):
        plot_data.plot(self.plot_datas)


step_to_volmdlr_primitive = {'CARTESIAN_POINT':Point3D, 
 'DIRECTION':Vector3D, 
 'VECTOR':Vector3D, 
 'AXIS1_PLACEMENT':None, 
 'AXIS2_PLACEMENT_2D':None, 
 'AXIS2_PLACEMENT_3D':Frame3D, 
 'LINE':Line3D, 
 'CIRCLE':Circle3D, 
 'ELLIPSE':Ellipse3D, 
 'PARABOLA':None, 
 'HYPERBOLA':None, 
 'PCURVE':None, 
 'CURVE_REPLICA':None, 
 'OFFSET_CURVE_3D':None, 
 'TRIMMED_CURVE':None, 
 'B_SPLINE_CURVE':BSplineCurve3D, 
 'B_SPLINE_CURVE_WITH_KNOTS':BSplineCurve3D, 
 'BEZIER_CURVE':BSplineCurve3D, 
 'RATIONAL_B_SPLINE_CURVE':BSplineCurve3D, 
 'UNIFORM_CURVE':BSplineCurve3D, 
 'QUASI_UNIFORM_CURVE':BSplineCurve3D, 
 'SURFACE_CURVE':None, 
 'SEAM_CURVE':LineSegment3D, 
 'COMPOSITE_CURVE_SEGMENT':None, 
 'COMPOSITE_CURVE':Wire3D, 
 'COMPOSITE_CURVE_ON_SURFACE':Wire3D, 
 'BOUNDARY_CURVE':Wire3D, 
 'PLANE':Plane3D, 
 'CYLINDRICAL_SURFACE':None, 
 'CONICAL_SURFACE':None, 
 'SPHERICAL_SURFACE':None, 
 'TOROIDAL_SURFACE':None, 
 'DEGENERATE_TOROIDAL_SURFACE':None, 
 'B_SPLINE_SURFACE_WITH_KNOTS':BSplineSurface3D, 
 'B_SPLINE_SURFACE':BSplineSurface3D, 
 'BEZIER_SURFACE':BSplineSurface3D, 
 'OFFSET_SURFACE':None, 
 'SURFACE_REPLICA':None, 
 'RATIONAL_B_SPLINE_SURFACE':BSplineSurface3D, 
 'RECTANGULAR_TRIMMED_SURFACE':None, 
 'SURFACE_OF_LINEAR_EXTRUSION':None, 
 'SURFACE_OF_REVOLUTION':None, 
 'UNIFORM_SURFACE':BSplineSurface3D, 
 'QUASI_UNIFORM_SURFACE':BSplineSurface3D, 
 'RECTANGULAR_COMPOSITE_SURFACE':Face3D, 
 'CURVE_BOUNDED_SURFACE':Face3D, 
 'VERTEX_POINT':None, 
 'EDGE_CURVE':LineSegment3D, 
 'ORIENTED_EDGE':None, 
 'FACE_BOUND':None, 
 'FACE_OUTER_BOUND':None, 
 'EDGE_LOOP':Contour3D, 
 'POLY_LOOP':Contour3D, 
 'VERTEX_LOOP':Contour3D, 
 'ADVANCED_FACE':Face3D, 
 'FACE_SURFACE':Face3D, 
 'CLOSED_SHELL':Shell3D, 
 'OPEN_SHELL':Shell3D, 
 'CONNECTED_FACE_SET':Shell3D}