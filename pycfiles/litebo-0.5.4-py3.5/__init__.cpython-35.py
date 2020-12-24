# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/litebo/__init__.py
# Compiled at: 2020-05-03 06:11:49
# Size of source mod 2**32: 705 bytes
import os, sys
from litebo.utils import dependencies
__version__ = '0.5.4'
__author__ = 'ThomasYoung'
__MANDATORY_PACKAGES__ = '\ncython\npyrfr>=0.5.0\nsetuptools\nnumpy>=1.7.1\nscipy>=0.18.1\nConfigSpace>=0.4.6,<0.5\nscikit-learn==0.21.3\n'
dependencies.verify_packages(__MANDATORY_PACKAGES__)
supported_platforms = [
 'win32', 'linux2', 'linux1', 'darwin']
if sys.platform not in supported_platforms:
    raise ValueError('Lite-BO cannot run on platform-%s' % sys.platform)
if sys.version_info < (3, 5, 2):
    raise ValueError('Lite-BO requires Python 3.5.2 or newer.')