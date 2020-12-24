# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/audio.py
# Compiled at: 2013-04-04 15:36:35
"""Translates into an HTML5 C{<audio>} element."""
from muntjac.ui.abstract_media import AbstractMedia

class Audio(AbstractMedia):
    """The Audio component translates into an HTML5 C{<audio>} element and as
    such is only supported in browsers that support HTML5 media markup.
    Browsers that do not support HTML5 display the text or HTML set by calling
    L{setAltText}.

    A flash-player fallback can be implemented by setting HTML content allowed
    (L{setHtmlContentAllowed} and calling L{setAltText} with the flash player
    markup. An example of flash fallback can be found at the <a href=
    "https://developer.mozilla.org/En/Using_audio_and_video_in_Firefox#Using_Flash"
    >Mozilla Developer Network</a>.

    Multiple sources can be specified. Which of the sources is used is selected
    by the browser depending on which file formats it supports. See <a
    href="http://en.wikipedia.org/wiki/HTML5_video#Table">wikipedia</a> for a
    table of formats supported by different browsers.

    @author: Vaadin Ltd
    @author: Richard Lincoln
    """
    CLIENT_WIDGET = None

    def __init__(self, caption='', source=None):
        """@param caption: The caption of the audio component
        @param source: The audio file to play.
        """
        super(Audio, self).__init__()
        self.setCaption(caption)
        self.setSource(source)
        self.setShowControls(True)