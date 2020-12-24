# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDccLib/abstract/menu.py
# Compiled at: 2020-01-16 21:51:46
# Size of source mod 2**32: 1352 bytes
"""
Module that contains abstract implementation for DCC menus
"""
from __future__ import print_function, division, absolute_import
from tpPyUtils import decorators

class AbstractMenu(object):

    def __init__(self, name='AbstractMenu'):
        super(AbstractMenu, self).__init__()
        self._name = name

    @staticmethod
    @decorators.abstractmethod
    def create_category(category_name, category_items, parent_menu):
        """
        Creates a new category on the given menu. If not menu given this menu is used
        :param category_name: str, name of the category to add
        :param category_items: list(str), list of items to add to this category
        :param parent_menu: str
        :return:
        """
        raise NotImplementedError('abstract DCC menu function create_category() not implemented!')

    @decorators.abstractmethod
    def create_menu(self, file_path=None, parent_menu=None):
        """
        Creates a new DCC menu
        If file path is not given, menu is created without items
        :param file_path: str, path where JSON menu file is located
        :param parent_menu: str, name of the menu to append this menu into
        :return:
        """
        raise NotImplementedError('abstract DCC menu function create_menu() not implemented!')