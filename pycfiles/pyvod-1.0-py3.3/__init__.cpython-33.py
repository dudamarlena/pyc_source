# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/vod/__init__.py
# Compiled at: 2014-05-20 13:56:49
# Size of source mod 2**32: 293 bytes
__import__('pkg_resources').declare_namespace(__name__)
import os, sys, gettext
if sys.version_info.major != 3:
    raise Exception('Sorry this software only works with python 3.')
gettext.install('pyvod', os.path.join(os.path.dirname(__file__), 'i18n'))