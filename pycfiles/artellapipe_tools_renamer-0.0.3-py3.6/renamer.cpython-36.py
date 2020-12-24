# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/renamer/widgets/renamer.py
# Compiled at: 2020-03-13 14:14:59
# Size of source mod 2**32: 946 bytes
"""
Tool that allow to rename DCC nodes in an easy way
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import artellapipe
from artellapipe.libs.naming.core import naminglib
import tpDcc
from tpDcc.tools.renamer.widgets import renamer

class ArtellaRenamerWidget(renamer.RenamerWidget, object):
    NAMING_LIB = naminglib.ArtellaNameLib

    def __init__(self, config, parent):
        naming_config = tpDcc.ConfigsMgr().get_config(config_name='tpDcc-naming',
          package_name=(artellapipe.project.get_clean_name()),
          root_package_name='tpDcc',
          environment=(artellapipe.project.get_environment()))
        super(ArtellaRenamerWidget, self).__init__(config=config, naming_config=naming_config, parent=parent)