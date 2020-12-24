# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/conditions/filters.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 5895 bytes
"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '19/07/2018'
import fnmatch
from tomwer.core.log import TomwerLogger
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.scan.scanfactory import ScanFactory
import os, re
from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
_logger = TomwerLogger(__name__)

class BaseFilter(object):
    __doc__ = '\n    Apply a filter to an object\n    '

    def description(self):
        pass

    def isFiltered(self, value):
        """
        Return True if the value not filtered

        """
        raise NotImplementedError('Base class')


class _PatternBaseFilter(BaseFilter):
    __doc__ = 'Filter based on a pattern'

    def __init__(self, pattern):
        BaseFilter.__init__(self)
        self.setPattern(pattern)

    def setPattern(self, pattern):
        """
        compile th filter for the given pattern
        :param str pattern:
        """
        self._pattern = pattern

    def getPattern(self):
        return self._pattern


class RegularExpressionFilter(_PatternBaseFilter):
    __doc__ = 'Filter a string based on a defined pattern'

    def __init__(self, pattern):
        _PatternBaseFilter.__init__(self, pattern=pattern)

    def setPattern(self, pattern):
        super().setPattern(pattern)
        if self._pattern is not None:
            try:
                self._filter = re.compile(self._pattern)
            except re.error as e:
                try:
                    self.unvalidPatternDefinition(self._pattern, e)
                    _logger.error(e)
                finally:
                    e = None
                    del e

    def description(self):
        return 'Filter a string base on a regular expression'

    def isFiltered(self, value):
        try:
            match = self._filter.match(value) is None
        except:
            return False
            return match

    def unvalidPatternDefinition(self, pattern, error):
        _logger.error('%s is not a valid pattern. Error is %s' % (pattern, error))


class UnixFileNamePatternFilter(_PatternBaseFilter):
    __doc__ = "Filter a string based on 'fnmatch' module (unix filename pattern \n    matching)"

    def __init__(self, pattern):
        _PatternBaseFilter.__init__(self, pattern)

    def description(self):
        return 'Filter a string base on a glob (unix style pathname)'

    def isFiltered(self, value):
        try:
            match = fnmatch.fnmatch(value, self._pattern)
        except:
            match = False

        return not match


class FileNameFilter(_PatternBaseFilter, SingleProcess):
    __doc__ = 'Filter than can call several filter type'
    inputs = [
     _input_desc(name='data', type=TomoBase, handler='process', doc='scan path')]
    outputs = [
     _output_desc(name='data', type=TomoBase, doc='scan path')]
    FILTER_TYPES = ('unix file name pattern', 'regular expression')
    _DEFAULT_FILTER_TYPE = FILTER_TYPES[0]

    def __init__(self, pattern):
        self._fnFilter = UnixFileNamePatternFilter(pattern)
        self._reFilter = RegularExpressionFilter(pattern)
        self._filters = {}
        self._filters['unix file name pattern'] = self._fnFilter
        self._filters['regular expression'] = self._reFilter
        self._activeFilter = self._DEFAULT_FILTER_TYPE
        _PatternBaseFilter.__init__(self, pattern)
        SingleProcess.__init__(self)
        self.activeFilter = self._DEFAULT_FILTER_TYPE

    @property
    def activeFilter(self):
        return self._activeFilter

    @activeFilter.setter
    def activeFilter(self, filter_type):
        assert filter_type in self.FILTER_TYPES
        self._activeFilter = filter_type
        self._filters[self.activeFilter].setPattern(pattern=(self.getPattern()))

    def setPattern(self, pattern):
        super().setPattern(pattern)
        self._filters[self._activeFilter].setPattern(pattern)

    def isFiltered(self, value):
        return self._filters[self._activeFilter].isFiltered(value)

    def process(self, scan):
        _scan = scan
        if isinstance(scan, dict):
            _scan = ScanFactory.create_scan_object_frm_dict(scan)
        elif _scan is None:
            return False
            assert isinstance(_scan, TomoBase)
            if not self.isFiltered(os.path.basename(_scan.path)):
                if self._return_dict:
                    return _scan.to_dict()
                return _scan
        else:
            return