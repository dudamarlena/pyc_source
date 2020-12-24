# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/bundledescription.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.xmlparser import Element
from salamoia.h2o.bundle import Description
from salamoia.h2o.schema import SchemaDescription
from salamoia.h2o.service import ServiceDescription
__all__ = [
 'BundleDescription']

class FeatureElement(Element):
    __module__ = __name__
    childClasses = {}
    attributes = ['path']
    parserClass = None

    def init(self):
        super(FeatureElement, self).init()
        self.content = self.parserClass(self.filewrapper().bundle.resourceWrapper(self.path))


class SchemaElement(FeatureElement):
    __module__ = __name__
    parserClass = SchemaDescription


class ServiceElement(FeatureElement):
    __module__ = __name__
    parserClass = ServiceDescription


class BundleDescription(Description):
    """
    Root element of the XML bundle description found in salamoia_bundle.xml
    """
    __module__ = __name__
    childClasses = {'schema': SchemaElement, 'service': ServiceElement}
    attributes = [
     'name']
    rootElementName = 'bundle'
    dtd = 'bundle.dtd'

    def activate(self):
        for i in self.children:
            i.content.activate()

    def __repr__(self):
        return '<Bundle %s>' % self.name


from salamoia.tests import *
runDocTests()