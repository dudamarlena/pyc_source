# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/reports/introspect.py
# Compiled at: 2012-10-12 07:02:39
from itertools import izip
from coils.core import CoilsException
from namespaces import XML_NAMESPACE, ALL_PROPS, REVERSE_XML_NAMESPACE

def introspect_properties(target):
    namespaces = {'http://apache.org/dav/props/': 'A', 'urn:ietf:params:xml:ns:caldav': 'C', 
       'DAV:': 'D', 
       'urn:ietf:params:xml:ns:carddav': 'E', 
       'http://groupdav.org/': 'G'}
    properties = []
    nm_ordinal = 74
    methods = [ method for method in dir(target) if method.startswith('get_property_') ]
    for method in methods:
        parts = method.split('_', 3)
        if len(parts) == 4:
            if parts[2] != 'unknown':
                namespace = REVERSE_XML_NAMESPACE.get(parts[2], 'DAV')
                if namespace.upper() == 'DAV':
                    prefix = 'D'
                elif namespace in namespaces:
                    prefix = namespaces[namespace]
                else:
                    prefix = chr(nm_ordinal)
                    namespaces[namespace] = prefix
                    nm_ordinal += 1
                element = parts[3].replace('_', '-')
                properties.append((method,
                 namespace,
                 element,
                 parts[2],
                 ('{0}:{1}').format(prefix, element)))

    keys = namespaces.iterkeys()
    values = namespaces.itervalues()
    namespaces = dict(izip(values, keys))
    return (properties, namespaces)