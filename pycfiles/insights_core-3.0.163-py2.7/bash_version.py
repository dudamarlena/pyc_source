# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/rules/bash_version.py
# Compiled at: 2019-11-14 13:57:46
"""
Bash Version
============

This is a simple rule and can be run against the local host
using the following command::

$ insights-run -p examples.rules.bash_version

or from the examples/rules directory::

$ python sample_rules.py
"""
from insights.core.plugins import make_info, rule
from insights.parsers.installed_rpms import InstalledRpms
KEY = 'BASH_VERSION'
CONTENT = 'Bash RPM Version: {{ bash_version }}'

@rule(InstalledRpms)
def report(rpms):
    bash = rpms.get_max('bash')
    return make_info(KEY, bash_version=bash.nvra)