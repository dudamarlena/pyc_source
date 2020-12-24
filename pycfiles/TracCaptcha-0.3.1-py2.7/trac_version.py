# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/trac_version.py
# Compiled at: 2011-02-04 14:14:08
import trac
from trac_captcha.lib.version import Version
version_sequence = map(int, trac.__version__.split('dev')[0].split('.'))
if len(version_sequence) < 3:
    version_sequence.append(0)
trac_version = Version(major=version_sequence[0], minor=version_sequence[1], patch_level=version_sequence[2])