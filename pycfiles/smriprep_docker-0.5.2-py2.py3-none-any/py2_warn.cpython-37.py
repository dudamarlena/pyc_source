# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/setuptools/pkg_resources/py2_warn.py
# Compiled at: 2020-02-14 17:24:53
# Size of source mod 2**32: 723 bytes
import sys, warnings, textwrap
msg = textwrap.dedent('\n    You are running Setuptools on Python 2, which is no longer\n    supported and\n    >>> SETUPTOOLS WILL STOP WORKING <<<\n    in a subsequent release (no sooner than 2020-04-20).\n    Please ensure you are installing\n    Setuptools using pip 9.x or later or pin to `setuptools<45`\n    in your environment.\n    If you have done those things and are still encountering\n    this message, please comment in\n    https://github.com/pypa/setuptools/issues/1458\n    about the steps that led to this unsupported combination.\n    ')
pre = 'Setuptools will stop working on Python 2\n'
sys.version_info < (3, ) and warnings.warn(pre + '************************************************************' + msg + '************************************************************')