# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/collective/flowplayercaptions/exportimport.py
# Compiled at: 2011-01-03 13:52:37
from Products.CMFCore.utils import getToolByName
_PROPERTIES = [
 dict(name='plugins/captionsContent/url', type_='string', value='${portal_url}++resource++collective.flowplayercaptions/flowplayer.content-3.2.0.swf'),
 dict(name='plugins/captionsContent/bottom', type_='int', value=30),
 dict(name='plugins/captionsContent/opacity', type_='string', value='1.0'),
 dict(name='plugins/captionsContent/backgroundColor', type_='string', value='#ffffff'),
 dict(name='plugins/captionsContent/backgroundGradient', type_='string', value='none'),
 dict(name='plugins/captionsContent/width', type_='string', value='90%'),
 dict(name='plugins/captionsContent/borderColor', type_='string', value='#000000'),
 dict(name='plugins/captionsContent/style/body/color', type_='string', value='#000000'),
 dict(name='plugins/captionsContent/style/body/fontSize', type_='string', value='14px'),
 dict(name='plugins/captions/url', type_='string', value='${portal_url}++resource++collective.flowplayercaptions/flowplayer.captions-3.2.2.swf'),
 dict(name='plugins/captions/captionTarget', type_='string', value='captionsContent')]

def import_various(context):
    if not context.readDataFile('collective.flowplayercaptions.txt'):
        return
    site = context.getSite()
    ptool = getToolByName(site, 'portal_properties')
    props = ptool.flowplayer_properties
    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])