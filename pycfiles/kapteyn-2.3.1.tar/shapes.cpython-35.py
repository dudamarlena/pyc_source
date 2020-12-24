# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/jansky/data/users/breddels/src/kapteyn-sky2/kapteyn/shapes.py
# Compiled at: 2016-03-21 11:21:08
# Size of source mod 2**32: 84998 bytes
"""
.. highlight:: python
   :linenothreshold: 10

Module shapes
===============
This module defines a class for drawing shapes that define an area in your
image. The drawing is interactive using mouse- and keyboard buttons.
For each defined area the module :mod:`maputils` calculates the sum of the intensities,
the area and some other properties of the data. The shapes are one of
polygon, ellipse, circle, rectangle or spline.

The strength of this module is that it duplicates a shape to other selected
images using transformations to world coordinates. This enables one to compare
e.g. flux in two images with different WCS systems.
It works with spatial maps and maps with mixed axes (e.g. position-velocity maps)
and maps with linear axes.
The order of the two axes in a map can be swapped.
 
.. autoclass:: Shapecollection

Utility functions
-----------------

.. index:: Sample points on an ellipse
.. autofunction:: ellipsesamples
"""
from matplotlib import __version__ as mplversion
mploldversion = mplversion < '1.2.0'
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.pyplot import show, figure, get_current_fig_manager
from matplotlib.artist import Artist
from matplotlib.mlab import dist_point_to_segment
from matplotlib.widgets import Button, RadioButtons
from datetime import datetime
from kapteyn import tabarray
if mploldversion:
    import matplotlib.nxutils as nxutils
else:
    import matplotlib.path as path
from kapteyn.maputils import AxesCallback
from sys import stdout, exit
from kapteyn.mplutil import KeyPressFilter
from numpy import pi, array, dot, zeros, sin, cos, asarray, hypot, matrix, concatenate
from numpy import equal, nonzero, amin, arange
from numpy import min as Amin
from numpy import max as Amax
from numpy import nan as NAN
from math import cos as Cos
from math import sin as Sin
from math import atan2 as Atan2
from math import sqrt as Sqrt
from math import radians, degrees
try:
    from gipsy import finis, anyout
    gipsymod = True
except:
    gipsymod = False

__version__ = '1.1'
KeyPressFilter.allowed = [
 'f', 'g']

def button_setcolor(btnobj, c):
    """
   -----------------------------------------------------------
   Purpose:    Change color of button
   Parameters:
    btnobj     The button
    c          A color
   -----------------------------------------------------------
   """
    btnobj.color = c
    btnobj._lastcolor = c
    btnobj.ax.set_axis_bgcolor(c)
    if btnobj.drawon:
        btnobj.ax.figure.canvas.draw()


Button.setcolor = button_setcolor

def rotate(x, y, pa):
    x = array(x)
    y = array(y)
    pa_rad = pa * pi / 180.0
    sinP = sin(pa_rad)
    cosP = cos(pa_rad)
    xr = x * cosP - y * sinP
    yr = x * sinP + y * cosP
    return (xr, yr)


def ellipsesamples(xc, yc, major, minor, pa, n):
    """
   Get sample positions on ellipse
   Algorithm from 'Mathematical Elements for Computer Graphics' by
   Rogers and Adams, section about 'Parametric Representation of an Ellipse'
   Many methods which calculate sample positions on an ellipse
   suffer from a reasonable sampling near the positions where the
   curvature of an ellipse is large.
   The method we use, finds more sample points near the end points of an ellipse where the
   curvature is large while the increment between sample points along
   the sides of the ellipse where the curvature is not large, is small

   For an ellipse centered at (0,0), semimajor axis a and semiminor axis b
   the parametric representation is given by::

               x = a * cos(th)
               y = b * sin(th)

   'th' is the parameter and it represents the angle between 0 and 2*pi
   One can derive a recursive relation::

            x_i+1 =       x_i cos(dth) - (a/b) y_i sin(dth)
            y_i+1 = (b/a) x_i sin(dth) +       y_i cos(dth)

   dth is a step size in the angle th. It is equal to 2*pi/(n-1)
   n-1 is the required number or unique points on the ellipse and
   therefore an input parameter.
   The routine returns a result which is empty when either a or b is zero.

   The shift of the origin and the rotation of the ellipse can be
   combined into one matrix::

                  | cos(a)     sin (a)    0 | | 1  0  0 |
         T =      |-sin(a)     cos (a)    0 | | 0  1  0 |
                  |     0           0     1 | | xc yc 1 |

   Finally the result is computed with::

            X, Y, dummy = (x, y, 1).T

   The result is a polygon which describes the maximum inscribed area
   for the given ellipse parameters (Smith, L.B., "Drawing Ellipses, Hyperbolas,
   or Parabolas With a Fixed Number of Points and Maximum Inscribed Area,"
   Comp. J., Vol. 14, pp. 81-86, 1969

   :param xc:    Center position of ellipse in x direction
   :type xc:     float

   :param yc:    Center position of ellipse in y direction
   :type yc:     float

   :param major: Semi major axis in pixels
   :type major:  float

   :param minor: Semi minor axis in pixels
   :type minor:  float

   :param pa:    Position angle in degrees
   :type pa:     float

   :param n:     Number of sample points
   :type n:      int

   :Notes:
      The 'classical' method involves the calculation of many cosine
      and sine functions. This method avoids that by using a method
      which calculates a new sample based on the information of a
      previous sample. However, we didn't find a way to do this properly
      using NumPy. The classic method is very suitable to do implement
      in NumPy and is therefore faster than the algorithm here.
      But the sampling is better and we can do with less samples to
      get the same result.
   """
    a = abs(major)
    b = abs(minor)
    if a == 0 or b == 0.0:
        return list(zip([], []))
    dth = 2 * pi / n
    cosdth = Cos(dth)
    sindth = Sin(dth)
    pa = radians(pa)
    cospa = Cos(pa)
    sinpa = Sin(pa)
    R = array([[cospa, sinpa, 0.0], [-sinpa, cospa, 0.0], [0.0, 0.0, 1.0]])
    Tt = array([[1, 0, 0], [0, 1, 0], [xc, yc, 1]])
    T = dot(R, Tt)
    xy = zeros((n, 3))
    xy[:, 2] = 1.0
    m = array([[cosdth, -a * sindth / b, 0.0], [b * sindth / a, cosdth, 0.0], [0, 0, 1]])
    xy[0] = (
     a, 0.0, 1)
    for i in range(n - 1):
        xy[i + 1] = dot(m, xy[i])

    xy = dot(xy, T)
    return xy[:, :2]


