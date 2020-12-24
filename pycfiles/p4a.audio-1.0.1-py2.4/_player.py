# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/_player.py
# Compiled at: 2007-11-27 08:43:15
from zope import interface
from zope import component
from p4a.audio import interfaces
from Products.CMFCore import utils as cmfutils

class OggAudioPlayer(object):
    """An AudioPlayer for ogg"""
    __module__ = __name__
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)

    def __init__(self, context):
        self.context = context

    def __call__(self, downloadurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        player = '%s/++resource++oggplayer/cortado-ovt-stripped-0.2.2.jar' % site.absolute_url()
        return '\n        <div class="ogg-player">\n            <applet code="com.fluendo.player.Cortado.class" \n                    archive="%(player)s" \n         \t        width="100" height="50">\n              <param name="url" value="%(url)s"/>\n              <param name="local" value="false"/>\n              <param name="duration" value="00352"/>\n              <param name="video" value="false"/>\n              <param name="audio" value="true"/>\n              <param name="bufferSize" value="200"/>\n              <param name="debug" value="3" />\n              <param name="seekable" value="true" />\n              <param name="autoPlay" value="false" />\n              <param name="showStatus" value="false" />\n              <param name="statusHeight" value="20" />\n            </applet>\n        </div>\n        ' % {'player': player, 'url': downloadurl}