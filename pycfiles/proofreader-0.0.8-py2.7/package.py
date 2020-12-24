# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/proofreader/license_checker/package.py
# Compiled at: 2018-03-13 09:30:54


class Package(object):
    LICENSE_TAG = 'License: '
    NAME_TAG = 'Name: '
    _meta_data = []

    def __init__(self, pkg_obj):
        """
        :param pkg_obj: :class: `pkg_resources.DistInfoDistribution`
        """
        self._pkg_obj = pkg_obj

    def _extract_meta_value(self, tag):
        """Find a target value by `tag` from given meta data.

        :param tag: str
        :param meta_data: list
        :return: str
        """
        try:
            return [ l[len(tag):] for l in self.meta_data if l.startswith(tag) ][0]
        except IndexError:
            return '* Not Found *'

    @property
    def license(self):
        return self._extract_meta_value(self.LICENSE_TAG)

    @property
    def meta_data(self):
        if not self._meta_data:
            for tag in ['METADATA', 'PKG-INFO']:
                try:
                    self._meta_data = list(self._pkg_obj.get_metadata_lines(tag))
                except (IOError, KeyError):
                    pass

        return self._meta_data

    @property
    def name(self):
        return self._extract_meta_value(self.NAME_TAG)

    @property
    def version(self):
        return self._pkg_obj.version or ''