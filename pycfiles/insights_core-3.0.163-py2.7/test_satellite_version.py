# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_satellite_version.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.satellite_version import Satellite6Version
from insights.parsers import ParseException
import pytest
satellite_version = '\nCOMMAND> cat /usr/share/foreman/lib/satellite/version.rb\n\nmodule Satellite\n  VERSION = "6.1.3"\nend\n'
no_sat = '\nscdb-1.15.8-1.el6sat.noarch                                 Wed May 18 14:48:14 2016\nscl-utils-20120927-27.el6_6.x86_64                          Wed May 18 14:18:16 2016\nSDL-1.2.14-6.el6.x86_64                                     Wed May 18 14:16:25 2016\n'

def test_get_sat6_version():
    result = Satellite6Version(context_wrap(satellite_version, path='satellite_version'))
    assert result.full == '6.1.3'
    assert result.version == '6.1.3'
    assert result.major == 6
    assert result.minor == 1
    assert result.release is None
    return


def test_get_no_sat_version():
    with pytest.raises(ParseException) as (e):
        Satellite6Version(context_wrap(no_sat, path='satellite_version'))
    assert 'Cannot parse satellite version' in str(e)