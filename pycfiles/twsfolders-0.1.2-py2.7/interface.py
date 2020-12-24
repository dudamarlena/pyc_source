# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/interface.py
# Compiled at: 2014-07-10 04:53:00
from zope.interface import Interface, Attribute

class IItem(Interface):
    id = Attribute('')
    sid = Attribute('')
    name = Attribute('')
    title = Attribute('')
    description = Attribute('')
    parent = Attribute('')
    folder = Attribute('')
    created = Attribute('')
    modified = Attribute('')

    def has_property(self, name):
        """

        :param name:
        :return:
        """
        pass

    def get_property(self, name, default=None):
        """

        :param name:
        :param default:
        :return:
        """
        pass

    def set_property(self, name, value):
        """

        :param name:
        :param value:
        :return:
        """
        pass

    def get_properties(self, view=None):
        """

        :param view:
        :return:
        """
        pass

    def set_properties(self, properties):
        """

        :param properties:
        :return:
        """
        pass

    def mark_changed(self):
        """

        :return:
        """
        pass

    def get_url_item(self, url):
        """

        :param url:
        :return:
        """
        pass


class IFolder(IItem):

    def add_item(self, item, overwrite=False):
        """

        :param item:
        :param overwrite:
        :return:
        """
        pass

    def has_item(self, name):
        """

        :param name:
        :return:
        """
        pass

    def get_item(self, name):
        """

        :param name:
        :return:
        """
        pass

    def rename_item(self, name, new_name, overwrite=False):
        """

        :param name:
        :param new_name:
        :param overwrite:
        :return:
        """
        pass

    def delete_item(self, name):
        """

        :param name:
        :return:
        """
        pass

    def delete_items(self, names):
        """

        :param names:
        :return:
        """
        pass

    def move_item(self, name, target_folder, overwrite=False):
        """

        @param name:
        :param target_folder:
        :param overwrite:
        :return:
        """
        pass

    def list_items(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        pass

    def len_items(self):
        """

        :return:
        """
        pass


class IRootFolders(Interface):
    pass