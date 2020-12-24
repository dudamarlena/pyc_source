# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/inspect.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..tags.context import DataSetter
from ..elements import Attribute
from .. import errors
from moya.compat import text_type

class ElementContainer(object):

    def __init__(self, archive):
        self.archive = archive

    def __getitem__(self, elementid):
        return self.archive.get_element(elementid)

    def __contains__(self, elementid):
        try:
            self[elementid]
        except errors.ElementNotFoundError:
            return False

        return True


class Inspect(DataSetter):
    """
    Get an object which contains all the elements in the project.
    """

    class Help:
        synopsis = b'inspect elements in the project'

    def get_value(self, context):
        return ElementContainer(self.archive)


class QualifyElementref(DataSetter):
    """
    Qualifies an element reference.

    """
    app = Attribute(b'An application name', type=b'expression', default=None)
    lib = Attribute(b'A library name', type=b'expression', default=None)
    ref = Attribute(b'An element reference', type=b'expression', required=b'yes')

    class Meta:
        one_of = [
         ('app', 'lib')]

    class Help:
        synopsis = b'create an element reference with an app/lib name'

    def get_value(self, context):
        app, lib, ref = self.get_parameters(context, b'app', b'lib', b'ref')
        if app is not None:
            app = self.archive.get_app(app)
        if lib is not None:
            lib = self.archive.get_lib(lib)
        ref = text_type(ref)
        try:
            element = self.archive.get_element(ref, app=app, lib=lib or None)
        except Exception as e:
            self.throw(b'qualify-elementref.not-found', (b'unable to look up element ({})').format(e))

        element_ref = (b'{}#{}').format(element.app.name, element.element.libname)
        return element_ref