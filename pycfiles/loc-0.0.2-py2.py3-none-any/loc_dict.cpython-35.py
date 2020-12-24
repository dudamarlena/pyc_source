# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/loc-project/loc/loc_dict.py
# Compiled at: 2018-10-18 22:52:49
# Size of source mod 2**32: 3250 bytes
"""
Implement Localization Dictionary Class, quickly translate text from one
locale to another.
"""
from bidict import bidict
from .locales import locale_list
from .compat import iteritems

class LocDict(object):
    __doc__ = "\n    Localization Dictionary.\n\n    Assumptions:\n\n    1. There's no duplicate words in single Locale.\n    2. There's no duplicate words globally in all Locales.\n\n    :param data: a dict, key = locale code, value = bi-direction dict.\n        key value definition for the bi-direction dict is, key = localized text,\n        value = number index.\n    :param locales: a list, supported locale list.\n    "

    def __init__(self, data):
        self.data = dict()
        self.locales = list()
        if isinstance(data, dict):
            self._init_with_dict(data)
        elif isinstance(data, (tuple, list)):
            self._init_with_list(data)

    def _init_with_dict(self, data):
        _data = dict()
        _locales = list()
        locale_vs_value_counts = dict()
        for locale in locale_list:
            if locale in data:
                value_list = data.get(locale)
                locale_vs_value_counts[locale] = len(value_list)
                _data[locale] = bidict(dict([(value, ind) for ind, value in enumerate(value_list)]))
                _locales.append(locale)

        count_set = set(locale_vs_value_counts.values())
        if len(count_set) != 1:
            locales_with_bad_data = list()
            for count in count_set:
                for locale, value_counts in locale_vs_value_counts.items():
                    if count == value_counts:
                        locales_with_bad_data.append(locale)
                        break

            msg = 'number of unique value in `{}` and `{}` is different!'.format(locales_with_bad_data[0], locales_with_bad_data[1])
            raise ValueError(msg)
        _locales.sort()
        self.data = _data
        self.locales = _locales

    def _init_with_list(self, data):
        _data = dict()
        for row in data:
            for locale, value in iteritems(row):
                try:
                    _data[locale].append(value)
                except:
                    _data[locale] = [
                     value]

        self._init_with_dict(_data)

    def find_locale(self, value):
        """
        Find the locale code for `value`.
        """
        for locale in self.locales:
            if value in self.data[locale]:
                return locale

        msg = "Can't detect language of '%s'" % value
        raise ValueError(msg)

    def trans_to(self, value, dst_loc, src_loc=None):
        """
        Translate the `value` to target locale language.
        """
        if dst_loc not in self.data:
            msg = '%s is not available!' % dst_loc
            raise ValueError(msg)
        if src_loc is None:
            src_loc = self.find_locale(value)
        try:
            ind = self.data[src_loc][value]
        except KeyError:
            msg = '%r is not available in %s' % (value, src_loc)
            raise KeyError(msg)

        return self.data[dst_loc].inv[ind]