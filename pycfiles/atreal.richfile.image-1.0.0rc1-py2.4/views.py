# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/image/browser/views.py
# Compiled at: 2009-09-04 10:39:07
from zope.interface import implements
from atreal.richfile.image.interfaces import IImageable
from atreal.richfile.qualifier.common import RFView
from atreal.richfile.qualifier.interfaces import IRFView
from atreal.richfile.image import RichFileImageMessageFactory as _

class RFImageView(RFView):
    __module__ = __name__
    plugin_interface = IImageable
    kss_id = 'image'
    viewlet_name = 'atreal.richfile.image.viewlet'
    update_message = _('The image preview has been updated.')
    active_message = _('Image preview activated.')
    unactive_message = _('Image preview un-activated.')