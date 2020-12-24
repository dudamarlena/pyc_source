# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/templatetags/djblets_images.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import division, unicode_literals
import logging, re
from django import template
from django.template import TemplateSyntaxError
from django.utils import six
from django.utils.html import format_html, format_html_join
from django.utils.six.moves import cStringIO as StringIO
from django.utils.translation import ugettext as _
from PIL import Image
from djblets.util.decorators import blocktag
logger = logging.getLogger(__name__)
register = template.Library()

def save_image_to_storage(image, storage, filename):
    """Save an image to storage."""
    f = storage.open(filename, mode=b'w+b')
    image.save(f, b'png')
    f.close()


@register.simple_tag
def crop_image(f, x, y, width, height):
    """
    Crops an image at the specified coordinates and dimensions, returning the
    resulting URL of the cropped image.
    """
    filename = f.name
    storage = f.storage
    basename = filename
    if filename.find(b'.') != -1:
        basename = filename.rsplit(b'.', 1)[0]
    new_name = b'%s_%d_%d_%d_%d.png' % (basename, x, y, width, height)
    if not storage.exists(new_name):
        try:
            f = storage.open(filename)
            data = StringIO(f.read())
            f.close()
            image = Image.open(data)
            image = image.crop((x, y, x + width, y + height))
            save_image_to_storage(image, storage, new_name)
        except (IOError, KeyError) as e:
            logger.exception(b'Error cropping image file %s at %d, %d, %d, %d and saving as %s: %s', filename, x, y, width, height, new_name, e)
            return b''

    return storage.url(new_name)


@register.filter
def thumbnail(f, size=b'400x100'):
    """Create a thumbnail of the given image.

    This will create a thumbnail of the given ``file`` (a Django FileField or
    ImageField) with the given size. Size can either be a string of WxH (in
    pixels), or a 2-tuple. If the size is a tuple and the second part is None,
    it will be calculated to preserve the aspect ratio.

    This will return the URL to the stored thumbnail.
    """
    if isinstance(size, six.string_types):
        x, y = (int(x) for x in size.split(b'x'))
        size_str = size
    elif isinstance(size, tuple):
        x, y = size
        if y is None:
            size_str = b'%d' % x
        else:
            size_str = b'%dx%d' % (x, y)
    else:
        raise ValueError(b'Thumbnail size "%r" could not be be parsed', size)
    filename = f.name
    if filename.find(b'.') != -1:
        basename, format = filename.rsplit(b'.', 1)
        miniature = b'%s_%s.%s' % (basename, size_str, format)
    else:
        basename = filename
        miniature = b'%s_%s' % (basename, size_str)
    storage = f.storage
    if not storage.exists(miniature):
        try:
            f = storage.open(filename, b'rb')
            data = StringIO(f.read())
            f.close()
            image = Image.open(data)
            if y is None:
                x = min(image.size[0], x)
                y = int(x * (image.size[1] / image.size[0]))
            image.thumbnail([x, y], Image.ANTIALIAS)
            save_image_to_storage(image, storage, miniature)
        except (IOError, KeyError) as e:
            logger.exception(b'Error thumbnailing image file %s and saving as %s: %s', filename, miniature, e)
            return b''

    return storage.url(miniature)


def build_srcset(sources):
    """Return the source set attribute value for the given sources.

    The resulting sources will be sorted by value, with the pixel density
    (``x``) values coming before width (``w``) values.

    Args:
        sources (dict):
            A mapping of descriptors (e.g., ``'2x'`` or ``'512w'``) that
            describe the requirement for the source to be shown to URLs.

    Returns:
        unicode:
        The returned ``srcset`` attribute value.
    """

    def _compare_sources(a, b):
        a_descriptor_type = a[0][(-1)]
        b_descriptor_type = b[0][(-1)]
        if a_descriptor_type == b_descriptor_type:
            return cmp(a[1], b[1])
        else:
            if a_descriptor_type == b'x':
                return -1
            return 1

    sources_info = []
    for descriptor, url in six.iteritems(sources):
        if not url:
            continue
        if not descriptor:
            descriptor = b'1x'
        valid = descriptor.endswith(('x', 'w'))
        if valid:
            try:
                sources_info.append((descriptor, float(descriptor[:-1]), url))
            except ValueError:
                valid = False

        if not valid:
            raise ValueError(_(b'"%s" is not a valid srcset size descriptor.') % descriptor)

    sources_info = sorted(sources_info, cmp=_compare_sources)
    return format_html_join(b', ', b'{0} {1}', ((url, descriptor) for descriptor, descriptor_value, url in sources_info))


@register.simple_tag
def srcset(sources):
    """Render the source set attribute value for the given sources.

    The resulting sources will be sorted by value, with the pixel density
    (``x``) values coming before width (``w``) values.

    Args:
        sources (dict):
            A mapping of descriptors (e.g., ``'2x'`` or ``'512w'``) that
            describe the requirement for the source to be shown to URLs.

    Returns:
        unicode:
        The rendered ``srcset`` attribute value.
    """
    try:
        return build_srcset(sources)
    except ValueError as e:
        raise TemplateSyntaxError(six.text_type(e))


@register.tag
@blocktag(end_prefix=b'end_')
def image_source_attrs(context, nodelist, *options):
    """Render source attributes for an image tag.

    This will render ``src="..." srcset="..."`` attributes for an ``<img>``
    tag, based on the sources provided in the tag's content. There should be
    one source definition per line (with an optional trailing comma) in the
    form of::

        <descriptor> <URL>

    These will get turned into a ``srcset``, and the ``1x`` descriptor (which
    is required) will be set as the ``src`` attribute.

    Args:
        block_content (unicode):
            The block content containing image sources.

    Returns:
        Attributes for the ``<img>`` tag.

    Example:
        .. code-block:: html+django

           <img {% image_source_attrs %}
                1x {%  static "images/myimage.png" %}
                2x {%  static "images/myimage@2x.png" %}
                3x {%  static "images/myimage@3x.png" %}
                {% end_image_source_attrs %}>
    """
    content = nodelist.render(context).strip()
    try:
        sources = {}
        for source in re.split(b',|\\n+', content):
            source = source.strip()
            if source:
                descriptor, url = source.split(b' ', 1)
                sources[descriptor.strip()] = url.strip()

    except ValueError:
        raise TemplateSyntaxError(_(b'The source definition passed to {% image_source_attrs %} is not structured correctly. Make sure that there is one source definition per line and that it contains a descriptor and a URL.'))

    try:
        src_value = sources[b'1x']
    except KeyError:
        raise TemplateSyntaxError(_(b'The source definition passed to {% image_source_attr %} must contain a "1x" descriptor.'))

    return format_html(b'src="{0}" srcset="{1}"', src_value, build_srcset(sources))