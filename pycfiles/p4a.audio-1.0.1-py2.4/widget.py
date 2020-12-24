# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/browser/widget.py
# Compiled at: 2007-11-27 08:43:07
from zope import component
from zope.app.form.browser import widget
from p4a.audio import interfaces
from p4a.fileimage import file

class MediaPlayerWidget(file.FileDownloadWidget):
    """Widget which produces some form of media player.
    """
    __module__ = __name__

    def __call__(self):
        file_present = True
        if not self._data:
            file_present = False
        url = self.url
        if not file_present:
            return widget.renderElement('span', cssClass='media-absent media-player', contents='No media to play')
        field = self.context
        contentobj = field.context.context
        mime_type = unicode(contentobj.get_content_type())
        media_player = component.queryAdapter(field, interface=interfaces.IMediaPlayer, name=mime_type)
        if media_player is None:
            return widget.renderElement('span', cssClass='player-not-available media-player', contents='No available player for mime type "%s"' % mime_type)
        return '<div class="media-player">%s</div>' % media_player(url)