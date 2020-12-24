# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/vma_ra_enabled_s390x.py
# Compiled at: 2019-12-13 11:35:35
"""
VmaRaEnabledS390x - file ``/sys/kernel/mm/swap/vma_ra_enabled``
===============================================================

Parser to parse the output of file ``/sys/kernel/mm/swap/vma_ra_enabled``
"""
from insights import Parser, parser
from insights.specs import Specs
from insights.parsers import SkipException

@parser(Specs.vma_ra_enabled)
class VmaRaEnabledS390x(Parser):
    """
    Base class to parse ``/sys/kernel/mm/swap/vma_ra_enabled`` file,
    the file content will be stored in a string.

    Sample output for file::

        True

    Examples:
        >>> type(vma)
        <class 'insights.parsers.vma_ra_enabled_s390x.VmaRaEnabledS390x'>
        >>> vma.ra_enabled
        True

    Attributes:
        ra_enabled (bool): The result parsed

    Raises:
        SkipException: When file content is empty

    """

    def parse_content(self, content):
        if not content:
            raise SkipException('Input content is empty')
        if content[0] == 'True':
            self.ra_enabled = True
        else:
            self.ra_enabled = False