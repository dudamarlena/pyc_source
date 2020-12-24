# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhn_schema_version.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.rhn_schema_version import rhn_schema_version
schema_content_ok = ('\n5.6.0.10-2.el6sat\n').strip()
schema_content_no = ('\n-bash: /usr/bin/rhn-schema-version: No such file or directory\n').strip()

def test_rhn_schema_version():
    result = rhn_schema_version(context_wrap(schema_content_ok))
    assert result == '5.6.0.10-2.el6sat'
    result = rhn_schema_version(context_wrap(schema_content_no))
    assert result is None
    return