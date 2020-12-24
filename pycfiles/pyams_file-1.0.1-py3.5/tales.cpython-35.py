# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/skin/tales.py
# Compiled at: 2019-12-20 07:23:03
# Size of source mod 2**32: 4215 bytes
"""PyAMS_file.skin.tales module

This module provides several TALES extensions which can be used inside Chameleon templates.
"""
from pyramid.renderers import render
from zope.interface import Interface
from pyams_file.interfaces.thumbnail import IThumbnails
from pyams_file.skin import render_image
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

@adapter_config(name='picture', context=(
 Interface, Interface, Interface), provides=ITALESExtension)
class PictureTALESExtension(ContextRequestViewAdapter):
    __doc__ = "Picture TALES adapter\n\n    This TALES adapter can be used to automatically create a 'picture' HTML tag\n    embedding all image attributes.\n    "

    def render(self, context=None, lg_thumb='lg', lg_width=12, md_thumb='md', md_width=12, sm_thumb='sm', sm_width=12, xs_thumb='xs', xs_width=12, def_thumb=None, def_width=None, alt='', css_class=''):
        """Render TALES extension"""
        if context is None:
            context = self.context
        if context.content_type.startswith('image/svg'):
            return render('templates/svg-picture.pt', {'image': context, 
             'lg_width': lg_width, 
             'md_width': md_width, 
             'sm_width': sm_width, 
             'xs_width': xs_width, 
             'alt': alt, 
             'css_class': css_class}, request=self.request)
        if def_thumb is None:
            def_thumb = md_thumb or lg_thumb or sm_thumb or xs_thumb
        if def_width is None:
            def_width = md_width or lg_width or sm_width or xs_width
        return render('templates/picture.pt', {'image': context, 
         'lg_thumb': lg_thumb, 
         'lg_width': lg_width, 
         'md_thumb': md_thumb, 
         'md_width': md_width, 
         'sm_thumb': sm_thumb, 
         'sm_width': sm_width, 
         'xs_thumb': xs_thumb, 
         'xs_width': xs_width, 
         'def_thumb': def_thumb, 
         'def_width': def_width, 
         'alt': alt, 
         'css_class': css_class}, request=self.request)


@adapter_config(name='thumbnails', context=(
 Interface, Interface, Interface), provides=ITALESExtension)
class ThumbnailsExtension(ContextRequestViewAdapter):
    __doc__ = 'extension:thumbnails(image) TALES extension\n\n    This TALES extension returns the IThumbnails adapter of given image.\n    '

    def render(self, context=None):
        """Render TALES extension"""
        if context is None:
            context = self.context
        return IThumbnails(context, None)


@adapter_config(name='thumbnail', context=(
 Interface, Interface, Interface), provides=ITALESExtension)
class ThumbnailExtension(ContextRequestViewAdapter):
    __doc__ = 'extension:thumbnail(image, width, height, css_class, img_class) TALES extension\n\n    This TALES extension doesn\'t return an adapter but HTML code matching given image and\n    dimensions. If image is a classic image, an "img" tag with source to thumbnail of required\n    size is returned. If image in an SVG image, a "div" is returned containing whole SVG data of\n    given image.\n    '

    def render(self, context=None, width=None, height=None, css_class='', img_class=''):
        """Render TALES extension"""
        if context is None:
            context = self.context
        return render_image(context, width, height, self.request, css_class, img_class, True)