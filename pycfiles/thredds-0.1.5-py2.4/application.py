# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/thredds/application.py
# Compiled at: 2006-11-25 19:23:46
"""
THREDDS catalog generator implemented as a WSGI application.

This WSGI app generates a THREDDS catalog for a given directory.
It can be used to serve static data, or combined with the pydap DAP
server.

For static data, use the following configuration together with Paste
Deploy::

    [composit:main]
    use = egg:Paste#cascade
    app1 = static
    app2 = thredds
    catch = 404

    [app:static]
    use = egg:Paste#static
    document_root = /path/to/data

    [app:thredds]
    use = egg:thredds
    name = myserver
    root = /path/to/data
    type = HTTPServer

With pydap, try this::

    [composit:main]
    use = egg:Paste#cascade
    app1 = thredds
    app2 = pydap
    catch = 404

    [app:thredds]
    use = egg:thredds
    name = myserver
    root = /path/to/data
    type = OpenDAP

    [app:pydap]
    use = egg:dap
    root = /path/to/data
"""
__author__ = 'Roberto De Almeida <rob@pydap.org>'
import os
from paste.request import construct_url
from paste.httpexceptions import HTTPException, HTTPNotFound
try:
    from dap.plugins.lib import loadhandler
except ImportError:
    pass

from thredds import templess
catalog = '<catalog t:attr="name name" version="1.0.1" \n    xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"\n    xmlns:xlink="http://www.w3.org/1999/xlink"\n    xmlns:t="http://johnnydebris.net/xmlns/templess">\n\n    <service t:attr="name service; base base; serviceType type" />\n\n    <dataset t:attr="name dataset">\n        <metadata inherited="true">\n            <serviceName t:content="service" />\n        </metadata>\n        <dataset t:replace="datasets" />\n    </dataset>\n\n    <catalogRef t:replace="subdirs" />\n</catalog>'
dataset = '<dataset xmlns:t="http://johnnydebris.net/xmlns/templess"\n    t:attr="name name; urlPath url" />'
catalogRef = '<catalogRef xmlns:t="http://johnnydebris.net/xmlns/templess"\n    t:attr="xlink:href url; xlink:title name; name name" />'

def make_app(global_conf, root, **kwargs):
    return ThreddsCatalog(root, **kwargs)


class ThreddsCatalog(object):
    __module__ = __name__

    def __init__(self, root, name=None, type='File', template=None, stylesheet=None):
        self.root = root
        self.name = name or 'THREDDS catalog'
        self.type = type
        self.template = template
        self.xsl = stylesheet
        self._dataset_template = templess.template(dataset)
        self._catalogRef_template = templess.template(catalogRef)
        self._catalog_template = templess.template(catalog)

    def __call__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        path_info = environ.get('PATH_INFO', '')
        if path_info.endswith('/catalog.xml'):
            path = path_info[:-len('/catalog.xml')]
            path = path.lstrip('/')
            return self._catalog(path)
        else:
            raise HTTPNotFound

    def _catalog(self, basepath):
        if self.template:
            self._catalog_template = templess.template(open(self.template))
        if self.type.lower() == 'file':
            base = 'file://%s' % self.root
        else:
            base = construct_url(self.environ, with_query_string=False, with_path_info=False)
        dir = os.path.join(self.root, basepath)
        dirs, files = [], []
        for item in os.listdir(dir):
            path = os.path.join(dir, item)
            if os.path.isdir(path):
                context = {'name': item, 'url': os.path.join(basepath, item, 'catalog.xml')}
                subdir = self._catalogRef_template.render(context)
                dirs.append(subdir)
            elif self.type.lower() in ['opendap', 'dods']:
                try:
                    H = loadhandler(path)
                    context = {'name': H.description, 'url': os.path.join(basepath, item)}
                    dataset = self._dataset_template.render(context)
                    files.append(dataset)
                    H.close()
                except:
                    pass

            else:
                context = {'name': item, 'url': os.path.join(basepath, item)}
                dataset = self._dataset_template.render(context)
                files.append(dataset)

        output = []
        if self.xsl:
            output.append('<?xml-stylesheet href="%s" type="text/xsl"?>' % self.xsl)
        context = {'name': self.name, 'base': base + '/', 'service': self.name, 'type': self.type, 'dataset': '%s data' % self.name, 'datasets': files, 'subdirs': dirs}
        output.append(self._catalog_template.unicode(context).encode('utf-8'))
        headers = [
         ('Content-type', 'application/xml; charset=utf-8')]
        self.start('200 OK', headers)
        for line in output:
            yield line