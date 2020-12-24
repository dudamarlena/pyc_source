# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/serializers.py
# Compiled at: 2019-06-12 01:17:17
"""Utilities for serializing content."""
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise

class DjbletsJSONEncoder(DjangoJSONEncoder):
    """A JSON encoder that supports lazy strings, datetimes, and other objects.

    This is a specialization of
    :py:class:`~django.core.serializers.json.DjangoJSONEncoder` the does the
    following:

    * Evaluates strings translated with
      :py:func:`~django.utils.translation.ugettext_lazy` or
      :py:func:`~django.utils.translation.gettext_lazy` to real strings.

    * Removes the milliseconds and microseconds
      from :py:class:`datetimes <datetime.datetime>` (unless setting
      ``strip_datetime_ms=False`` when constructing the encoder). This is
      to help keep timestamps from appearing too new when compared against
      data coming from a MySQL database (which historically, and by default,
      chops off milliseconds).

    * Serializes Django :py:class:`models <django.db.models.base.Model>` with
      a ``to_json`` method via that method.
    """

    def __init__(self, strip_datetime_ms=True, *args, **kwargs):
        """Initialize the encoder.

        Args:
            strip_datetime_ms (bool, optional):
                Determines whether milliseconds should be stripped from a
                :py:class:`~datetime.datetime`. This is ``True`` by default,
                to preserve the old behavior of the encoder.
        """
        super(DjbletsJSONEncoder, self).__init__(*args, **kwargs)
        self.strip_datetime_ms = strip_datetime_ms

    def default(self, obj):
        """Encode the object into a JSON-compatible structure.

        Args:
            obj (object):
                The object to encode.

        Returns:
            object:
            A JSON-compatible structure (e.g., a :py:class:`dict`,
            :py:class:`list`, py:class:`unicode`, or :py:class:`bytes` object).
        """
        if isinstance(obj, Promise):
            return force_text(obj)
        if isinstance(obj, datetime.datetime) and self.strip_datetime_ms:
            r = obj.isoformat()
            if obj.microsecond:
                r = r[:19] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        if hasattr(obj, 'to_json') and callable(obj.to_json):
            return obj.to_json()
        return super(DjbletsJSONEncoder, self).default(obj)