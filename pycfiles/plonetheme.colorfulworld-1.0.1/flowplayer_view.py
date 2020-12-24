# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/browser/flowplayer_view.py
# Compiled at: 2010-09-15 08:23:40
from zope import interface
from zope import component
from Acquisition import aq_inner
import simplejson, urllib, os
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.flowplayer.utils import properties_to_dict, flash_properties_to_dict
from collective.flowplayer.interfaces import IFlowPlayable
from collective.flowplayer.interfaces import IMediaInfo, IFlowPlayerView
from plone.memoize.instance import memoize
from plone.memoize import view

class JavaScript(BrowserView):

    @view.memoize_contextless
    def portal_state(self):
        """ returns 
            http://dev.plone.org/plone/browser/plone.app.layout/trunk/plone/app/layout/globals/portal.py
        """
        return component.getMultiAdapter((self.context, self.request), name='plone_portal_state')

    @property
    def flowplayer_properties(self):
        properties_tool = getToolByName(self.context, 'portal_properties')
        return getattr(properties_tool, 'flowplayer_properties', None)

    @property
    def flowplayer_properties_as_dict(self):
        portal_url = self.portal_state().portal_url()
        return properties_to_dict(self.flowplayer_properties, portal_url, ignore=[
         'title',
         'loop',
         'initialVolumePercentage',
         'showPlaylist'])

    @property
    def flash_properties_as_dict(self):
        portal_url = self.portal_state().portal_url()
        return flash_properties_to_dict(self.flowplayer_properties, portal_url)

    def update(self):
        portal_url = self.portal_state().portal_url()
        if not portal_url.endswith('/'):
            portal_url += '/'
        self.show_cb_playlist_buttons = not self.flowplayer_properties.getProperty('showPlaylist')
        self.events = ''
        volume = self.flowplayer_properties.getProperty('initialVolumePercentage')
        if volume:
            self.events += '.onLoad( function() { this.setVolume(%d); })' % volume
        if self.flowplayer_properties.getProperty('loop'):
            self.events += '.onBeforeFinish( function() { return false; })'

    def __call__(self, request=None, response=None):
        """ Returns global configuration of the Flowplayer taken from portal_properties """
        self.update()
        self.request.response.setHeader('Content-type', 'text/javascript')
        return '(function($) {\n        $(function() { \n            $(\'.autoFlowPlayer\').each(function() {\n                var config = %(config)s;\n                if ($(this).is(\'.minimal\')) { config.plugins.controls = null; }\n                var audio = $(this).is(\'.audio\');\n                if (audio) {\n                    // $(this).width(500);\n                    config.plugins.controls.all = false;\n                    config.plugins.controls.play = true;\n                    config.plugins.controls.scrubber = true;\n                    config.plugins.controls.mute = true;\n                    config.plugins.controls.volume = true;\n                }\n                if ($(this).is(\'div\')) {\n                    // comming from Kupu, there are relative urls\n                    config.clip.baseUrl = $(\'base\').attr(\'href\');\n                    config.clip.url = $(this).find(\'a\').attr(\'href\');\n                    // Ignore global autoplay settings\n                    if ($(this).find(\'img\').length == 0) {\n                        // no image. Don\'t autoplay, remove all elements inside the div to show player directly.\n                        config.clip.autoPlay = false;\n                        $(this).empty();\n                    } else {\n                        // Clip is probably linked as image, so autoplay the clip after image is clicked\n                        config.clip.autoPlay = true;\n                    }\n                }\n                flowplayer(this, %(params)s, config)%(events)s;\n                $(\'.flowPlayerMessage\').remove();\n            });\n            $(\'.playListFlowPlayer\').each(function() {\n                var config = %(config)s;\n                var audio = $(this).is(\'.audio\');\n                if (audio) { config.plugins.controls.fullscreen = false; }\n                if ($(this).is(\'.minimal\')) { config.plugins.controls = null; }\n                if ($(this).find(\'img\').length > 0) { \n                    // has splash\n                    config.clip.autoPlay = true;\n                }\n                portlet_parents = $(this).parents(\'.portlet\');\n                var playlist_selector = \'div#flowPlaylist\';\n                if (portlet_parents.length > 0) {\n                    var portlet = true;\n                    // playlist has to be bound to unique item\n                    playlist_selector_id = portlet_parents.parent().attr(\'id\')+\'-playlist\';\n                    $(this).parent().find(\'.flowPlaylist-portlet-marker\').attr(\'id\', playlist_selector_id);\n                    playlist_selector = \'#\'+playlist_selector_id;\n                    if (audio) {\n                        config.plugins.controls.all = false;\n                        config.plugins.controls.play = true;\n                        config.plugins.controls.scrubber = true;\n                        config.plugins.controls.mute = true;\n                        config.plugins.controls.volume = false;\n                    }\n                } else {\n                    var portlet = false;\n                }\n                if (!portlet) {\n                    $("#pl").scrollable({items:playlist_selector, size:4, clickable:false});\n                }\n                // manual = playlist is setup using HTML tags, not using playlist array in config\n                flowplayer(this, %(params)s, config).playlist(playlist_selector, {loop: true, manual: true})%(events)s;\n                $(this).show();\n                $(\'.flowPlayerMessage\').remove();\n\n            });\n        });\n})(jQuery);\n' % dict(params=simplejson.dumps(self.flash_properties_as_dict), config=simplejson.dumps(self.flowplayer_properties_as_dict, indent=4), events=self.events)