def cubicspline(xyu, nsamples):
    """
   -----------------------------------------------------------
   Purpose:    Give a set positions (x,y) as control points, 
               calculate interpolated points which span cubic 
               polynomials between those control points.
   Parameters:
    xyu:       Unscaled sequence of positions (x,y) usually 
               representing a user defined polygon
    nsamples:  Number of spline interpolation points in each segment
               A segment is has two control points as start and end point.
   Returns:    Unscaled interpolated data including the control points.
               As a polygon the interpolated data is not closed so the last
               point is not equal to the first.
   Notes:      -Cubic splines, Mathematical elements for computer graphics, 
               2nd ed., Rogers & Adams
               -The algorithm calculates internal tangents but it needs
               two additional tangents for the first and last control points.
               Here we force smoothness by setting these to tangents to
               the same value. which is the tangent corresponding to the
               first segment.
               -Internally, the data is always scaled in the range [-1,1]
   Examples:   x = [0,1000,2000, 3000, 2500,  1200,  800]
               y = [0,1000,-1000, 0,   1000, 1800, 1700]
               xy = zip(x,y)
               nsamples = 100
               xy_spl = cubicspline(xy, samples)
   -----------------------------------------------------------
   """
    np = len(xyu)
    if np < 3:
        return
    xymin = Amin(xyu, 0)
    xymax = Amax(xyu, 0)
    scale = float(max(xymax[0] - xymin[0], xymax[1] - xymin[1]))
    if scale == 0.0:
        return
    xys = asarray(xyu) / scale
    x, y = list(zip(*xys))
    x = list(x)
    y = list(y)
    x.append(x[0])
    y.append(y[0])
    xy = list(zip(x, y))
    np += 1
    x1 = array(x[:-1])
    x2 = array(x[1:])
    y1 = array(y[:-1])
    y2 = array(y[1:])
    t = hypot(x2 - x1, y2 - y1)
    M = zeros((np, np))
    M[(0, 0)] = M[(-1, -1)] = 1.0
    R = zeros((np, 2))
    for row in range(1, np - 1):
        col = row - 1
        t_first = t[(row - 1)]
        t_next = t[row]
        M[(row, col)] = t_next
        M[(row, col + 1)] = 2.0 * (t_first + t_next)
        M[(row, col + 2)] = t_first
        x1 = xy[(row - 1)][0]
        x2 = xy[row][0]
        x3 = xy[(row + 1)][0]
        y1 = xy[(row - 1)][1]
        y2 = xy[row][1]
        y3 = xy[(row + 1)][1]
        R[(row, 0)] = 3.0 * (t_first / t_next * (x3 - x2) + t_next / t_first * (x2 - x1))
        R[(row, 1)] = 3.0 * (t_first / t_next * (y3 - y2) + t_next / t_first * (y2 - y1))

    P1 = (
     x[1] - x[0], y[1] - y[0])
    Plast = P1
    R[0] = P1
    R[-1] = Plast
    Ptan = matrix(M).I * R
    ta = array(list(range(nsamples))) / float(nsamples)
    ta2 = ta * ta
    ta3 = ta * ta2
    F = matrix(zeros((4, len(ta))))
    G = matrix(zeros((4, 2)))
    F[0] = 2.0 * ta3 - 3.0 * ta2 + 1.0
    F[1] = 1.0 - F[0]
    F2 = ta * (ta2 - 2.0 * ta + 1.0)
    F3 = ta * (ta2 - ta)
    for seg in range(np - 1):
        F[2] = F2 * t[seg]
        F[3] = F3 * t[seg]
        G[0] = xy[seg]
        G[1] = xy[(seg + 1)]
        G[2] = Ptan[seg]
        G[3] = Ptan[(seg + 1)]
        Pspline = F.T * G
        if seg == 0:
            v = Pspline.copy()
        else:
            v = concatenate((v, Pspline))

    if scale:
        v *= scale
    return v


class Poly(Polygon):

    def __init__(self, frame, framenr, active, markers, x0, y0, type=None, acolor='y', spline=False, **kwargs):
        canvas = frame.figure.canvas
        self.canvas = canvas
        self.active = active
        self.frame = frame
        self.framenr = framenr
        self.kwargs = kwargs
        self.shapecolor = acolor
        self.edgecolor = 'r'
        self.shapetype = type
        self.epsilon = 20
        Polygon.__init__(self, list(zip([x0], [y0])), closed=False, alpha=0.1, edgecolor='r', picker=5, animated=False, **self.kwargs)
        if not spline:
            self.frame.add_patch(self)
        self.markers = Line2D([x0], [y0], marker='o', markerfacecolor='r', color='r', animated=False)
        self.frame.add_line(self.markers)
        self.startmarker = Line2D([x0], [y0], marker='o', markerfacecolor='b', color='b', animated=False)
        self.frame.add_line(self.startmarker)
        self.closestindx = None
        self.x0 = x0
        self.y0 = y0
        self.area = None
        self.sum = None
        self.flux = None
        self.spline = None
        if spline:
            self.spline = Polygon(list(zip([x0], [y0])), closed=False, alpha=0.3, edgecolor='r')
            self.frame.add_patch(self.spline)
        if self.active:
            self.set_active(markers)
        else:
            self.set_inactive()

    def copy(self, frame, framenr, x0, y0, xy, active, markers):
        newobj = Poly(frame, framenr, active, markers, x0, y0, type=self.shapetype, **self.kwargs)
        newobj.updatexy(xy)
        return newobj

    def updatexy(self, xy, x0=None, y0=None):
        self.set_xy(xy)
        x, y = list(zip(*self.get_xy()))
        self.markers.set_data(x, y)
        self.startmarker.set_data(x[0], y[0])
        if x0 is not None:
            self.x0 = x0
        if y0 is not None:
            self.y0 = y0

    def shiftxy(self, x0, y0):
        x, y = list(zip(*self.xy))
        dx = x0 - self.x0
        dy = y0 - self.y0
        x = asarray(x) + dx
        y = asarray(y) + dy
        return list(zip(x, y))

    def set_active(self, markers=False):
        self.active = True
        alpha = 0.5
        if self.markers:
            self.markers.set_visible(markers)
            self.startmarker.set_visible(markers)
        if self.spline != None:
            self.spline.set_facecolor(self.shapecolor)
            self.spline.set_edgecolor(self.edgecolor)
            self.spline.set_alpha(alpha)
        else:
            self.set_facecolor(self.shapecolor)
            self.set_edgecolor(self.edgecolor)
            self.set_alpha(alpha)

    def addvertex(self, x, y, markers=True):
        xyl = list(self.get_xy())
        xyl.append([x, y])
        self.set_xy(xyl)
        self.markers.set_data(list(zip(*self.get_xy())))
        self.markers.set_visible(markers)

    def set_markers(self, vis=True):
        if self.markers != None:
            self.markers.set_visible(vis)
            self.startmarker.set_visible(vis)

    def set_inactive(self):
        self.active = False
        self.set_markers(False)
        alpha = 0.3
        if self.spline == None:
            self.set_facecolor('y')
            self.set_edgecolor(self.edgecolor)
            self.set_alpha(alpha)
        else:
            self.spline.set_facecolor('y')
            self.spline.set_alpha(alpha)
            self.spline.set_edgecolor(self.edgecolor)

    def indexclosestmarker(self, x, y):
        xt, yt = list(zip(*self.frame.transData.transform(self.xy)))
        xt = asarray(xt)
        yt = asarray(yt)
        d = (xt - x) * (xt - x) + (yt - y) * (yt - y)
        a2 = equal(d, amin(d))
        inds = nonzero(a2)[0]
        i = int(inds[0])
        if d[i] > self.epsilon:
            i = None
        self.closestindx = i
        return i

    def deletemarker(self, indx):
        xyl = list(self.xy)
        if len(xyl) == 2:
            return
        if indx == 0:
            del xyl[-1]
            del xyl[0]
            if len(xyl) > 0:
                xyl.append(xyl[0])
        else:
            del xyl[indx]
        self.xy = xyl
        self.markers.set_data(list(zip(*self.xy)))

    def indexsegmentinrange(self, x, y):
        if not self.spline:
            tra = self.get_transform()
        else:
            tra = self.spline.get_transform()
        xyt = tra.transform(self.xy)
        p = (x, y)
        ind = None
        dmin = None
        for i in range(len(xyt) - 1):
            s0 = xyt[i]
            s1 = xyt[(i + 1)]
            d = dist_point_to_segment(p, s0, s1)
            if dmin == None:
                dmin = d
                ind = i
            elif d < dmin:
                dmin = d
                ind = i

        return ind

    def insertmarker(self, x, y, indx):
        if indx == None:
            return
        i = indx + 1
        if i >= len(self.xy):
            return
        self.xy = array(list(self.xy[:i]) + [(x, y)] + list(self.xy[i:]))
        self.markers.set_data(list(zip(*self.xy)))

    def delete(self):
        self.frame.lines.remove(self.markers)
        if self.spline:
            self.frame.patches.remove(self.spline)
        else:
            self.frame.patches.remove(self)

    def inside(self, x, y):
        pos = [
         (
          x, y)]
        if mploldversion:
            mask = nxutils.points_inside_poly(pos, self.xy)
        else:
            polypath = path.Path(self.xy)
            mask = polypath.contains_points(pos)
        return mask[0]

    def moveall(self, dx, dy):
        x, y = list(zip(*self.xy))
        x = asarray(x) + dx
        y = asarray(y) + dy
        self.markers.set_data(x, y)
        self.startmarker.set_data(x[0], y[0])
        self.xy = list(zip(x, y))
        self.x0 += dx
        self.y0 += dy
        return self.xy

    def movemarker(self, x, y, indx):
        self.xy[indx] = (
         x, y)
        self.markers.set_data(list(zip(*self.xy)))
        if indx == 0:
            self.startmarker.set_data(x, y)

    def allinsideframe(self):
        x1, x2 = self.frame.get_xlim()
        y1, y2 = self.frame.get_ylim()
        if self.spline:
            xy = self.spline.xy
        else:
            xy = self.xy
        inside = True
        for x, y in xy:
            if x > x2 or x < x1 or y > y2 or y < y1:
                inside = False
                break

        return inside


