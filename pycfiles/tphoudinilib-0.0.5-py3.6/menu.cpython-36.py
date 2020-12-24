# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpHoudiniLib/core/menu.py
# Compiled at: 2020-01-16 21:52:53
# Size of source mod 2**32: 895 bytes
"""
Module that contains functions and classes related with Maya menus
"""
from __future__ import print_function, division, absolute_import
import tpDccLib
from tpDccLib.abstract import menu as abstract_menu

class HoudiniMenu(abstract_menu.AbstractMenu, object):

    def __init__(self, name='HoudiniMenu'):
        super(HoudiniMenu, self).__init__()
        self.name = name

    def create_menu(self, file_path=None, parent_menu=None):
        """
        Creates a new DCC menu app
        If file path is not given the menu is created without items
        :param name: str, name for the menu
        :param file_path: str, path where JSON menu file is located
        :param parent_menu: str, Name of the menu to append this menu to
        :return: variant, nativeMenu || None
        """
        pass


tpDccLib.Menu = HoudiniMenu