# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/rules/sample_script.py
# Compiled at: 2019-05-16 13:41:33
"""
Sample Rule
===========

This is a simple rule and can be run against the local host
using the following command::

    $ insights-run -p examples.rules.sample_script

or from the examples/rules directory::

    $ ./sample_rules.py
"""
from insights.core.plugins import make_fail, make_pass, rule
from insights.parsers.redhat_release import RedhatRelease
CONTENT = 'This machine runs {{product}}.'

@rule(RedhatRelease, content=CONTENT)
def report(rel):
    """Fires if the machine is running Fedora."""
    if 'Fedora' in rel.product:
        return make_pass('IS_FEDORA', product=rel.product)
    else:
        return make_fail('IS_NOT_FEDORA', product=rel.product)


if __name__ == '__main__':
    from insights import run
    run(report, print_summary=True)