class Ellipse(Poly):

    def __init__(self, frame, framenr, active, markers, x0, y0, type=None, r1=0.0, r2=0.0, r3=0.0, **kwargs):
        startang, endang, delta = (0.0, 360.0, 1.0)
        self.phi = arange(startang, endang + delta, delta) * pi / 180.0
        self.pa = r3
        self.x0 = x0
        self.y0 = y0
        self.maj = r1
        self.min = r2
        Poly.__init__(self, frame, framenr, active, markers, x0, y0, type=type, acolor='m', **kwargs)
        self.updatexy(self.getvertices())

    def getvertices(self):
        n = 200
        vertices = ellipsesamples(self.x0, self.y0, self.maj, self.min, self.pa, n)
        return vertices

    def movemarker(self, x, y, indx):
        n = len(self.xy)
        d = n / 8
        minor = d <= indx < 3 * d or 5 * d <= indx < 7 * d
        majorpa = indx >= 7 * d or 0 <= indx < d
        major = 3 * d <= indx < 5 * d
        if majorpa:
            self.pa = degrees(Atan2(y - self.y0, x - self.x0))
        axis = Sqrt((self.x0 - x) ** 2 + (self.y0 - y) ** 2)
        if minor:
            self.min = axis
        if major or majorpa:
            self.maj = axis
        self.xy = self.getvertices()
        xn, yn = list(zip(*self.xy))
        self.markers.set_data(xn, yn)
        self.startmarker.set_data(xn[0], yn[0])

    def copy(self, frame, framenr, x0, y0, xy, active, markers):
        newobj = Ellipse(frame, framenr, active, markers, x0, y0, type=self.shapetype, r1=self.maj, r2=self.min, r3=self.pa, **self.kwargs)
        newobj.updatexy(xy)
        return newobj

    def updatexy(self, xy, x0=None, y0=None):
        self.xy = xy
        self.markers.set_data(list(zip(*self.xy)))
        if x0 is not None:
            self.x0 = x0
        if y0 is not None:
            self.y0 = y0
        x, y = list(zip(*self.xy))
        n90 = len(xy) / 4
        self.maj = Sqrt((x[0] - self.x0) ** 2 + (y[0] - self.y0) ** 2)
        self.min = Sqrt((x[n90] - self.x0) ** 2 + (y[n90] - self.y0) ** 2)
        self.pa = degrees(Atan2(y[0] - self.y0, x[0] - self.x0))
        self.startmarker.set_data(x[0], y[0])


class Circle(Poly):

    def __init__(self, frame, framenr, active, markers, x0, y0, type=None, r1=0.0, r2=0.0, **kwargs):
        startang, endang, delta = (0.0, 360.0, 1.0)
        self.phi = arange(startang, endang + delta, delta) * pi / 180.0
        self.x0 = x0
        self.y0 = y0
        self.radius = r1
        Poly.__init__(self, frame, framenr, active, markers, x0, y0, type=type, acolor='g', **kwargs)
        self.updatexy(self.getvertices())

    def getvertices(self):
        vertices = list(zip(self.radius * cos(self.phi) + self.x0, self.radius * sin(self.phi) + self.y0))
        return vertices

    def movemarker(self, x, y, indx):
        self.radius = Sqrt((self.x0 - x) ** 2 + (self.y0 - y) ** 2)
        self.xy = self.getvertices()
        xn, yn = list(zip(*self.xy))
        self.markers.set_data(xn, yn)
        self.startmarker.set_data(xn[0], yn[0])

    def copy(self, frame, framenr, x0, y0, xy, active, markers):
        newobj = Circle(frame, framenr, active, markers, x0, y0, type=self.shapetype, r1=self.radius, **self.kwargs)
        newobj.updatexy(xy)
        return newobj

    def updatexy(self, xy, x0=None, y0=None):
        if x0 is not None:
            self.x0 = x0
        if y0 is not None:
            self.y0 = y0
        self.xy = xy
        self.markers.set_data(list(zip(*self.xy)))
        xr, yr = xy[0]
        self.radius = Sqrt((self.x0 - xr) ** 2 + (self.y0 - yr) ** 2)
        self.startmarker.set_data(xr, yr)


