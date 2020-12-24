# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/utils.py
# Compiled at: 2018-11-30 15:01:51
from brasil.gov.portal import _
from plone.formwidget.namedfile.converter import b64decode_file
from six.moves.urllib.parse import urlparse
from zope.interface import Invalid
import mimetypes
MESSAGE = _('You must use "Title|http://example.org" format to fill each line.')

def validate_list_of_links(value):
    """Check if value is a list of strings that follow the predefined
    format: "Title|http://example.org".
    """
    if not value:
        return True
    for item in value:
        if '|' not in item or item.count('|') > 1:
            raise Invalid(MESSAGE)
        _, v = item.split('|')
        parsed = urlparse(v.strip())
        if not all([parsed.scheme, parsed.netloc]):
            raise Invalid(MESSAGE)

    return True


def validate_background(value):
    """Check if file is an image or a video."""
    if not value:
        return True
    else:
        filename, _ = b64decode_file(value)
        mimetype, _ = mimetypes.guess_type(filename)
        if mimetype is None:
            return False
        return 'image' in mimetype or 'video' in mimetype