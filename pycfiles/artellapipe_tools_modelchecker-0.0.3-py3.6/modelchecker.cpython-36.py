# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/modelchecker/widgets/modelchecker.py
# Compiled at: 2020-03-13 14:08:03
# Size of source mod 2**32: 557 bytes
"""
Module that contains model checker implementation for Artella
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import artellapipe

class ArtellaModelChecker(artellapipe.PyblishTool, object):

    def __init__(self, project, config, settings, parent):
        super(ArtellaModelChecker, self).__init__(project=project, config=config, settings=settings, parent=parent)