# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/draw.py
# Compiled at: 2020-01-18 11:47:38
import sys, os.path
sys.path.append(os.path.dirname(__file__))
from odf.namespaces import DRAWNS, STYLENS, PRESENTATIONNS
from odf.element import Element

def StyleRefElement(stylename=None, classnames=None, **args):
    qattrs = {}
    if stylename is not None:
        f = stylename.getAttrNS(STYLENS, 'family')
        if f == 'graphic':
            qattrs[(DRAWNS, 'style-name')] = stylename
        elif f == 'presentation':
            qattrs[(PRESENTATIONNS, 'style-name')] = stylename
        else:
            raise ValueError("Style's family must be either 'graphic' or 'presentation'")
    if classnames is not None:
        f = classnames[0].getAttrNS(STYLENS, 'family')
        if f == 'graphic':
            qattrs[(DRAWNS, 'class-names')] = classnames
        elif f == 'presentation':
            qattrs[(PRESENTATIONNS, 'class-names')] = classnames
        else:
            raise ValueError("Style's family must be either 'graphic' or 'presentation'")
    return Element(qattributes=qattrs, **args)


def DrawElement(name=None, **args):
    e = Element(name=name, **args)
    if 'displayname' not in args:
        e.setAttrNS(DRAWNS, 'display-name', name)
    return e


def A(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(DRAWNS, 'a'), **args)


def Applet(**args):
    return Element(qname=(DRAWNS, 'applet'), **args)


def AreaCircle(**args):
    return Element(qname=(DRAWNS, 'area-circle'), **args)


def AreaPolygon(**args):
    return Element(qname=(DRAWNS, 'area-polygon'), **args)


def AreaRectangle(**args):
    return Element(qname=(DRAWNS, 'area-rectangle'), **args)


def Caption(**args):
    return StyleRefElement(qname=(DRAWNS, 'caption'), **args)


def Circle(**args):
    return StyleRefElement(qname=(DRAWNS, 'circle'), **args)


def Connector(**args):
    return StyleRefElement(qname=(DRAWNS, 'connector'), **args)


def ContourPath(**args):
    return Element(qname=(DRAWNS, 'contour-path'), **args)


def ContourPolygon(**args):
    return Element(qname=(DRAWNS, 'contour-polygon'), **args)


def Control(**args):
    return StyleRefElement(qname=(DRAWNS, 'control'), **args)


def CustomShape(**args):
    return StyleRefElement(qname=(DRAWNS, 'custom-shape'), **args)


def Ellipse(**args):
    return StyleRefElement(qname=(DRAWNS, 'ellipse'), **args)


def EnhancedGeometry(**args):
    return Element(qname=(DRAWNS, 'enhanced-geometry'), **args)


def Equation(**args):
    return Element(qname=(DRAWNS, 'equation'), **args)


def FillImage(**args):
    args.setdefault('type', 'simple')
    return DrawElement(qname=(DRAWNS, 'fill-image'), **args)


def FloatingFrame(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(DRAWNS, 'floating-frame'), **args)


def Frame(**args):
    return StyleRefElement(qname=(DRAWNS, 'frame'), **args)


def G(**args):
    return StyleRefElement(qname=(DRAWNS, 'g'), **args)


def GluePoint(**args):
    return Element(qname=(DRAWNS, 'glue-point'), **args)


def Gradient(**args):
    return DrawElement(qname=(DRAWNS, 'gradient'), **args)


def Handle(**args):
    return Element(qname=(DRAWNS, 'handle'), **args)


def Hatch(**args):
    return DrawElement(qname=(DRAWNS, 'hatch'), **args)


def Image(**args):
    return Element(qname=(DRAWNS, 'image'), **args)


def ImageMap(**args):
    return Element(qname=(DRAWNS, 'image-map'), **args)


def Layer(**args):
    return Element(qname=(DRAWNS, 'layer'), **args)


def LayerSet(**args):
    return Element(qname=(DRAWNS, 'layer-set'), **args)


def Line(**args):
    return StyleRefElement(qname=(DRAWNS, 'line'), **args)


def Marker(**args):
    return DrawElement(qname=(DRAWNS, 'marker'), **args)


def Measure(**args):
    return StyleRefElement(qname=(DRAWNS, 'measure'), **args)


def Object(**args):
    return Element(qname=(DRAWNS, 'object'), **args)


def ObjectOle(**args):
    return Element(qname=(DRAWNS, 'object-ole'), **args)


def Opacity(**args):
    return DrawElement(qname=(DRAWNS, 'opacity'), **args)


def Page(**args):
    return Element(qname=(DRAWNS, 'page'), **args)


def PageThumbnail(**args):
    return StyleRefElement(qname=(DRAWNS, 'page-thumbnail'), **args)


def Param(**args):
    return Element(qname=(DRAWNS, 'param'), **args)


def Path(**args):
    return StyleRefElement(qname=(DRAWNS, 'path'), **args)


def Plugin(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(DRAWNS, 'plugin'), **args)


def Polygon(**args):
    return StyleRefElement(qname=(DRAWNS, 'polygon'), **args)


def Polyline(**args):
    return StyleRefElement(qname=(DRAWNS, 'polyline'), **args)


def Rect(**args):
    return StyleRefElement(qname=(DRAWNS, 'rect'), **args)


def RegularPolygon(**args):
    return StyleRefElement(qname=(DRAWNS, 'regular-polygon'), **args)


def StrokeDash(**args):
    return DrawElement(qname=(DRAWNS, 'stroke-dash'), **args)


def TextBox(**args):
    return Element(qname=(DRAWNS, 'text-box'), **args)