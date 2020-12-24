# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/reports/multistatus.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation.api import elementflow
PROP_METHOD = 0
PROP_NAMESPACE = 1
PROP_LOCALNAME = 2
PROP_DOMAIN = 3
PROP_PREFIXED = 4

def Multistatus_Response(resources=None, properties=None, stream=None, namespaces=None):
    with elementflow.xml(stream, 'D:multistatus', indent=True, namespaces=namespaces) as (response):
        for resource in resources:
            with response.container('D:response'):
                response.file.write(('<D:href>{0}</D:href>').format(resource.webdav_url))
                known = {}
                unknown = []
                for i in range(len(properties)):
                    prop = properties[i]
                    if hasattr(resource, prop[PROP_METHOD]):
                        x = getattr(resource, prop[PROP_METHOD])
                        known[prop] = x()
                        x = None
                    else:
                        unknown.append(prop)

                if len(known) > 0:
                    with response.container('D:propstat'):
                        response.element('D:status', text='HTTP/1.1 200 OK')
                        with response.container('D:prop'):
                            for prop in known.keys():
                                if known[prop] is None:
                                    response.element(prop[PROP_PREFIXED])
                                else:
                                    response.file.write(('<{0}>{1}</{0}>').format(prop[PROP_PREFIXED], known[prop]))

                if len(unknown) > 0:
                    with response.container('D:propstat'):
                        response.element('D:status', text='HTTP/1.1 404 Not found')
                        with response.container('D:prop'):
                            for prop in unknown:
                                response.element(prop[PROP_PREFIXED])

    return