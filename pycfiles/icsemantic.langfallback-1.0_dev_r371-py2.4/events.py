# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/events.py
# Compiled at: 2008-10-06 10:31:06
"""
icsemantic.langfallback events

@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
from zope.component import getUtility
from icsemantic.core.interfaces import IicSemanticManagementContentTypes, IContentTypesMultilingualPatcher

def site_patcher(event):
    """
        handler que se dispara en el IBeforeTraverseEvent

        En el event.object recibe el portal y tiene que patchear
        a todos los ContentTypes que esten configurados

            >>> from icsemantic.langfallback.events import site_patcher

            >>> class Event: pass
            >>> event = Event()

        le paso cualquier porqueria como portal...
            >>> event.object = 'portal'
            >>> site_patcher(event)

        le paso un portal pero no es Site...
            >>> event.object = portal
            >>> site_patcher(event)

        le paso un portal que es un Site...
            >>> from zope.app.component.hooks import setSite
            >>> setSite(portal)
            >>> site_patcher(event)

    """
    if not getattr(event.object, '_v_multiligual_patched', None):
        try:
            pcm = getUtility(IicSemanticManagementContentTypes, name='icsemantic.configuration')
        except:
            return
        else:
            ccpatcher = getUtility(IContentTypesMultilingualPatcher)
            for type_name in pcm.fallback_types:
                try:
                    ccpatcher.patch(type_name, True)
                    event.object._v_multiligual_patched = True
                except:
                    pass

    return