class Rectangle(Poly):

    def __init__(self, frame, framenr, active, markers, x0, y0, type=None, r1=0.0, r2=0.0, **kwargs):
        self.x0 = x0
        self.y0 = y0
        self.width = r1
        self.height = r2
        self.pa = 0.0
        Poly.__init__(self, frame, framenr, active, markers, x0, y0, type=type, acolor='r', **kwargs)
        self.updatexy(self.getvertices())

    def getvertices(self):
        x = [
         0.0, 0.0, 0.0, 0.0]
        y = [0.0, 0.0, 0.0, 0.0]
        x[0] = self.x0 - 0.5 * self.width
        y[0] = self.y0 - 0.5 * self.height
        x[1] = x[0] + self.width
        y[1] = y[0]
        x[2] = x[1]
        y[2] = y[1] + self.height
        x[3] = x[0]
        y[3] = y[2]
        vertices = list(zip(x, y))
        return vertices

    def movemarker(self, xnew, ynew, indx):
        x, y = list(zip(*self.xy))
        dx = xnew - x[indx]
        dy = ynew - y[indx]
        x = [a - self.x0 for a in x]
        y = [a - self.y0 for a in y]
        xr, yr = rotate(x, y, -self.pa)
        xrnew, yrnew = rotate(xnew - self.x0, ynew - self.y0, -self.pa)
        if indx != 0:
            dxr = xrnew - xr[indx]
            dyr = yrnew - yr[indx]
            if indx > 2:
                dxr = -dxr
            if indx < 2:
                dyr = -dyr
            xr[0] -= dxr
            yr[0] -= dyr
            xr[1] += dxr
            yr[1] -= dyr
            xr[2] += dxr
            yr[2] += dyr
            xr[3] -= dxr
            yr[3] += dyr
            self.width = abs(x[1] - x[0])
            self.height = abs(y[2] - y[0])
        else:
            pa1 = Atan2(yr[0], xr[0])
            pa2 = Atan2(yrnew, xrnew)
            self.pa += degrees(pa2 - pa1)
        x, y = rotate(xr, yr, self.pa)
        x = [a + self.x0 for a in x]
        y = [a + self.y0 for a in y]
        self.xy = list(zip(x, y))
        self.markers.set_data(x, y)
        self.startmarker.set_data(x[0], y[0])

    def copy(self, frame, framenr, x0, y0, xy, active, markers):
        newobj = Rectangle(frame, framenr, active, markers, self.x0, self.y0, type=self.shapetype, r1=self.width, r2=self.height, **self.kwargs)
        newobj.updatexy(xy)
        return newobj

    def updatexy(self, xy, x0=None, y0=None):
        self.xy = xy
        x, y = list(zip(*self.xy))
        self.markers.set_data(x, y)
        if x0 is not None:
            self.x0 = x0
        if y0 is not None:
            self.y0 = y0
        xpa = (x[1] + x[2]) / 2.0
        ypa = (y[1] + y[2]) / 2.0
        self.pa = degrees(Atan2(ypa - self.y0, xpa - self.x0))
        self.width = Sqrt((x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2)
        self.height = Sqrt((x[1] - x[2]) ** 2 + (y[2] - y[2]) ** 2)
        self.startmarker.set_data(x[0], y[0])


class Spline(Poly):

    def __init__(self, frame, framenr, active, markers, x0, y0, type=None, r1=0.0, r2=0.0, **kwargs):
        Poly.__init__(self, frame, framenr, active, markers, x0, y0, type=type, acolor='r', spline=True, **kwargs)

    def copy(self, frame, framenr, x0, y0, xy, active, markers):
        newobj = Spline(frame, framenr, active, markers, x0, y0, type=self.shapetype, **self.kwargs)
        newobj.updatexy(xy)
        return newobj


class Shapecollection(object):
    __doc__ = "\n   Administration class for a collection of shapes.\n   The figure \n\n   :param images:  In each image a shape can be drawn using mouse-\n                   and keyboard buttons. This shape is duplicated\n                   either in pixel coordinates or world coordinates in\n                   the other images of the list with images.\n                   These images have two attributes that are relevant for\n                   this module. These are *fluxfie* to define how the\n                   flux should be calculated using fixed variables\n                   *s* for the sum of the intensities of the pixels\n                   in an area and *a* which represents the area.\n   :type images:   A list of objects from class :class:`maputils.Annotatedimage`\n\n   :param ifigure: The Matplotlib figure where the images are.\n   :type ifigure:  Matplotlib :class:`Figure` object\n   \n   :param wcs:     The default is *True* which implies that in case of\n                   multiple images shapes propagate through world\n                   coordinates. If you have images with the same\n                   size and WCS, then set *wcs=False* to\n                   duplicate shapes in pixel coordinates which is\n                   much faster.\n   :type wcs:      Boolean\n   \n   :param inputfilename:\n                   Name of file on disk which stores shape information.\n                   The objects are read from this file and plotted on\n                   all the images in the image list. The coordinates\n                   in the file can be either pixel- or world coordinates.\n                   You should specify that with parameter *inputwcs*\n   :type inputfilename:\n                   String\n\n   :param inputwcs: \n                   Set the shape mode for shapes from file to\n                   either pixels coordinates (*inputwcs=False*)\n                   or to world coordinates (*inputwcs=True*).\n   :type inputwcs: Boolean\n\n\n   This shape interactor reacts to the following keyboard and mouse buttons::\n\n      mouse - left  :  Drag a polygon point to a new position or\n                       change the radius of a circle or\n                       change the minor axis of an ellipse or\n                       change the major axis and position angle of an ellipse\n      mouse - middle:  Select an existing object in any frame\n      key   - a     :  Add a point to a polygon or spline\n      key   - c     :  Copy current object at mouse cursor\n      key   - d     :  Delete a point in a polygon or spline\n      key   - e     :  Erase active object and associated objects in other images\n      key   - i     :  Insert a point in a polygon or spline\n      key   - n     :  Start with a new object\n      key   - u     :  Toggle markers. Usually for a hardcopy\n                       one does not want to show the markers of a shape.\n      key   - w     :  Write object data in current image to file on disk\n      key   - r     :  Read objects from file for current image\n      key   - [     :  Next active object in current shape selection\n      key   - ]     :  Previous active object in current shape selection\n      \n      Interactive navigation defined by canvas\n      Amongst others:\n      key   - f     :  Toggle fullscreen\n      key   - g     :  Toggle grid\n\n\n      Gui buttons:\n      'Quit'         :  Abort program\n      'plot result'  :  Plot calculated flux as function of shape and image\n      'Save result'  :  Save flux information to disk\n                        The file names are generated and contain date\n                        and time stamp (e.g flux_24042010_212029.dat)\n      'Pol.'         :  Select shape polygon. Start with key 'n' for\n                        new polygon. Add new points with key 'a'.\n      'Ell.'         :  Select shape ellipse. Start with key 'n' for\n                        new ellipse. With left mouse button Drag major axis to change\n                        size and rotation or, using a point near the\n                        center, drag entire ellipse to a new position.\n      'Cir.:'        :  Select shape circle. Start with key 'n' for\n                        new circle. The radius can be changed by dragging\n                        an arbitrary point on the border to a new position.\n      'Rec.'         :  Select shape rectangle. Start with key 'n' for\n                        new rectangle. Drag any of the four edges to resize\n                        the rectangle.\n      'Spl.'         :  Like the polygon but the points between two knots\n                        follow a spline curve.\n\n   :Notes:\n\n      All shapes are derived from a polygon class. There is one method\n      that generates coordinates for all shapes and :meth:`maputils.getflux`\n      uses the same routine to calculate whether a pixel in an enclosing\n      box is within or outside the shape. For circles and ellipses the\n      number of polygon points is 360 and this slows down the calculation\n      significantly. Methods which assume a perfect circle or ellipse can\n      handle the inside/outside problem much faster, but note that due to different\n      WCS's, ellipses and circles don't keep their shape in other images.\n      So in fact only a polygon is the common shape. A spline is a polygon\n      with an artificially increased number of points.\n\n   :Example:\n   \n     ::\n\n      fig = plt.figure(figsize=(12,10))\n      frame1 = fig.add_axes([0.07,0.1,0.35, 0.8])\n      frame2 = fig.add_axes([0.5,0.1,0.43, 0.8])\n      im1 = f1.Annotatedimage(frame1)\n      im2 = f2.Annotatedimage(frame2)\n      im1.Image(); im1.Graticule()\n      im2.Image(); im2.Graticule()\n      im1.interact_imagecolors(); im1.interact_toolbarinfo()\n      im2.interact_imagecolors(); im2.interact_toolbarinfo()\n      im1.plot(); im2.plot()\n      im1.fluxfie = lambda s, a: s/a\n      im2.fluxfie = lambda s, a: s/a\n      im1.pixelstep = 0.5; im2.pixelstep = 0.5\n      images = [im1, im2]\n      shapes = shapes.Shapecollection(images, fig, wcs=True, inputwcs=True)\n\n   "

    def __init__(self, images, ifigure, wcs=True, inputfilename=None, inputwcs=False, gipsy=False):
        self.frames = []
        self.images = images
        self.numberofimages = len(images)
        self.inputfilename = inputfilename
        self.inputwcs = inputwcs
        self.gipsy = gipsy
        self.wcs = wcs
        self.activeobject = None
        self.showactivestate = True
        self.currenttype = 0
        self.canvas = ifigure.canvas
        self.numberoftypes = 5
        self.shapetypes = self.polygon, self.ellipse, self.circle, self.rectangle, self.spline = list(range(self.numberoftypes))
        self.maxindx = [
         -1] * self.numberoftypes
        self.currentobj = [
         -1] * self.numberoftypes
        self.shapes = [[]] * self.numberoftypes
        self.currentimage = None
        self.canvas.mpl_connect('key_press_event', self.key_pressed_global)
        self.cidmove = ifigure.canvas.mpl_connect('motion_notify_event', self.motion_notify)
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.button_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.button_release)
        self.toolbar = get_current_fig_manager().toolbar
        for im in self.images:
            self.frames.append(im.frame)

        self.figure = ifigure
        self.shapedict = {'pol': self.polygon, 'ell': self.ellipse, 'cir': self.circle, 'rec': self.rectangle, 'spl': self.spline}
        self.figresult = figure(figsize=(6, 5))
        self.frameresult = self.figresult.add_subplot(1, 1, 1)
        self.frameresult.set_title('Flux as function of shape and image', y=1.05)
        self.results = False
        self.xstart = 0.0
        self.ystart = 0.0
        ypos = 0.96
        yhei = 0.03
        self.graycol = 'chartreuse'
        quit_button = self.figure.add_axes([0.01, ypos, 0.11, yhei])
        b0 = Button(quit_button, 'Quit')
        b0.on_clicked(self.doquit)
        result_button = self.figure.add_axes([0.13, ypos, 0.11, yhei])
        b1 = Button(result_button, 'Plot Flux')
        b1.on_clicked(self.plotresults)
        save_button = self.figure.add_axes([0.25, ypos, 0.11, yhei])
        b2 = Button(save_button, 'Save Flux')
        b2.on_clicked(self.saveresults)
        pol_button = self.figure.add_axes([0.74, ypos, 0.05, yhei])
        b3 = Button(pol_button, 'Pol.')
        b3.on_clicked(self.setpoly)
        ell_button = self.figure.add_axes([0.79, ypos, 0.05, yhei])
        b4 = Button(ell_button, 'Ell.')
        b4.on_clicked(self.setellipse)
        cir_button = self.figure.add_axes([0.84, ypos, 0.05, yhei])
        b5 = Button(cir_button, 'Cir.')
        b5.on_clicked(self.setcircle)
        rec_button = self.figure.add_axes([0.89, ypos, 0.05, yhei])
        b6 = Button(rec_button, 'Rec.')
        b6.on_clicked(self.setrectangle)
        spl_button = self.figure.add_axes([0.94, ypos, 0.05, yhei])
        b7 = Button(spl_button, 'Spl.')
        b7.on_clicked(self.setspline)
        self.buttons = [
         b0, b1, b2, b3, b4, b5, b6, b7]
        for i, b in enumerate(self.buttons):
            if i > 3:
                b.setcolor(self.graycol)
            if i == 3:
                b.setcolor('r')
            b.label.set_fontsize(10)

        tdict = dict(color='g', fontsize=10, va='bottom', ha='left')
        helptxt = 'SHAPES:\n'
        helptxt += 'n=start new object -- a=add point -- d=delete point -- i=insert point\n'
        helptxt += 'c=copy object -- e=erase object -- [=next shape in group -- ]=prev in gr.\n'
        helptxt += 'w=write shapes to disk -- r=read shapes from disk -- u=toggle markers\n'
        helptxt += 'Mouse-left=drag and/or change shape --- Mouse-middle=select shape'
        ifigure.text(0.01, 0.01, helptxt, tdict)
        helptxt = 'COLOURS:\n'
        helptxt += self.images[0].get_colornavigation_info()
        ifigure.text(0.5, 0.01, helptxt, tdict)

    def setpoly(self, event):
        for i in range(3, len(self.buttons)):
            self.buttons[i].setcolor(self.graycol)

        self.buttons[3].setcolor('r')
        self.setshape('pol')

    def setellipse(self, event):
        for i in range(3, len(self.buttons)):
            self.buttons[i].setcolor(self.graycol)

        self.buttons[4].setcolor('r')
        self.setshape('ell')

    def setcircle(self, event):
        for i in range(3, len(self.buttons)):
            self.buttons[i].setcolor(self.graycol)

        self.buttons[5].setcolor('r')
        self.setshape('cir')

    def setrectangle(self, event):
        for i in range(3, len(self.buttons)):
            self.buttons[i].setcolor(self.graycol)

        self.buttons[6].setcolor('r')
        self.setshape('rec')

    def setspline(self, event):
        for i in range(3, len(self.buttons)):
            self.buttons[i].setcolor(self.graycol)

        self.buttons[7].setcolor('r')
        self.setshape('spl')

    def setshape(self, label):
        """
      This is the callback function for the radio button with
      the selection of shapes.
      """
        newtype = self.shapedict[label]
        if newtype < 0 or newtype >= len(self.shapetypes):
            return
        oldtype = self.currenttype
        if oldtype == newtype:
            return
        oldindx = self.currentobj[oldtype]
        newindx = self.currentobj[newtype]
        self.currenttype = newtype
        if self.maxindx[oldtype] >= 0:
            for obj in self.shapes[oldtype][oldindx]:
                if obj.active:
                    obj.set_inactive()

        if self.activeobject is not None:
            frame = self.activeobject.frame
        else:
            frame = None
        if self.maxindx[newtype] >= 0:
            for obj in self.shapes[newtype][newindx]:
                if obj.frame is frame:
                    self.activeobject = obj
                    obj.set_active(markers=True)
                else:
                    obj.set_active()

        self.canvas.draw()

    def getimage(self, event):
        image = None
        for ima in self.images:
            if ima.frame.contains(event)[0]:
                image = ima
                break

        return image

    def getframenr(self, event):
        nr = None
        for i, fr in enumerate(self.frames):
            if fr.contains(event)[0]:
                nr = i
                break

        return nr

    def updatesplines(self):
        if self.activeobject is None:
            return
        xy = cubicspline(self.activeobject.xy, 10)
        if xy != None and self.activeobject.spline != None:
            self.activeobject.spline.xy = xy
            cindx = self.currentobj[self.currenttype]
            for obj in self.shapes[self.currenttype][cindx]:
                if obj is not self.activeobject:
                    if self.wcs:
                        im1 = self.currentimage
                        im2 = self.images[obj.framenr]
                        obj.spline.xy = self.transformXY(self.activeobject.spline.xy, im1, im2)
                    else:
                        obj.spline.xy = self.activeobject.spline.xy

    def transformXY(self, xy1, im1, im2):
        """
      Given one or a sequence of positions in pixels *xy* that belong
      to an image with world coordinate system *proj1*, we want
      the pixel values in another world coordinate system given by
      *proj2*. This second projection can differ in output sky system.
      We follow the next procedure to transform:

      * 1: If the sky systems are equal then we can transform
        the pixel coordinates without a sky transformation.
      * 2: If the sky systems differ, transform the pixel position
        in world coordinates in the first system with the
        sky system of the second system.
      * 3: Transform the world coordinates into pixels in the
        second system. These world coordinates are now given
        in the sky system of the second world coordinate system.

      Some remarks about compatible image axes. Markers from image im1
      are copied to identical (i.e. in world coordinates) positions
      in im2. So the restriction is that the axes of both images
      allow world coordinate transformations. The axes can differ
      in sky system and/or spectral translation. Also the order of compatible
      axes can be swapped.
      So copying markers are possible in the following situations:
      
      (RA, DEC) -> (RA, DEC), (DEC, RA), (GLON, GLAT), (GLAT, GLON) etc.
      (RA, VOPT) -> (RA, VOPT), (VOPT, RA), (FREQ, RA), (RA, WAVE) etc.
                    (and as function of a pixel coordinate for DEC)

      If X, Y are linear types then:
      
      (DEC, X) -> (DEC, X), (X, DEC)
                  (and as function of a pixel coordinate for RA)
      (X, VOPT) -> (X, VOPT), (VOPT, X), (FREQ, X), (X, WAVE) etc.
      (X, Y) -> (X, Y), (Y, X)

      To verify these options we use the axis permutation array 'axperm'
      of the image object and the lonaxnum, lataxnum and specaxnum
      attributes of the projection object to inquire whether their
      axes have non linear transformations.
      """
        ax1x = im1.wcstypes[0]
        ax1y = im1.wcstypes[1]
        ax2x = im2.wcstypes[0]
        ax2y = im2.wcstypes[1]
        possible = ax2x in [ax1x, ax1y] and ax2y in [ax1x, ax1y]
        if possible:
            mixed = False
            if ax1x in ('lo', 'la') and ax1y not in ('lo', 'la'):
                mixed = True
            if ax1y in ('lo', 'la') and ax1x not in ('lo', 'la'):
                mixed = True
            if mixed:
                mixpix1 = im1.mixpix
                mixpix2 = im2.mixpix
                if mixpix1 is None or mixpix2 is None:
                    possible = False
                if not possible:
                    if isinstance(xy1, tuple) and len(xy1) == 2:
                        xy2 = (0, 0)
                    else:
                        xx = [
                         0.0] * len(xy1)
                        yy = [
                         0.0] * len(xy1)
                        xy2 = list(zip(xx, yy))
                    return xy2
                swap = ax1x != ax2x
                spectral = 'sp' in [ax1x, ax1y]
                proj1 = im1.projection
                proj2 = im2.projection
                if isinstance(xy1, tuple) and len(xy1) == 2:
                    twoelements = True
                    xy1 = list(zip([xy1[0]], [xy1[1]]))
                else:
                    twoelements = False
                if proj1.skyout != proj2.skyout:
                    proj1.skyout = proj2.skyout
                if not mixed:
                    xyworld1 = proj1.toworld(xy1)
                    if swap:
                        xw, yw = list(zip(*xyworld1))
                        xyworld1 = list(zip(yw, xw))
                    xy2 = proj2.topixel(xyworld1)
        else:
            if spectral and proj1.altspecarg != proj2.altspecarg:
                proj1s = proj1.spectra(proj2.altspecarg)
            else:
                proj1s = proj1
            z = zeros(len(xy1)) + mixpix1
            x, y = list(zip(*xy1))
            t = list(zip(x, y, z))
            xyworld1 = proj1s.toworld(t)
            n = len(xy1)
            unknown = zeros(n) + NAN
            zp = zeros(n) + mixpix2
            xw, yw, zw = list(zip(*xyworld1))
            if swap:
                world = (
                 yw, xw, unknown)
            else:
                world = (
                 xw, yw, unknown)
            pixel = (
             unknown, unknown, zp)
            world, pixel = proj2.mixed(world, pixel)
            xy2 = list(zip(pixel[0], pixel[1]))
        proj1.skyout = None
        if twoelements:
            xy2 = (
             xy2[0][0], xy2[0][1])
        return xy2

    def addnewobject(self, shapetype, x, y, framenr):
        oldgroup = self.maxindx[self.currenttype]
        if oldgroup >= 0:
            for obj in self.shapes[self.currenttype][oldgroup]:
                if obj.active:
                    obj.set_inactive()

        self.currenttype = shapetype
        self.maxindx[self.currenttype] += 1
        if self.activeobject is not None:
            self.activeobject.set_markers(False)
        objlist = []
        obj = None
        currentframe = self.frames[framenr]
        x1, x2 = currentframe.get_xlim()
        y1, y2 = currentframe.get_ylim()
        maj = abs(x2 - x1) / 5.0
        min = abs(y2 - y1) / 8.0
        baseobj = None
        active = markers = True
        xpb = ypb = 0.0
        if self.currenttype == self.ellipse:
            baseobj = Ellipse(currentframe, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=maj, r2=min)
        else:
            if self.currenttype == self.polygon:
                baseobj = Poly(currentframe, framenr, active, markers, xpb, ypb, type=self.currenttype)
            else:
                if self.currenttype == self.circle:
                    baseobj = Circle(currentframe, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=min)
                else:
                    if self.currenttype == self.rectangle:
                        baseobj = Rectangle(currentframe, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=maj, r2=min)
                    elif self.currenttype == self.spline:
                        baseobj = Spline(currentframe, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=maj, r2=min)
        baseobj.updatexy(list(zip(x, y)))
        if self.wcs:
            xyworld = self.images[framenr].toworld(baseobj.xy[:, 0], baseobj.xy[:, 1])
        im1 = self.images[framenr]
        for i in range(self.numberofimages):
            active = True
            markers = False
            if i != baseobj.framenr:
                if self.wcs:
                    im2 = self.images[i]
                    xy = self.transformXY(baseobj.xy, im1, im2)
                else:
                    xy = baseobj.xy
                obj = baseobj.copy(self.frames[i], i, xpb, ypb, xy, active, markers)
            else:
                obj = baseobj
                obj.set_active()
            objlist.append(obj)

        if len(objlist) > 0:
            numlists = len(self.shapes[self.currenttype])
            if numlists == 0:
                self.shapes[self.currenttype] = [
                 objlist]
            else:
                self.shapes[self.currenttype].append(objlist)
            self.currentobj[self.currenttype] = numlists
        self.activeobject = baseobj
        self.activeobject.set_markers(True)
        if self.currenttype == self.spline:
            self.updatesplines()
        self.canvas.draw()

    def key_pressed_global(self, event):
        """This is the event handler for all types of supported shapes for which we want
         statistics"""
        if not event.inaxes:
            return
        if self.toolbar.mode != '':
            return
        if event.key is None:
            return
        self.currentimage = self.getimage(event)
        if self.currentimage == None:
            return
        xpb = event.xdata
        ypb = event.ydata
        if self.wcs:
            xw, yw = self.currentimage.toworld(xpb, ypb)
        keypressed = event.key.lower()
        if keypressed in ('n', 'c'):
            if keypressed == 'c':
                if not self.activeobject:
                    return
                if not self.activeobject.frame.contains(event)[0]:
                    return
                if self.activeobject.shapetype != self.currenttype:
                    pass
                return
            oldgroup = self.maxindx[self.currenttype]
            if oldgroup >= 0:
                for obj in self.shapes[self.currenttype][oldgroup]:
                    if obj.active:
                        obj.set_inactive()

            self.maxindx[self.currenttype] += 1
            if self.activeobject:
                self.activeobject.set_markers(False)
            objlist = []
            obj = None
            x1, x2 = event.inaxes.get_xlim()
            y1, y2 = event.inaxes.get_ylim()
            maj = abs(x2 - x1) / 5.0
            min = abs(y2 - y1) / 8.0
            framenr = self.getframenr(event)
            baseobj = None
            if keypressed == 'n':
                active = markers = True
                if self.currenttype == self.ellipse:
                    baseobj = Ellipse(event.inaxes, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=maj, r2=min)
                else:
                    if self.currenttype == self.polygon:
                        baseobj = Poly(event.inaxes, framenr, active, markers, xpb, ypb, type=self.currenttype)
                    else:
                        if self.currenttype == self.circle:
                            baseobj = Circle(event.inaxes, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=min)
                        else:
                            if self.currenttype == self.rectangle:
                                baseobj = Rectangle(event.inaxes, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=maj, r2=min)
                            elif self.currenttype == self.spline:
                                baseobj = Spline(event.inaxes, framenr, active, markers, xpb, ypb, type=self.currenttype, r1=maj, r2=min)
                    xyshift = baseobj.xy
                    if self.wcs:
                        xyworld = self.getimage(event).toworld(xyshift[:, 0], xyshift[:, 1])
                    if keypressed == 'c':
                        active = markers = True
                        xyshift = self.activeobject.shiftxy(xpb, ypb)
                        baseobj = self.activeobject.copy(event.inaxes, framenr, xpb, ypb, xyshift, active, markers)
                    for i in range(self.numberofimages):
                        active = True
                        markers = False
                        if not self.frames[i].contains(event)[0]:
                            active = False
                            if self.wcs:
                                im1 = self.images[framenr]
                                im2 = self.images[i]
                                xy = self.transformXY(xyshift, im1, im2)
                                x0, y0 = self.transformXY((xpb, ypb), im1, im2)
                            else:
                                xy = xyshift
                                x0, y0 = xpb, ypb
                            obj = baseobj.copy(self.frames[i], i, x0, y0, xy, active, markers)
                        else:
                            obj = baseobj
                            obj.set_active()
                        objlist.append(obj)

                    if len(objlist) > 0:
                        numlists = len(self.shapes[self.currenttype])
                        if numlists == 0:
                            self.shapes[self.currenttype] = [
                             objlist]
                        else:
                            self.shapes[self.currenttype].append(objlist)
                        self.currentobj[self.currenttype] = numlists
                    self.activeobject = baseobj
                    self.activeobject.set_markers(True)
                    if keypressed == 'c' and self.currenttype == self.spline:
                        self.updatesplines()
                self.canvas.draw()
        if keypressed in ('[', ']'):
            newgroup = oldgroup = self.currentobj[self.currenttype]
            if oldgroup == -1:
                return
            if keypressed == '[':
                newgroup += 1
                if newgroup > self.maxindx[self.currenttype]:
                    newgroup = 0
            else:
                newgroup -= 1
                if newgroup < 0:
                    newgroup = self.maxindx[self.currenttype]
                if newgroup == oldgroup:
                    return
                if self.activeobject:
                    self.activeobject.set_markers(False)
            for obj in self.shapes[self.currenttype][oldgroup]:
                if obj.active:
                    obj.set_inactive()

            for obj in self.shapes[self.currenttype][newgroup]:
                obj.set_active()
                if obj.frame.contains(event)[0]:
                    self.activeobject = obj
                    self.activeobject.set_markers(True)

            self.currentobj[self.currenttype] = newgroup
            self.canvas.draw()
        else:
            if keypressed == 'a':
                if self.activeobject:
                    if not self.activeobject.frame.contains(event)[0]:
                        return
                cindx = self.currentobj[self.currenttype]
                if cindx >= 0 and self.currenttype in (self.polygon, self.spline):
                    framenr = self.getframenr(event)
                    self.activeobject.addvertex(xpb, ypb, True)
                    for obj in self.shapes[self.currenttype][cindx]:
                        if obj is not self.activeobject:
                            setmarker = False
                            if self.wcs:
                                im1 = self.images[framenr]
                                im2 = self.images[obj.framenr]
                                xp, yp = self.transformXY((xpb, ypb), im1, im2)
                            else:
                                xp, yp = xpb, ypb
                            obj.addvertex(xp, yp, setmarker)

                    if self.currenttype == self.spline:
                        self.updatesplines()
                    self.canvas.draw()
            else:
                if keypressed == 'd':
                    if self.activeobject is None:
                        return
                    indx = self.activeobject.indexclosestmarker(event.x, event.y)
                    if indx == None:
                        return
                    cindx = self.currentobj[self.currenttype]
                    if cindx >= 0 and self.currenttype in [self.polygon, self.spline]:
                        for obj in self.shapes[self.currenttype][cindx]:
                            obj.deletemarker(indx)

                        if self.currenttype == self.spline:
                            self.updatesplines()
                        self.canvas.draw()
                else:
                    if keypressed == 'i':
                        if self.activeobject is None:
                            return
                        indx = self.activeobject.indexsegmentinrange(event.x, event.y)
                        cindx = self.currentobj[self.currenttype]
                        if cindx >= 0 and self.currenttype in [self.polygon, self.spline]:
                            framenr = self.getframenr(event)
                            for obj in self.shapes[self.currenttype][cindx]:
                                if obj == self.activeobject:
                                    xp, yp = xpb, ypb
                                else:
                                    im1 = self.images[framenr]
                                    im2 = self.images[obj.framenr]
                                    xp, yp = self.transformXY((xpb, ypb), im1, im2)
                                obj.insertmarker(xp, yp, indx)

                            if self.currenttype == self.spline:
                                self.updatesplines()
                            self.canvas.draw()
                    else:
                        if keypressed == 'e':
                            oldgroup = self.currentobj[self.currenttype]
                            if oldgroup < 0:
                                return
                            for obj in self.shapes[self.currenttype][oldgroup]:
                                obj.delete()

                            del self.shapes[self.currenttype][oldgroup]
                            self.maxindx[self.currenttype] -= 1
                            if self.maxindx[self.currenttype] < 0:
                                self.currentobj[self.currenttype] = -1
                                newgroup = None
                                for sh in self.shapetypes:
                                    if sh != self.currenttype and self.currentobj[sh] != -1:
                                        self.currenttype = sh
                                        newgroup = self.currentobj[sh]
                                        break

                                if newgroup == None:
                                    self.activeobject = None
                                    self.canvas.draw()
                            else:
                                newgroup = oldgroup - 1
                            if newgroup < 0:
                                newgroup = self.maxindx[self.currenttype]
                            self.currentobj[self.currenttype] = newgroup
                            if newgroup >= 0:
                                for obj in self.shapes[self.currenttype][newgroup]:
                                    obj.set_active()
                                    if obj.frame.contains(event)[0]:
                                        self.activeobject = obj
                                        self.activeobject.set_markers(True)

                            self.canvas.draw()
                        else:
                            if keypressed == 'w':
                                stamp = datetime.now().strftime('%d%m%Y_%H%M%S')
                                filename = 'shapes_' + stamp + '.dat'
                                f = open(filename, 'w')
                                stamp = datetime.now().strftime('! Saved at %A %d/%m/%Y %H:%M:%S\n')
                                f.write(stamp)
                                iminfo = '! Data saved for image: %s\n' % self.currentimage.sourcename
                                f.write(iminfo)
                                if self.currentimage.slicepos is None:
                                    iminfo = '! Image was not a slice from N-dim. data source (N>2)'
                                else:
                                    iminfo = '! Axes in image: %s %s\n' % (self.currentimage.projection.ctype[0], self.currentimage.projection.ctype[1])
                                    iminfo += '! Slice position(s) on %s: %s\n' % (self.currentimage.sliceaxnames, self.currentimage.slicepos)
                                    if self.gipsy and gipsymod:
                                        iminfo += '! The slice positions are in FITS pixels\n'
                                        iminfo += '! For GIPSY grid coordinates subtract CRPIX first\n'
                                f.write(iminfo)
                                f.write('! Format of this file:\n')
                                f.write('! Shape # - object# - x pixel - y pixel - x world - y world\n')
                                f.write('! ---------------------------------------------------------\n')
                                for sh in self.shapes:
                                    for ol, objlist in enumerate(sh):
                                        for obj in objlist:
                                            if self.framesequal(obj.frame, self.currentimage.frame):
                                                im = self.images[obj.framenr]
                                                for mx, my in obj.xy:
                                                    if im.mixpix == None:
                                                        xw, yw = im.projection.toworld((mx, my))
                                                    else:
                                                        xw, yw, dum = im.projection.toworld((mx, my, im.mixpix))
                                                    f.write('%d %d %12f %12f %12f %12f\n' % (obj.shapetype, ol, mx, my, xw, yw))

                                f.close()
                                mes = 'Wrote shape data to file: %s' % filename
                                self.currentimage.messenger(mes)
                            else:
                                if keypressed == 'r':
                                    if self.inputfilename == None:
                                        self.currentimage.messenger('No input file name specified!')
                                        return
                                    im = self.currentimage
                                    framenr = self.getframenr(event)
                                    t = tabarray.tabarray(self.inputfilename)
                                    if not self.inputwcs:
                                        shapenr, polynr, x, y = t.columns((0, 1, 2,
                                                                           3))
                                    else:
                                        shapenr, polynr, xw, yw = t.columns((0, 1,
                                                                             4, 5))
                                        if im.mixpix == None:
                                            x, y = im.projection.topixel((xw, yw))
                                        else:
                                            x, y, dum = im.projection.topixel((xw, yw, im.mixpix))
                                    smax = shapenr.max()
                                    omax = polynr.max()
                                    for sh in range(self.numberoftypes):
                                        for ob in range(int(omax) + 1):
                                            xlist = []
                                            ylist = []
                                            for s, o, x1, y1 in zip(shapenr, polynr, x, y):
                                                if s == sh and o == ob:
                                                    xlist.append(x1)
                                                    ylist.append(y1)

                                            if len(xlist):
                                                self.addnewobject(sh, xlist, ylist, framenr)

                                    mes = 'Read data from file %s' % self.inputfilename
                                    self.currentimage.messenger(mes)
                                elif keypressed == 'u' and self.activeobject:
                                    if self.showactivestate:
                                        self.activeobject.set_inactive()
                                        self.active = True
                                        self.showactivestate = False
                                    else:
                                        self.activeobject.set_active(markers=True)
                                        self.showactivestate = True
                                    self.canvas.draw()

    def button_press(self, event):
        if not event.inaxes:
            return
        if self.toolbar.mode != '':
            return
        if not self.activeobject:
            return
        if event.button == 2:
            for i, fr in enumerate(self.frames):
                if fr.contains(event)[0]:
                    currentframe = i
                    break

            x = event.xdata
            y = event.ydata
            newgroup = None
            oldgroup = self.currentobj[self.currenttype]
            oldtype = self.currenttype
            self.activeobject.closestindx = self.activeobject.indexclosestmarker(event.x, event.y)
            oldactiveobject = self.activeobject
            for sh in self.shapes:
                for group, objlist in enumerate(sh):
                    obj = objlist[currentframe]
                    if obj.inside(x, y):
                        newgroup = group
                        newtype = obj.shapetype
                        self.activeobject = obj
                        break

                if newgroup != None:
                    break

            if newgroup == None:
                return
            for obj in self.shapes[oldtype][oldgroup]:
                if obj.active:
                    obj.set_inactive()

            for obj in self.shapes[newtype][newgroup]:
                markers = obj == self.activeobject
                obj.set_active(markers)

            self.currentobj[newtype] = newgroup
            self.currenttype = newtype
            self.canvas.draw()
        elif event.button == 1:
            self.xstart = event.xdata
            self.ystart = event.ydata
            self.activeobject.closestindx = self.activeobject.indexclosestmarker(event.x, event.y)
            if self.activeobject.closestindx == None and self.activeobject.inside(event.xdata, event.ydata):
                self.activeobject.closestindx = -1
            return

    def motion_notify(self, event):
        """ Move one marker or the whole object"""
        if not event.inaxes:
            return
        if self.toolbar.mode != '':
            return
        currentimage = self.getimage(event)
        if not self.activeobject:
            return
        if not self.activeobject.frame.contains(event)[0]:
            group = self.currentobj[self.currenttype]
            if group < 0:
                return
            framenr = self.getframenr(event)
            if framenr == None:
                return
            self.activeobject.set_inactive()
            self.activeobject = self.shapes[self.currenttype][group][framenr]
            self.activeobject.set_active(markers=True)
            self.canvas.draw()
            return
        self.currentimage = self.getimage(event)
        if self.currentimage == None:
            return
        if event.button == 1:
            xp = event.xdata
            yp = event.ydata
            group = self.currentobj[self.currenttype]
            if group < 0:
                return
            indx = self.activeobject.closestindx
            dx = xp - self.xstart
            dy = yp - self.ystart
            x0 = self.activeobject.x0
            y0 = self.activeobject.y0
            if indx is None:
                return
            if indx != -1:
                self.activeobject.movemarker(xp, yp, indx)
            else:
                xy_shifted = self.activeobject.moveall(dx, dy)
            for obj in self.shapes[self.currenttype][group]:
                if obj is not self.activeobject:
                    if self.wcs:
                        im1 = self.currentimage
                        im2 = self.images[obj.framenr]
                    if indx == -1:
                        if self.wcs:
                            xy_other = self.transformXY(xy_shifted, im1, im2)
                            x0_other, y0_other = self.transformXY((x0, y0), im1, im2)
                            obj.updatexy(xy_other, x0_other, y0_other)
                            obj.updatexy(xy_other, x0_other, y0_other)
                        else:
                            obj.moveall(dx, dy)
                    elif indx != None:
                        if self.wcs:
                            if self.currenttype in (self.polygon, self.spline):
                                xp_new, yp_new = self.transformXY((xp, yp), im1, im2)
                                obj.movemarker(xp_new, yp_new, indx)
                            else:
                                xy_other = self.transformXY(self.activeobject.xy, im1, im2)
                                x0_other, y0_other = self.transformXY((x0, y0), im1, im2)
                                obj.updatexy(xy_other, x0_other, y0_other)
                        else:
                            obj.movemarker(xp, yp, indx)

            self.xstart = xp
            self.ystart = yp
            if self.currenttype == self.spline:
                self.updatesplines()
            self.canvas.draw()

    def button_release(self, event):
        if not event.inaxes:
            return
        if self.toolbar.mode != '':
            return
        if not self.activeobject:
            return
        currentimage = self.getimage(event)
        if currentimage == None:
            return
        if event.button in (1, 3):
            self.activeobject.closestindx = None
        if event.button == 1 and self.currenttype == self.spline:
            self.updatesplines()
            self.canvas.draw()

    def framesequal(self, fr1, fr2):
        if fr1.get_position().x0 != fr2.get_position().x0:
            return False
        if fr1.get_position().x1 != fr2.get_position().x1:
            return False
        if fr1.get_position().y0 != fr2.get_position().y0:
            return False
        if fr1.get_position().y0 != fr2.get_position().y0:
            return False
        return True

    def plotresults(self, event):
        markerlist = [
         '+', ',', '.', '1', '2', '3', '4', '<', '>', 'D', 'H', '^', 'd', 'h', 'o', 'p', 's', 'v', 'x', '|']
        mes = '\nObject properties:'
        if self.gipsy and gipsymod:
            anyout(mes)
        else:
            print(mes)
        fluxlist = []
        for i, im in enumerate(self.images):
            for sh in self.shapes:
                for ol, objlist in enumerate(sh):
                    for obj in objlist:
                        if self.framesequal(obj.frame, im.frame):
                            if obj.allinsideframe():
                                if obj.spline:
                                    xy = obj.spline.xy
                                else:
                                    xy = obj.xy
                                obj.area, obj.sum = im.getflux(xy)
                                obj.flux = im.fluxfie(obj.sum, obj.area)
                                mes = 'Object %d with shape %d in image %d has area=%g, sum=%g, flux=%g' % (ol, obj.shapetype, i, obj.area, obj.sum, obj.flux)
                                if self.gipsy and gipsymod:
                                    anyout(mes)
                                else:
                                    print(mes)
                                fluxlist.append(obj.flux)
                            else:
                                mes = 'Object %d with shape %d in image %d has pixels outside frame' % (ol, obj.shapetype, i)
                                if self.gipsy and gipsymod:
                                    anyout(mes)
                                else:
                                    print(mes)
                                obj.area = obj.sum = obj.flux = None

        mindx = 0
        frameresult = self.frameresult
        frameresult.clear()
        for sh in self.shapes:
            for objlist in sh:
                x = []
                y = []
                for i, obj in enumerate(objlist):
                    x.append(i)
                    y.append(obj.flux)

                frameresult.plot(x, y, marker=markerlist[mindx], color='r', label=str(mindx))
                frameresult.plot(x, y, '-', color='k')
                mindx += 1
                if mindx == len(markerlist) - 1:
                    mindx = 0

        if len(fluxlist) == 0:
            self.figresult.canvas.draw()
            self.results = False
            return
        fluxlist = asarray(fluxlist)
        ymin = fluxlist.min()
        ymax = fluxlist.max()
        d = (ymax - ymin) / 20.0
        frameresult.set_ylim(ymin - d, ymax + d)
        frameresult.set_xlim(-0.5, self.numberofimages - 1 + 0.5)
        frameresult.set_title('Flux as function of shape and image')
        xticks = list(range(self.numberofimages))
        frameresult.set_xticks(xticks)
        frameresult.set_xlabel('Image number')
        frameresult.set_ylabel('Flux')
        frameresult.legend()
        self.results = True
        self.figresult.canvas.draw()

    def doquit(self, event):
        if self.gipsy and gipsymod:
            finis()
        else:
            exit()

    def saveresults(self, event):
        if not self.results:
            self.plotresults(event)
        stamp = datetime.now().strftime('%d%m%Y_%H%M%S')
        filename = 'flux_' + stamp + '.dat'
        f = open(filename, 'w')
        stamp = datetime.now().strftime('! Saved at %A %d/%m/%Y %H:%M:%S\n')
        f.write(stamp)
        f.write('! sh: 0=polygon  1=ellipse  2=circle  3=rectangle  4=spline\n')
        f.write('! obj: object number\n')
        for i, im in enumerate(self.images):
            iminfo = '! im %d = %s\n' % (i, im.basename)
            f.write(iminfo)

        f.write('!\n')
        f.write('! %4s %4s %4s %16s %16s %16s\n' % ('sh', 'obj', 'im', 'sum', 'area',
                                                    'flux'))
        line = '!' + '=' * 78 + '\n'
        f.write(line)
        for sh in self.shapes:
            for ol, objlist in enumerate(sh):
                for obj in objlist:
                    if obj.area != None:
                        f.write('  %4d %4d %4d %16g %16g %16g\n' % (obj.shapetype, ol, obj.framenr, obj.sum, obj.area, obj.flux))

        f.close()
        mes = 'Wrote flux results to file: %s' % filename
        self.currentimage.messenger(mes)
        if self.gipsy and gipsymod:
            anyout(mes)


