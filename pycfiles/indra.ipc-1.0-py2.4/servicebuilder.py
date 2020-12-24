# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/ipc/servicebuilder.py
# Compiled at: 2008-07-28 17:15:44
"""@file servicebuilder.py
@author Phoenix
@brief Class which will generate service urls.

$LicenseInfo:firstyear=2007&license=mit$

Copyright (c) 2007-2008, Linden Research, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
$/LicenseInfo$
"""
from indra.base import config
from indra.ipc import llsdhttp
from indra.ipc import russ
services_config = {}
try:
    services_config = llsdhttp.get(config.get('services-config'))
except:
    pass

_g_builder = None

def build(name, context={}, **kwargs):
    """ Convenience method for using a global, singleton, service builder.  Pass arguments either via a dict or via python keyword arguments, or both!

    Example use:
     > context = {'channel':'Second Life Release', 'version':'1.18.2.0'}
     > servicebuilder.build('version-manager-version', context)
       'http://int.util.vaak.lindenlab.com/channel/Second%20Life%20Release/1.18.2.0'
     > servicebuilder.build('version-manager-version', channel='Second Life Release', version='1.18.2.0')
       'http://int.util.vaak.lindenlab.com/channel/Second%20Life%20Release/1.18.2.0'
     > servicebuilder.build('version-manager-version', context, version='1.18.1.2')
       'http://int.util.vaak.lindenlab.com/channel/Second%20Life%20Release/1.18.1.2'
    """
    global _g_builder
    context = context.copy()
    context.update(kwargs)
    if _g_builder is None:
        _g_builder = ServiceBuilder()
    return _g_builder.buildServiceURL(name, context)


class ServiceBuilder(object):
    __module__ = __name__

    def __init__(self, services_definition=services_config):
        """        @brief
        @brief Create a ServiceBuilder.
        @param services_definition Complete services definition, services.xml.
        """
        self.services = services_definition['services']
        self.builders = {}
        for service in self.services:
            service_builder = service.get('service-builder')
            if not service_builder:
                continue
            if isinstance(service_builder, dict):
                for (name, builder) in service_builder.items():
                    full_builder_name = service['name'] + '-' + name
                    self.builders[full_builder_name] = builder

            else:
                self.builders[service['name']] = service_builder

    def buildServiceURL(self, name, context):
        """        @brief given the environment on construction, return a service URL.
        @param name The name of the service.
        @param context A dict of name value lookups for the service.
        @returns Returns the 
        """
        base_url = config.get('services-base-url')
        svc_path = russ.format(self.builders[name], context)
        return base_url + svc_path