# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/pkg_resources/py2_warn.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 655 bytes
import sys, warnings, textwrap
msg = textwrap.dedent('\n    You are running Setuptools on Python 2, which is no longer\n    supported and\n    >>> SETUPTOOLS WILL STOP WORKING <<<\n    in a subsequent release (no sooner than 2020-04-20).\n    Please ensure you are installing\n    Setuptools using pip 9.x or later or pin to `setuptools<45`\n    in your environment.\n    If you have done those things and are still encountering\n    this message, please follow up at\n    https://bit.ly/setuptools-py2-warning.\n    ')
pre = 'Setuptools will stop working on Python 2\n'
sys.version_info < (3, ) and warnings.warn(pre + '************************************************************' + msg + '************************************************************')