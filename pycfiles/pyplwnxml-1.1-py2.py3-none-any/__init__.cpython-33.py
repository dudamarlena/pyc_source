# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pluzz/__init__.py
# Compiled at: 2014-05-17 07:41:24
# Size of source mod 2**32: 238 bytes
import os, sys, gettext
if sys.version_info.major != 3:
    raise Exception('Sorry this software only works with python 3.')
gettext.install('pypluzz', os.path.join(os.path.dirname(__file__), 'i18n'))