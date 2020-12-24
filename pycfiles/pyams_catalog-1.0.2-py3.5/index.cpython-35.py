# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/index.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 6113 bytes
"""PyAMS_catalog.index module

This module provides several Hypatia indexes which use a discriminator based on interface
support of indexes objects.
"""
from datetime import date, datetime
from ZODB.broken import Broken
from hypatia.facet import FacetIndex
from hypatia.field import FieldIndex
from hypatia.keyword import KeywordIndex
from hypatia.text import TextIndex
from hypatia.text.lexicon import Lexicon
from hypatia.util import BaseIndexMixin
from persistent import Persistent
from pyams_catalog.interfaces import DATE_RESOLUTION, NO_RESOLUTION
from pyams_catalog.nltk import NltkFullTextProcessor
__docformat__ = 'restructuredtext'
_MARKER = object()

class InterfaceSupportIndexMixin(BaseIndexMixin):
    __doc__ = 'Custom index mixin handling objects interfaces'

    def __init__(self, interface):
        self.interface = interface

    def discriminate(self, obj, default):
        """See interface IIndexInjection"""
        if self.interface is not None:
            obj = self.interface(obj, None)
            if obj is None:
                pass
            return default
        if callable(self.discriminator):
            value = self.discriminator(obj, _MARKER)
        else:
            value = getattr(obj, self.discriminator, _MARKER)
        if callable(value):
            value = value(obj)
        if value is None or value is _MARKER:
            return default
        if isinstance(value, Persistent):
            raise ValueError('Catalog cannot index persistent object {0!r}'.format(value))
        if isinstance(value, Broken):
            raise ValueError('Catalog cannot index broken object {0!r}'.format(value))
        return value


class FieldIndexWithInterface(InterfaceSupportIndexMixin, FieldIndex):
    __doc__ = 'Field index with interface support'

    def __init__(self, interface, discriminator, family=None):
        InterfaceSupportIndexMixin.__init__(self, interface)
        FieldIndex.__init__(self, discriminator, family)


def get_resolution(value, resolution):
    """Set resolution of given date or datetime

        >>> from pyams_catalog.interfaces import *
        >>> from pyams_catalog.index import get_resolution
        >>> from datetime import date, datetime

    Starting with dates:

        >>> today = date(2017, 7, 11)
        >>> get_resolution(today, YEAR_RESOLUTION)
        datetime.date(2017, 1, 1)
        >>> get_resolution(today, MONTH_RESOLUTION)
        datetime.date(2017, 7, 1)
        >>> get_resolution(today, DATE_RESOLUTION)
        datetime.date(2017, 7, 11)

    Asking for a resolution higher than DATE with a date input only returns date:

        >>> get_resolution(today, MINUTE_RESOLUTION)
        datetime.date(2017, 7, 11)

    Same examples with datetimes:

        >>> now = datetime(2017, 7, 11, 13, 22, 10)
        >>> get_resolution(now, YEAR_RESOLUTION)
        datetime.datetime(2017, 1, 1, 0, 0)
        >>> get_resolution(now, MONTH_RESOLUTION)
        datetime.datetime(2017, 7, 1, 0, 0)
        >>> get_resolution(now, DATE_RESOLUTION)
        datetime.datetime(2017, 7, 11, 0, 0)
        >>> get_resolution(now, HOUR_RESOLUTION)
        datetime.datetime(2017, 7, 11, 13, 0)
        >>> get_resolution(now, MINUTE_RESOLUTION)
        datetime.datetime(2017, 7, 11, 13, 22)
        >>> get_resolution(now, SECOND_RESOLUTION)
        datetime.datetime(2017, 7, 11, 13, 22, 10)
    """
    if not value:
        return value
    if resolution < NO_RESOLUTION:
        args = []
        if not isinstance(value, datetime):
            resolution = min(resolution, DATE_RESOLUTION)
        args.extend(value.timetuple()[:resolution + 1])
        if isinstance(value, datetime):
            args.extend(([1] * (DATE_RESOLUTION - resolution) + [0] * 5)[:7 - len(args)])
            args.append(value.tzinfo)
            value = datetime(*args)
        else:
            args.extend([1] * (DATE_RESOLUTION - resolution))
            value = date(*args)
        return value


class DatetimeIndexWithInterface(FieldIndexWithInterface):
    __doc__ = 'Normalized datetime index with interface support'

    def __init__(self, interface, discriminator, resolution=DATE_RESOLUTION, family=None):
        FieldIndexWithInterface.__init__(self, interface, discriminator, family)
        self.resolution = resolution

    def discriminate(self, obj, default):
        value = super(DatetimeIndexWithInterface, self).discriminate(obj, default)
        return get_resolution(value, self.resolution)


class KeywordIndexWithInterface(InterfaceSupportIndexMixin, KeywordIndex):
    __doc__ = 'Keyword index with interface support'

    def __init__(self, interface, discriminator, family=None):
        InterfaceSupportIndexMixin.__init__(self, interface)
        KeywordIndex.__init__(self, discriminator, family)


class FacetIndexWithInterface(InterfaceSupportIndexMixin, FacetIndex):
    __doc__ = 'Facet index with interface support'

    def __init__(self, interface, discriminator, facets, family=None):
        InterfaceSupportIndexMixin.__init__(self, interface)
        FacetIndex.__init__(self, discriminator, facets, family)


class TextIndexWithInterface(InterfaceSupportIndexMixin, TextIndex):
    __doc__ = 'Text index with interface support'

    def __init__(self, interface, discriminator, lexicon=None, language='english', index=None, family=None):
        InterfaceSupportIndexMixin.__init__(self, interface)
        if lexicon is None:
            lexicon = Lexicon(NltkFullTextProcessor(language))
        TextIndex.__init__(self, discriminator, lexicon, index, family)