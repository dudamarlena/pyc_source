# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\packages\builtins.py
# Compiled at: 2010-12-23 17:42:44
"""
Standard packages required by SeisHub.
"""
from seishub.core.core import Component, implements
from seishub.core.db.util import formatResults
from seishub.core.packages.installer import registerStylesheet, registerIndex
from seishub.core.packages.interfaces import IPackage, IResourceType, IMapper
import os

class SeisHubPackage(Component):
    """
    The SeisHub package.
    """
    implements(IPackage)
    package_id = 'seishub'
    version = '0.1'


class StylesheetResource(Component):
    """
    A stylesheet resource type for SeisHub.
    """
    implements(IResourceType)
    package_id = 'seishub'
    resourcetype_id = 'stylesheet'
    registerStylesheet('xslt' + os.sep + 'index_xhtml.xslt', 'index.xhtml')
    registerStylesheet('xslt' + os.sep + 'index_json.xslt', 'index.json')
    registerStylesheet('xslt' + os.sep + 'meta_xhtml.xslt', 'meta.xhtml')
    registerStylesheet('xslt' + os.sep + 'meta_json.xslt', 'meta.json')
    registerStylesheet('xslt' + os.sep + 'resourcelist_xhtml.xslt', 'resourcelist.xhtml')
    registerStylesheet('xslt' + os.sep + 'resourcelist_json.xslt', 'resourcelist.json')
    registerStylesheet('xslt' + os.sep + 'resourcelist_admin.xslt', 'resourcelist.admin')
    registerIndex('media-type', '/xsl:stylesheet/xsl:output/@media-type', 'text')


class SchemaResource(Component):
    """
    A schema resource type for SeisHub.
    """
    implements(IResourceType)
    package_id = 'seishub'
    resourcetype_id = 'schema'


class XPathMapper(Component):
    """ 
    A mapper to directly query XPath expressions. 
    """
    implements(IMapper)
    package_id = 'seishub'
    mapping_url = '/xpath'

    def process_GET(self, request):
        if len(request.path) < 7:
            return {}
        xpath = request.path[6:]
        try:
            resources = self.env.catalog.query(xpath, full=True)
        except:
            return {}

        results = []
        for resource in resources:
            data = self.env.catalog.getIndexData(resource)
            data['package_id'] = resource.package._id
            data['resourcetype_id'] = resource.resourcetype._id
            data['document_id'] = resource.document._id
            data['resource_name'] = str(resource._name)
            results.append(data)

        return formatResults(request, results, count=len(results))