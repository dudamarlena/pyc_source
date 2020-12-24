# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cube\graphics.py
# Compiled at: 2007-04-06 03:29:04
from scenegraph import *

class NetworkCube(ColorCube):
    """A subclass of ColorCube that uses the inside space of the cube to
    display a scatter plot of points according to network data.  The axes
    correspond to the source address, destination address, and destination port
    of network packets."""
    __module__ = __name__

    def __init__(self):
        """Initialize a new NetworkCube.  This sets up axis minimums and
        maximums to their most extreme values and associates the x, y, and z
        axes with the packet source address, destination port, and destination
        address, respectively.  Additionally the color of each point
        corresponds to the destination port of the packet to ease visual
        interpretation of the interface."""
        ColorCube.__init__(self)
        self.optimize = 0
        self.data = []
        self.optdata = None
        self.optdatalen = 0
        self.unop_loops = 0
        self.xmin = 0
        self.xmax = 2 ** 32 - 1
        self.ymin = 0
        self.ymax = 2 ** 16 - 1
        self.zmin = 0
        self.zmax = 2 ** 32 - 1
        self.colors = {}
        self.map = {'x': 'ip_packet.source_address_n', 'y': 'ip_packet.tcp_packet.destination_port', 'z': 'ip_packet.destination_address_n', 'color': 'ip_packet.tcp_packet.destination_port'}
        return

    def value_for_axis(self, data, axis):
        """Pull a value from the given data according to the NetworkCube's
        mapping for the given axis.  For instance, by default the y axis is
        associated with a data packets ip_packet.tcp_packet.destination_port
        value.  This function retrieves that destination_port value from the
        data when axis is set to 'y'."""
        stack = []
        path = self.map[axis].split('.')
        d = data
        for pel in path:
            if d is not None and d.has_key(pel):
                d = d[pel]
                stack.append(d)
            else:
                return

        return d

    def color_for_val(self, y):
        """Return a color tuple (r,g,b,a) calculated from the list of colors
        given to the cube based on the y value given here where y >= 0.0 and y
        <= 1.0.  So, on a small scale, if the color list was the following:

            self.colors = {
                '0.0': (1.0, 0.0, 0.0, 0.5),
                '0.5': (0.0, 1.0, 0.0, 0.5),
                '1.0': (0.0, 0.0, 1.0, 0.5)
            }
            
        Then calling this function with a domain of values from 0.0 to 1.0
        would produce a range of results corresponding to a gradient from red
        at 0.0 to green at 0.5 to blue at 1.0 all the while maintaining a 50%
        transparency."""
        (lower, upper) = (0.0, 1.0)
        for (k, v) in self.colors.items():
            if lower < k and k < y:
                lower = k
            elif y < k and k < upper:
                upper = k

        lowcolor = self.colors[lower]
        highcolor = self.colors[upper]
        mod = (y - lower) / (upper - lower)
        r = lowcolor[0] + mod * (highcolor[0] - lowcolor[0])
        g = lowcolor[1] + mod * (highcolor[1] - lowcolor[1])
        b = lowcolor[2] + mod * (highcolor[2] - lowcolor[2])
        a = lowcolor[3] + mod * (highcolor[3] - lowcolor[3])
        return (
         r, g, b, a)

    def draw_points(self, points):
        """Execute OpenGL commands to draw the points in this object's data
        set.  For each point set the color using the
        NetworkCube.color_for_val(y) method."""
        for datum in points:
            d = {}
            for a in self.map.keys():
                d[a] = self.value_for_axis(datum, a)

            in_range = lambda v, min, max: min <= v and v <= max
            (x, y, z, color) = [ d[key] for key in ('x', 'y', 'z', 'color') ]
            if in_range(x, self.xmin, self.xmax) and in_range(y, self.ymin, self.ymax) and in_range(z, self.zmin, self.zmax):
                x = (x - self.xmin) / float(self.xmax - self.xmin)
                y = (y - self.ymin) / float(self.ymax - self.ymin)
                z = (z - self.zmin) / float(self.zmax - self.zmin)
                color = (color - self.ymin) / float(self.ymax - self.ymin)
                glColor4f(*self.color_for_val(color))
                glVertex3f(x, y, z)

    def render(self):
        """Render this object's pieces.  Note that the points are optionally
        organized into display lists based on a basic optimization schedule.
        Whenever 500 points have been added or after 30000 loops of having any
        un-optimized points it will re-create a display list.  During rendering
        this display list is rendered and then any unoptimized points are
        rendered."""
        GLObject._prerender(self)
        glBegin(GL_LINES)
        ColorCube._render(self)
        glEnd()
        l = len(self.data)
        if self.optimize == 1 and (l - self.optdatalen > 500 or self.unop_loops > 30000 and l > self.optdatalen):
            print 'Rebuilding list optdata=%s, optdatalen=%s, l=%s' % (self.optdata, self.optdatalen, l)
            if self.optdata is not None:
                glDeleteLists(self.optdata, 1)
            self.optdata = glGenLists(1)
            self.optdatalen = l
            glNewList(self.optdata, GL_COMPILE_AND_EXECUTE)
            glBegin(GL_POINTS)
            self.draw_points(self.data)
            glEnd()
            glEndList()
            self.unop_loops = 0
        else:
            if self.optdata is not None:
                glCallList(self.optdata)
            glBegin(GL_POINTS)
            self.draw_points(self.data[self.optdatalen:len(self.data)])
            glEnd()
            if l > self.optdatalen:
                self.unop_loops += 1
        GLObject._postrender(self)
        return