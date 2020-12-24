# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/helpers/output.py
# Compiled at: 2008-09-09 15:07:38
from lxml import etree
import sys

def csv(data):
    """ Outputs x,y data in .csv format. """
    res = []
    for line in data:
        assert len(line) == 2
        try:
            outline = float(line[0]) + ' ,' + float(line[1])
            res.append(outline)
        except ValueError:
            raise ValueError('Data provided not castable to float.\n')

    return res


class pelote(object):
    """ Represents a Pelote graph."""
    __module__ = __name__

    def __init__(self, title=None):
        self.root = etree.Element('plot')
        self.root.attrib['xmlns'] = 'http://www.uszla.me.uk/xsl/1.0/pelote'
        tnode = etree.Element('title')
        tnode.text = title
        self.root.append(tnode)
        self.pointlists = []
        self.axes = []
        self.range = None
        return

    class pointlist(object):
        __module__ = __name__

        def __init__(self):
            self.elem = etree.Element('pointList')

        def addpoint(self, x, y):
            try:
                float(x)
                float(y)
            except ValueError:
                print >> sys.stderr, x, y
                raise ValueError('Data not coercable to number.\n')

            point = etree.Element('point')
            point.attrib['x'] = str(x)
            point.attrib['y'] = str(y)
            self.elem.append(point)

        def addpoints(self, l):
            for (x, y) in l:
                self.addpoint(x, y)

    class _range(object):
        __module__ = __name__

        def __init__(self, floorX=None, floorY=None, ceilingX=None, ceilingY=None):
            if not floorX:
                if not floorY:
                    assert ceilingX or ceilingY
                    self.elem = etree.Element('range')
                    if floorX and ceilingX:
                        pass
                    else:
                        raise ceilingX > floorX or AssertionError
                if floorY and ceilingY:
                    pass
                else:
                    raise ceilingY > floorY or AssertionError
            try:
                if floorX:
                    float(floorX)
                    self.elem.attrib['floorX'] = str(floorX)
                if floorY:
                    float(floorY)
                    self.elem.attrib['floorY'] = str(floorY)
                if ceilingX:
                    float(ceilingX)
                    self.elem.attrib['ceilingX'] = str(ceilingX)
                if ceilingY:
                    float(ceilingY)
                    self.elem.attrib['ceilingY'] = str(ceilingY)
            except ValueError:
                raise ValueError('invalid value specified for range\n')

    class axis(object):
        __module__ = __name__

        def __init__(self):
            super(axis, self).__init__()

        class ticklist(object):
            """ Ticklist, attached to an axis in a Pelote graph."""
            __module__ = __name__

            def __init__(self, numticks=None):
                self.elem = etree.Element('tickList')
                if numticks:
                    self.elem.attrib['numTicks'] = str(numticks)

            def addtick(self, x):
                try:
                    float(x)
                except ValueError:
                    raise ValueError('tick value non-numeric\n')

                tick = etree.Element('tick')
                tick.attrib['value'] = str(x)

            def addticks(self, data):
                for x in data:
                    self.addtick(x)

        def __init__(self, orientation, position=None, title=None, numticks=None, ticks=None):
            self.elem = etree.Element('axis')
            assert orientation == 'x' or orientation == 'y'
            self.elem.attrib['type'] = orientation
            if position:
                try:
                    float(position)
                except ValueError:
                    raise ValueError('position value non-numeric\n')
                else:
                    self.elem.attrib['position'] = str(position)
            if title:
                self.elem.attrib['title'] = str(title)
            if numticks:
                self.addticklist(numticks=numticks)
            elif ticks:
                self.addticklist(data=ticks)

        def addticklist(self, numticks=None, data=None):
            assert numticks != None or data != None
            if numticks:
                try:
                    int(numticks)
                    assert int(numticks) > 0
                    tl = self.ticklist(numticks=numticks)
                    self.elem.append(tl.elem)
                except ValueError:
                    raise ValueError('non-integer number of ticks\n')

            elif data:
                tl = self.ticklist()
                tl.addticks(data)
                self.elem.append(tl.elem)
            return

    def attach(self, pl):
        if isinstance(pl, self.pointlist):
            self.pointlists.append(pl)
        if isinstance(pl, self.axis):
            self.axes.append(pl)
        if isinstance(pl, self._range):
            if self.range:
                raise AssertionError('Range already set!\n')
            self.range = pl

    def addpointlist(self, data=None):
        """ Attach a pointlist to a Pelote plot. """
        pl = self.pointlist()
        self.attach(pl)
        if data is not None:
            pl.addpoints(data)
        return pl

    def addaxis(self, orientation, position=None, title=None, numticks=None, ticks=None):
        """ Attach an axis to a Pelote plot."""
        ax = self.axis(orientation, position=position, title=title, numticks=numticks, ticks=ticks)
        self.attach(ax)

    def addrange(self, floorX=None, floorY=None, ceilingX=None, ceilingY=None):
        """ Attach a range to a Pelote plot. """
        r = self._range(floorX=floorX, floorY=floorY, ceilingX=ceilingX, ceilingY=ceilingY)
        self.attach(r)

    def serialize(self):
        """ Serialize a Pelote plot file as an ElementTree. """
        if self.range or len(self.axes) > 0:
            ps = etree.Element('paramSet')
            if self.range:
                ps.append(self.range.elem)
            for x in self.axes:
                ps.append(x.elem)

            self.root.append(ps)
        for l in self.pointlists:
            self.root.append(l.elem)

    def write(self, f):
        """ Serialize and write out a Pelote plot to a file or file-like object. 
        
        ``f`` can be either a string or a file-like object. If ``f`` is a string, 
        it is taken to be the filename to use."""
        if isinstance(f, basestring):
            f = open(f, 'w')
        self.serialize()
        print >> f, '<?xml version="1.0"?>'
        print >> f, '<?xml-stylesheet type="text/xsl" href="http://www.uszla.me.uk/xsl/1.0/pelote/pelote.xsl"?>'
        etree.ElementTree(self.root).write(f)