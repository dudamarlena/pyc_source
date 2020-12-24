# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/truepy/_license_data.py
# Compiled at: 2020-01-23 12:02:01
# Size of source mod 2**32: 4735 bytes
import json
from datetime import datetime
from ._name import Name
from ._bean_serializers import bean_class

@bean_class('de.schlichtherle.license.LicenseContent')
class LicenseData(object):
    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'
    UNKNOWN_NAME = 'CN=Unknown'

    @property
    def not_before(self):
        """The notBefore timestamp of this license"""
        return self._not_before

    @property
    def not_after(self):
        """The notAfter timestamp of this license"""
        return self._not_after

    @property
    def issued(self):
        """The issued timestamp of this license"""
        return self._issued

    @property
    def issuer(self):
        """The license issuer distinguished name"""
        return self._issuer

    @property
    def holder(self):
        """The license holder distinguished name"""
        return self._holder

    @property
    def subject(self):
        """The license subject"""
        return self._subject

    @property
    def consumer_type(self):
        """The type of entity to which this license is issued"""
        return self._consumer_type

    @property
    def info(self):
        """Generic information about this license"""
        return self._info

    @property
    def extra(self):
        """The license extra data"""
        return self._extra

    def __init__(self, not_before, not_after, issued=None, issuer=None, holder=None, subject=None, consumer_type=None, info=None, extra=None):
        """A class representing a license with a validity window and meta data.

        Any timestamps passed must be either instances of datetime.datetime, or
        strings parsable by License.TIMESTAMP_FORMAT; the timezone is assumed
        to be UTC.

        :param not_before: The timestamp when this license starts to be valid.
        :type not_before: datetime.datetime or str

        :param not_after: The timestamp when this license ceases to be valid.
            This must be strictly after `not_before`.
        :type not_after: datetime.datetime or str

        :param issued: The timestamp when this license was issued. This
            defaults to not_before.
        :type issued: datetime.datetime or str

        :param issuer: The issuer of this certificate. If not specified,
            UNKNOWN_NAME will be used.
        :type issuer: truepy.Name or str

        :param holder: The holder of this certificate. If not specified,
            UNKNOWN_NAME will be used.
        :type issuer: truepy.Name or str

        :param str subject: Free-form string data to associate with the
            license. This value will be stringified.

        :param str consumer_type: Free-form string data to associate with the
            license. This value will be stringified.

        :param str info: Free-form string data to associate with the license.
            This value will be stringified.

        :param object extra: Any type of data to store in the license. If this
            is not a string, it will be JSON serialised.
        """

        def timestamp(v):
            if isinstance(v, datetime):
                return v
            return datetime.strptime(v + ' UTC', self.TIMESTAMP_FORMAT + ' %Z')

        self._not_before = timestamp(not_before)
        self._not_after = timestamp(not_after)
        if self._not_before >= self._not_after:
            raise ValueError('%s is not before %s', self._not_before, self._not_after)
        else:
            self._issued = timestamp(issued or not_before)
            self._issuer = Name(str(issuer or self.UNKNOWN_NAME))
            self._holder = Name(str(holder or self.UNKNOWN_NAME))
            self._subject = str(subject or '')
            self._consumer_type = str(consumer_type or '')
            self._info = str(info or '')
            if not isinstance(extra, str):
                self._extra = json.dumps(extra)
            else:
                self._extra = extra