def main():
    fig = figure(figsize=(10, 10), facecolor='#fff07e')
    frames = [None, None, None, None]
    frames[0] = fig.add_subplot(2, 2, 1, aspect=1, adjustable='box', autoscale_on=False)
    frames[1] = fig.add_subplot(2, 2, 2, aspect=1, adjustable='box', autoscale_on=False)
    frames[2] = fig.add_subplot(2, 2, 3, aspect=1, adjustable='box', autoscale_on=False)
    frames[3] = fig.add_subplot(2, 2, 4, aspect=1, adjustable='box', autoscale_on=False)
    frames[0].set_xlim(0, 10)
    frames[0].set_ylim(0, 10)
    frames[1].set_xlim(0, 8)
    frames[1].set_ylim(0, 7)
    frames[2].set_xlim(0, 8)
    frames[2].set_ylim(0, 11)
    frames[3].set_xlim(0, 8)
    frames[3].set_ylim(0, 7)
    names = [
     'm101', 'M1', 'L1', 'NGC2323']

    class Projection(object):

        def __init__(self, name):
            self.name = name

        def toworld(self, xy):
            if self.name != 'L1':
                xyw = asarray(xy) * 2.0
            else:
                xyw = xy
            return xyw

        def topixel(self, xy):
            if self.name != 'L1':
                xyp = asarray(xy) / 2.0
            else:
                xyp = xy
            return xyp

    class Image(object):

        def __init__(self, name, frame):
            self.name = name
            self.frame = frame
            self.projection = Projection(name)

        def positionmessage(self, x, y):
            return '%g %g' % (x, y)

        def getflux(xy, pixelstep=0.2):
            return (10, 3)

    images = []
    for n, f in zip(names, frames):
        im = Image(n, f)
        images.append(im)

    shapes = Shapecollection(images, fig, wcs=True)
    show()


if __name__ == '__main__':
    main()