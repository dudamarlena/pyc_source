# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/skin.py
# Compiled at: 2014-05-10 19:33:20
from zope.publisher.interfaces.browser import IBrowserRequest, IBrowserSkinType
from zope.traversing.interfaces import IBeforeTraverseEvent
from ztfy.baseskin.interfaces import ISkinnable
from zope.component import adapter, queryUtility
from zope.publisher.skinnable import applySkin

@adapter(ISkinnable, IBeforeTraverseEvent)
def handleSkinTraversal(object, event):
    if IBrowserRequest.providedBy(event.request):
        path = event.request.get('PATH_INFO', '')
        if '++skin++' not in path:
            skin_name = ISkinnable(object).getSkin()
            if not skin_name:
                skin_name = 'ZMI'
            skin = queryUtility(IBrowserSkinType, skin_name)
            if skin is not None:
                applySkin(event.request, skin)
    return