# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/utils.py
# Compiled at: 2018-01-29 16:00:07
from plone import api
from sc.photogallery.config import JS_RESOURCES

class PhotoGalleryMixin:
    """Common methods and functions used by views and and tiles."""

    def js_resources(self):
        """Return a list of JS resources that are not available in the
        registry, but need to be loaded anyway. This way the slideshow
        could use resources registered locally or globally.

        :returns: list of ids
        :rtype: list
        """
        js_registry = api.portal.get_tool('portal_javascripts')
        global_resources = js_registry.getResourceIds()
        return [ r for r in JS_RESOURCES if r not in global_resources ]


def last_modified(context):
    """Return the date of the most recently modified object in a container."""
    objects = context.objectValues()
    modified = [ int(obj.modified().strftime('%s')) for obj in objects ]
    modified.append(int(context.modified().strftime('%s')))
    modified.sort()
    return modified[(-1)]


def human_readable_size(size):
    """Return a number in human readable format."""
    if size < 0:
        raise ValueError
    if size < 1024:
        return str(size)
    else:
        for unit in ['kB', 'MB', 'GB']:
            size /= 1024.0
            if abs(size) < 1024.0:
                return ('{size:3.1f} {unit}').format(size=size, unit=unit)

        return ('{size:.1f} GB').format(size=size)