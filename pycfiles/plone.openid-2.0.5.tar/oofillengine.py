# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plone/oofill/oofillengine.py
# Compiled at: 2010-06-11 04:48:34
__doc__ = '\n$Id$\n'
__author__ = 'Jean-Nicolas Bès <contact@atreal.net>'
__docformat__ = 'plaintext'
__licence__ = 'GPL'
from zope.component import getMultiAdapter
from zope.interface import implements
from plone.oofill.interfaces import IOOFillEngine
from oofill.parser import OOFill
import StringIO

def renderMacro(context, view, viewname, macro):
    options = dict(template='here/@@' + viewname, macro=macro)
    extra_context = dict(options=options, view=view, template=view.index)

    def wrapper():
        text = context.macro_renderer.pt_render(extra_context=extra_context)
        return text

    return wrapper


class OOFillPTWrapper(object):
    __module__ = __name__


class OOFillEngine(object):
    """An odt filling engine.
    """
    __module__ = __name__
    implements(IOOFillEngine)

    def fillFromView(self, odtfile, context, viewname, outfile=None, protected=True):
        view = getMultiAdapter((context, context.REQUEST), name=viewname)
        obj = OOFillPTWrapper()
        for macro in view.index.macros.keys():
            setattr(obj, macro, renderMacro(context, view, viewname, macro))

        return self.fillFromObject(odtfile, obj, outfile, protected)

    def fillFromObject(self, odtfile, obj, outfile=None, protected=True):
        ofilinst = OOFill(odtfile)
        if outfile == None:
            outfile = StringIO.StringIO()
        ofilinst.render(obj, outfile, protected)
        return outfile