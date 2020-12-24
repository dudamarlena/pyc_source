# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rhev_data_center.py
# Compiled at: 2019-05-16 13:41:33
"""
rhev_data_center - datasource ``rhev_data_center``
==================================================
"""
import json
from re import compile as re_compile
from insights import CommandParser, parser
from insights.parsers import SkipException
from insights.specs import Specs

@parser(Specs.rhev_data_center)
class RhevDataCenter(CommandParser):
    """Walk through the `/rhev/data-center` directory of RHEV host and return the
    full path of files not having correct file ownership i.e vdsm:kvm. See the
    `rhev_data_center` Datasource for more info.

    Attributes:
        data(list): A list of the parsed output returned by `rhev_data_center` Datasource.

        incorrect_volume_ownership(list): Volumes attached to the RHEV VMs in
          the Data Center having incorrect file ownership.

    Raises:
        SkipException: If no files are found with incorrect ownership.

    The following are available in ``data`` and ``incorrect_volume_ownership``:

        * ``name``  - file owner
        * ``group`` - file group
        * ``path``  - full path of a file

    Examples:
        >>> assert len(rhev_dc.data) == 4
        >>> assert len(rhev_dc.incorrect_volume_ownership) == 1
        >>> assert rhev_dc.incorrect_volume_ownership[0]['path'] == '/rhev/data-center/mnt/host1.example.com:_nfsshare_data/a384bf5d-db92-421e-926d-bfb99a6b4b28/images/b7d6cc07-d1f1-44b3-b3c0-7067ec7056a3/4d6e5dea-995f-4a4e-b487-0f70361f6137'
        >>> assert rhev_dc.incorrect_volume_ownership[0]['name'] == 'root'
        >>> assert rhev_dc.incorrect_volume_ownership[0]['group'] == 'root'

    """

    def parse_content(self, content):
        if not content:
            raise SkipException('No files found with incorrect ownership.')
        self.data = json.loads(('').join(content))
        _vol_path_pattern = re_compile('/images/[0-9,a-z,-]*/[0-9,a-z,-]*')
        self.incorrect_volume_ownership = [ each for each in self.data if _vol_path_pattern.search(each['path']) ]