class File(BrowserView):
    interface.implements(IFlowPlayerView)

    def __init__(self, context, request):
        super(File, self).__init__(context, request)
        self.info = IMediaInfo(self.context, None)
        self.height = self.info is not None and self.info.height or None
        self.width = self.info is not None and self.info.width or None
        self._audio_only = self.info is not None and self.info.audio_only or None
        if self.height and self.width:
            self._scale = 'height: %dpx; width: %dpx;' % (self.height, self.width)
        else:
            self._scale = ''
        return

    def audio_only(self):
        return self._audio_only

    def scale(self):
        return self._scale

    def videos(self):
        return [
         dict(url=self.href(), title=self.context.Title(), description=self.context.Description(), height=self.height, width=self.width, audio_only=self._audio_only)]

    def href(self):
        context = aq_inner(self.context)
        ext = ''
        url = self.context.absolute_url()
        filename = context.getFilename()
        if filename:
            extension = os.path.splitext(filename)[1]
            if not url.endswith(extension):
                ext = '?e=%s' % extension
        return self.context.absolute_url() + ext

    def imageGoto(self, toNext):
        catalog = getToolByName(self, 'portal_catalog')
        inner = self.context.aq_inner
        parent = inner.aq_parent
        parent_path = parent.getPhysicalPath()
        parent_url = ('/').join(parent_path)
        results = catalog.searchResults(path={'query': parent_url, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                               'File'))
        current = self.context.absolute_url()
        prev = None
        next = None
        found = False
        for item in results:
            if not found:
                if item.getURL() == current:
                    found = True
                else:
                    prev = item.getURL()
            elif IFlowPlayable.providedBy(item.getObject()) or item.portal_type == 'Image':
                next = item.getURL()
                break

        if toNext:
            if next is None:
                return
            else:
                return next + '/view'
        elif prev is None:
            return
        else:
            return prev + '/view'
        return

    def imageGotoThumb(self, toNext):
        catalog = getToolByName(self, 'portal_catalog')
        inner = self.context.aq_inner
        parent = inner.aq_parent
        parent_path = parent.getPhysicalPath()
        parent_url = ('/').join(parent_path)
        results = catalog.searchResults(path={'query': parent_url, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                               'File'))
        current = self.context.absolute_url()
        prev = None
        next = None
        found = False
        for item in results:
            if not found:
                if item.getURL() == current:
                    found = True
                else:
                    prev = item.getURL()
            elif IFlowPlayable.providedBy(item.getObject()) or item.portal_type == 'Image':
                next = item.getURL()
                break

        if toNext:
            if next is None:
                return
            else:
                return next + '/image_mini'
        elif prev is None:
            return
        else:
            return prev + '/image_mini'
        return


class Link(File):

    def href(self):
        return self.context.getRemoteUrl()


class Folder(BrowserView):
    interface.implements(IFlowPlayerView)

    @memoize
    def playlist_class(self):
        properties_tool = getToolByName(self.context, 'portal_properties')
        props = getattr(properties_tool, 'flowplayer_properties', None)
        return props.getProperty('showPlaylist') and 'flowPlaylistVisible' or 'flowPlaylistHidden'

    @memoize
    def audio_only(self):
        return len([ v for v in self.videos() if not v['audio_only'] ]) == 0

    @memoize
    def scale(self):
        height = 0
        width = 0
        if self.audio_only():
            height = 27
            width = 400
        for video in self.videos():
            if video['height'] > height or video['width'] > width:
                height = video['height']
                width = video['width']

        if height and width:
            return 'height: %dpx; width: %dpx;' % (height, width)

    @memoize
    def videos(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = []
        for brain in self._query():
            video = brain.getObject()
            if not IFlowPlayable.providedBy(video):
                continue
            view = component.getMultiAdapter((
             video, self.request), interface.Interface, 'v2_flowplayer')
            results.append(dict(url=view.href(), title=brain.Title, description=brain.Description, height=view.height, width=view.width, audio_only=view.audio_only()))

        return results

    def first_clip_url(self):
        """ Clip must be quoted to playlist is able to find it in the flowplayer-playlist onBegin/getEl method call """
        videos = self.videos()
        if videos:
            return urllib.quote(videos[0].get('url'))
        else:
            return
        return

    def _query(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(object_provides=IFlowPlayable.__identifier__, path={'depth': 1, 'query': ('/').join(self.context.getPhysicalPath())}, sort_on='getObjPositionInParent')

    def imageGoto(self, toNext):
        catalog = getToolByName(self, 'portal_catalog')
        inner = self.context.aq_inner
        parent = inner.aq_parent
        parent_path = parent.getPhysicalPath()
        parent_url = ('/').join(parent_path)
        results = catalog.searchResults(path={'query': parent_url, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                               'File'))
        current = self.context.absolute_url()
        prev = None
        next = None
        found = False
        for item in results:
            if not found:
                if item.getURL() == current:
                    found = True
                else:
                    prev = item.getURL()
            elif IFlowPlayable.providedBy(item.getObject()) or item.portal_type == 'Image':
                next = item.getURL()
                break

        if toNext:
            if next is None:
                return
            else:
                return next + '/view'
        elif prev is None:
            return
        else:
            return prev + '/view'
        return


class Topic(Folder):
    interface.implements(IFlowPlayerView)

    def _query(self):
        return self.context.queryCatalog()