# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/tests/api_hacks.py
# Compiled at: 2017-10-20 20:11:12
"""Hacks to work around API inconsistencies between Archetypes and Dexterity."""

def set_image_field(obj, image, content_type):
    """Set image field in object on both, Archetypes and Dexterity."""
    from plone.namedfile.file import NamedBlobImage
    try:
        try:
            obj.setImage(image)
        except AttributeError:
            data = image if type(image) == str else image.getvalue()
            obj.image = NamedBlobImage(data=data, contentType=content_type)

    finally:
        obj.reindexObject()