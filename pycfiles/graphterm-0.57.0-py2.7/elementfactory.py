# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/elementfactory.py
# Compiled at: 2012-08-15 03:48:07
from svgwrite import container
from svgwrite import shapes
from svgwrite import path
from svgwrite import image
from svgwrite import text
from svgwrite import gradients
from svgwrite import pattern
from svgwrite import masking
from svgwrite import animate
from svgwrite import filters
factoryelements = {'g': container.Group, 
   'svg': container.SVG, 
   'defs': container.Defs, 
   'symbol': container.Symbol, 
   'marker': container.Marker, 
   'use': container.Use, 
   'a': container.Hyperlink, 
   'script': container.Script, 
   'style': container.Style, 
   'line': shapes.Line, 
   'rect': shapes.Rect, 
   'circle': shapes.Circle, 
   'ellipse': shapes.Ellipse, 
   'polyline': shapes.Polyline, 
   'polygon': shapes.Polygon, 
   'path': path.Path, 
   'image': image.Image, 
   'text': text.Text, 
   'tspan': text.TSpan, 
   'tref': text.TRef, 
   'textPath': text.TextPath, 
   'textArea': text.TextArea, 
   'linearGradient': gradients.LinearGradient, 
   'radialGradient': gradients.RadialGradient, 
   'pattern': pattern.Pattern, 
   'clipPath': masking.ClipPath, 
   'mask': masking.Mask, 
   'animate': animate.Animate, 
   'set': animate.Set, 
   'animateColor': animate.AnimateColor, 
   'animateMotion': animate.AnimateMotion, 
   'animateTransform': animate.AnimateTransform, 
   'filter': filters.Filter}

class ElementBuilder(object):

    def __init__(self, cls, factory):
        self.cls = cls
        self.factory = factory

    def __call__(self, *args, **kwargs):
        kwargs['factory'] = self.factory
        return self.cls(*args, **kwargs)


class ElementFactory(object):

    def __getattr__(self, name):
        if name in factoryelements:
            return ElementBuilder(factoryelements[name], self)
        raise AttributeError("'%s' has no attribute '%s'" % (self.__class__.__name__, name))