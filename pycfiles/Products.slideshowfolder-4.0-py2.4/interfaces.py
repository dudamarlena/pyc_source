# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/interfaces.py
# Compiled at: 2008-07-12 15:34:57
"""
module: slideshowfolder
created by: Johnpaul Burbank <jpburbank@tegus.ca>
Date: July 8, 2007
"""
from zope.interface import Interface
from zope import schema
from Products.slideshowfolder import SlideshowFolderMessageFactory as _

class ISlideShowFolder(Interface):
    """ Marker interface for a folder that holds content that implements ISlideshowImage"""
    __module__ = __name__


class ISlideshowImage(Interface):
    """ Interface for content items that can act as slideshow images.
    
        Such content should have an Archetypes ImageField called 'image'.
    """
    __module__ = __name__


class ISlideShowSettings(Interface):
    """Slide show setting fields"""
    __module__ = __name__
    showWidth = schema.Int(title=_('label_slideshow_width', default='Slideshow Width'), description=_('help_slideshow_width', default='Width of the slideshow in pixels.  Images will be shrunk to fit within the dimensions of the slideshow.'), default=600)
    showHeight = schema.Int(title=_('label_slideshow_height', default='Slideshow Height'), description=_('help_slideshow_height', default='Height of the slideshow in pixels.  Images will be shrunk to fit within the dimensions of the slideshow.'), default=450)
    slideDuration = schema.Int(title=_('label_slide_duration', default='Slide Duration'), description=_('help_slide_duration', default='Time in seconds between slide transitions'), default=5)
    transitionTime = schema.Float(title=_('label_trasition_time', default='Transition Time'), description=_('help_transition_time', default='Time in seconds for a slide transition to take place.'), default=0.5)
    thumbnails = schema.Bool(title=_('label_thumbnail_mode', default='Thumbnail Mode'), description=_('help_thumbnail_mode', default='Include navigation thumbnails below the image.'), default=True)
    fast = schema.Bool(title=_('label_fast_mode', default='Fast Mode'), description=_('help_fast_mode', default='Skips the slide transition when a user clicks on a thumbnail.'))
    captions = schema.Bool(title=_('label_show_captions', default='Show Captions'), description=_('help_show_captions', default='Include captions below the image.'), default=True)
    arrows = schema.Bool(title=_('label_show_controller', default='Show Controller'), description=_('help_show_controller', default='Include play/pause/forward/back controller in the slideshow.'), default=True)
    random = schema.Bool(title=_('label_random_order', default='Random order'), description=_('help_random_order', default='Shows slides in a random order.'))
    loop = schema.Bool(title=_('label_loop_slideshow', default='Loop Slideshow'), description=_('help_loop_slideshow', default='Repeats the slideshow once it has finished.'), default=True)
    linked = schema.Bool(title=_('label_link_images', default='Link images'), description=_('help_link_images', default='Link images to full-sized version'))


class ISlideShowView(Interface):
    """Browser view for the slide show folder"""
    __module__ = __name__

    def setWorkflowFilter(wf_filter='published'):
        """ Sets the review_state which will be used to filter the slideshow.  Defaults
            to 'published'.  May be set to None to disable filtering.
        """
        pass

    def getSlideshowImages():
        """Returns a list of images for the current slideshowfolder in a dict.
           Keys: 'name', 'caption'.
        """
        pass

    def getSlideshowSettings():
        """ Returns a dict of settings for the current slideshowfolder.
        """
        pass

    def getSlideshowSize():
        """ Returns a dict containing the name of the slideshow's image size,
            the width, and the height.
        """
        pass

    def getControllerTranslations():
        """ Returns a list of dicts, each containing the 'id' and 'msg' for a
            slideshow controller button.
        """
        pass


class IFolderSlideShowView(Interface):
    """Provides view methods in regards to the transition from folder to slideshow folder"""
    __module__ = __name__

    def isSlideshow():
        """Returns true if we're implementing the ISlideShowFolder interface.
        
        (Note: we're using implementation of that interface as a proxy for a few other
        behaviors that aren't technically w/in the scope of the interface, such
        as having the view selected and the config tab added.)"""
        pass

    def makeSlideshow():
        """Make a folderish object a slideshowfolder"""
        pass

    def unmakeSlideshow():
        """Remove all traces of slideshow-ness from a folder"""
        pass