# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/pdf/utils.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import Image
except ImportError:
    from PIL import Image

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils import six

def convert_data_uri_to_image(data):
    """Convert a data: URI to a PIL image."""
    prefix = b'data:image/png;base64,'
    if not (isinstance(data, six.text_type) and data.startswith(prefix)):
        raise ValueError(b'Image is not a valid data uri')
    image_data = StringIO()
    image_data.write(data[len(prefix):].decode(b'base64', b'strict'))
    image_data.seek(0)
    image = Image.open(image_data)
    image.copy().verify()
    image_data.close()
    return image


def get_pdf_worker_url(extension):
    """Returns the URL for the pdf.worker script.

    This will return an appropriate URL based on whether or not we're in
    debug mode.

    Args:
        extension (rbpowerpack.extension.PowerPackExtension):
            The Power Pack extension instance.

    Returns:
        unicode:
        The static URL for the appropriate worker script.
    """
    if settings.DEBUG:
        worker_filename = b'lib/pdf.worker.js'
    else:
        worker_filename = b'libpdf-worker.min.js'
    return static(b'ext/%s/js/%s' % (extension.id, worker_filename))