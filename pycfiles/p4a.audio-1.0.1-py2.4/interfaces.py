# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/interfaces.py
# Compiled at: 2007-11-27 08:43:15
from zope import interface
from zope import schema
from p4a.fileimage import file as p4afile
from p4a.fileimage import image as p4aimage
from p4a.audio import genre
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone4artists')

class IAnyAudioCapable(interface.Interface):
    """Any aspect of audio/content capable.
    """
    __module__ = __name__


class IPossibleAudio(IAnyAudioCapable):
    """All objects that should have the ability to be converted to some
    form of audio should implement this interface.
    """
    __module__ = __name__


class IAudioEnhanced(interface.Interface):
    """All objects that have their media features activated/enhanced
    should have this marker interface applied.
    """
    __module__ = __name__


class IAudio(interface.Interface):
    """Objects which have audio information.
    """
    __module__ = __name__
    title = schema.TextLine(title=_('Audio Title'), required=False)
    description = schema.Text(title=_('Description'), required=False)
    file = p4afile.FileField(title=_('File'), required=False)
    artist = schema.TextLine(title=_('Artist'), required=False)
    album = schema.TextLine(title=_('Album'), required=False)
    idtrack = schema.TextLine(title=_('Track Number'), required=False)
    audio_image = p4aimage.ImageField(title=_('Audio Image'), required=False, preferred_dimensions=(150,
                                                                                                    150))
    year = schema.Int(title=_('Year'), required=False)
    genre = schema.Choice(title=_('Genre'), required=False, vocabulary=genre.GENRE_VOCABULARY)
    comment = schema.Text(title=_('Comment'), required=False)
    variable_bit_rate = schema.Bool(title=_('Variable Bit Rate'), readonly=True)
    bit_rate = schema.Int(title=_('Bit Rate'), readonly=True)
    frequency = schema.Int(title=_('Frequency'), readonly=True)
    length = schema.Int(title=_('Length'), readonly=True)
    audio_type = schema.TextLine(title=_('Audio Type'), required=True, readonly=True)


class IAudioDataAccessor(interface.Interface):
    """Audio implementation accessor (ie mp3, ogg, etc).
    """
    __module__ = __name__
    audio_type = schema.TextLine(title=_('Audio Type'), required=True, readonly=True)

    def load(filename):
        """Load from filename"""
        pass

    def store(filename):
        """Store to filename"""
        pass


class IMediaPlayer(interface.Interface):
    """Media player represented as HTML.
    """
    __module__ = __name__

    def __call__(downloadurl):
        """Return the HTML required to play the audio content located
        at *downloadurl*.
        """
        pass


class IPossibleAudioContainer(IAnyAudioCapable):
    """Any folderish entity tha can be turned into an actual audio 
    container.
    """
    __module__ = __name__


class IAudioContainerEnhanced(interface.Interface):
    """Any folderish entity that has had it's IAudioContainer features
    enabled.
    """
    __module__ = __name__


class IAudioContainer(interface.Interface):
    """Folderish objects that have audio information, typically representing a CD."""
    __module__ = __name__
    title = schema.TextLine(title=_('Title'), required=False)
    description = schema.Text(title=_('Description'), required=False)
    artist = schema.TextLine(title=_('Artist'), required=False)
    audio_image = p4aimage.ImageField(title=_('CD Cover Image'), required=False, preferred_dimensions=(150,
                                                                                                       150))
    year = schema.Int(title=_('Year'), required=False)
    genre = schema.Choice(title=_('Genre'), required=False, vocabulary=genre.GENRE_VOCABULARY)


class IAudioProvider(interface.Interface):
    """Provide audio.
    """
    __module__ = __name__
    audio_items = schema.List(title=_('Audio Items'), required=True, readonly=True)


class IBasicAudioSupport(interface.Interface):
    """Provides certain information about audio support.
    """
    __module__ = __name__
    support_enabled = schema.Bool(title='Audio Support Enabled?', required=True, readonly=True)


class IAudioSupport(IBasicAudioSupport):
    """Provides full information about audio support.
    """
    __module__ = __name__


class IMediaActivator(interface.Interface):
    """For seeing the activation status or toggling activation."""
    __module__ = __name__
    media_activated = schema.Bool(title='Audio Activated', required=True, readonly=False)