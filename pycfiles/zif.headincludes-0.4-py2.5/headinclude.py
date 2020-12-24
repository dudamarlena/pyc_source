# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/headinclude.py
# Compiled at: 2010-03-12 11:12:03
""" utility to register an application's need for an inclusion inside <head>
"""
from zope.interface import implements
from zope.publisher.interfaces import IRequest
import zope.security.management, zope.security.interfaces, logging
from interfaces import IHeadIncludeRegistration

def getRequest():
    try:
        i = zope.security.management.getInteraction()
    except zope.security.interfaces.NoInteraction:
        return

    for p in i.participations:
        if IRequest.providedBy(p):
            return p


def doWarning():
    logging.getLogger().log(logging.WARN, 'headincludes not in wsgi filters. May affect js and css.')


class HeadIncluder(object):
    implements(IHeadIncludeRegistration)

    def register(self, url):
        request = getRequest()
        if request:
            includes = request.environment.get('wsgi.html.head.includes', '')
            if isinstance(includes, list):
                if url not in includes:
                    includes.append(url)
            else:
                doWarning()