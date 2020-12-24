# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/naming/core/naminglib.py
# Compiled at: 2020-03-08 12:44:32
# Size of source mod 2**32: 656 bytes
"""
Library that extends tpNameIt library functionality to support paths templates
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from tpDcc.libs.python import decorators
from tpDcc.libs.nameit.core import namelib
from artellapipe.libs import naming

@decorators.Singleton
class ArtellaNameLib(namelib.NameLib, object):

    def __init__(self):
        namelib.NameLib.__init__(self)
        self.naming_file = naming.config.get_path()
        self.init_naming_data()