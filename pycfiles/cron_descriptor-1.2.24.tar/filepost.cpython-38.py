# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/filepost.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 2440 bytes
from __future__ import absolute_import
import binascii, codecs, os
from io import BytesIO
from .packages import six
from packages.six import b
from .fields import RequestField
writer = codecs.lookup('utf-8')[3]

def choose_boundary():
    """
    Our embarrassingly-simple replacement for mimetools.choose_boundary.
    """
    boundary = binascii.hexlify(os.urandom(16))
    if not six.PY2:
        boundary = boundary.decode('ascii')
    return boundary


def iter_field_objects(fields):
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    if isinstance(fields, dict):
        i = six.iteritems(fields)
    else:
        i = iter(fields)
    for field in i:
        if isinstance(field, RequestField):
            yield field
        else:
            yield (RequestField.from_tuples)(*field)


def iter_fields(fields):
    """
    .. deprecated:: 1.6

    Iterate over fields.

    The addition of :class:`~urllib3.fields.RequestField` makes this function
    obsolete. Instead, use :func:`iter_field_objects`, which returns
    :class:`~urllib3.fields.RequestField` objects.

    Supports list of (k, v) tuples and dicts.
    """
    if isinstance(fields, dict):
        return ((k, v) for k, v in six.iteritems(fields))
    return ((
     k, v) for k, v in fields)


def encode_multipart_formdata(fields, boundary=None):
    """
    Encode a dictionary of ``fields`` using the multipart/form-data MIME format.

    :param fields:
        Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).

    :param boundary:
        If not specified, then a random boundary will be generated using
        :func:`urllib3.filepost.choose_boundary`.
    """
    body = BytesIO()
    if boundary is None:
        boundary = choose_boundary()
    for field in iter_field_objects(fields):
        body.write(b('--%s\r\n' % boundary))
        writer(body).write(field.render_headers())
        data = field.data
        if isinstance(data, int):
            data = str(data)
        elif isinstance(data, six.text_type):
            writer(body).write(data)
        else:
            body.write(data)
        body.write(b'\r\n')

    body.write(b('--%s--\r\n' % boundary))
    content_type = str('multipart/form-data; boundary=%s' % boundary)
    return (
     body.getvalue(), content_type)