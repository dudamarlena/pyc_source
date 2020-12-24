# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/rootfolders.py
# Compiled at: 2014-07-10 08:54:58
from zope.interface import implementer
from ZODB.Connection import Connection
import _compat
from _logger import log_debug
from interface import IRootFolders
from folder import Folder
from prefixes import URL_SEPARATOR, is_interface, validate_item

class RootAlreadyExistError(Exception):
    """ Root already exist."""
    pass


class RootDoNotExistError(Exception):
    """ Root do not exist."""
    pass


class ValidatorRefusedError(Exception):
    """ Root already exist."""
    pass


class NotExceptableValidatorError(Exception):
    """ Root already exist."""
    pass


@implementer(IRootFolders)
class RootFolders(object):

    def __init__(self, connection, validator=None):
        """
        @param connection: ZODB DB Storage connection
        @param validator:
        """
        if not isinstance(connection, Connection):
            raise TypeError('connection must an instance of ZODB Connection')
        if validator and not callable(validator):
            raise TypeError('validator must be callable')
        self.__root = connection.root()
        if validator is not None and not callable(validator) and not is_interface(validator):
            raise NotExceptableValidatorError('Validator must a callable or zope.interface')
        self.validator = validator
        log_debug('created with connection: %s' % connection, 'folders')
        return

    def get_url_item(self, url=None):
        if not url:
            return
        else:
            if not _compat.is_string(url):
                raise TypeError('expected url with string type, received %s' % type(url))
            separator = URL_SEPARATOR
            url_steps = url.split(separator)
            if not url_steps:
                return
            len_url_steps = len(url_steps)
            root_name = url_steps[0]
            root_folder = self.get_item(root_name)
            if len_url_steps == 1:
                if root_folder:
                    return root_folder
                else:
                    return

            if root_folder:
                if len_url_steps == 2 and not url_steps[1]:
                    return root_folder
                new_url = URL_SEPARATOR.join(url_steps[1:len_url_steps])
                return root_folder.get_url_item(new_url)
            return

    def add_item(self, item):
        if not isinstance(item, Folder):
            raise TypeError('Root folder must be a an instance of Folder, received %s' % type(item))
        name = item.name
        if name in self.__root:
            raise RootAlreadyExistError('Root folder with name:"%s" already exist' % name)
        if item.parent:
            raise AttributeError('Root folder must have no parent')
        if self.validator and not validate_item(item, self.validator):
            raise ValidatorRefusedError('Root folder %s - refused by folders validator' % type(item))
        self.__root[name] = item
        return True

    def get_item(self, name):
        if name in self.__root:
            return self.__root[name]
        else:
            return

    def list_items(self):
        return list(self.__root)

    def delete_item(self, name):
        item = self.get_item(name)
        if item:
            del self.__root[name]
            return item
        else:
            return

    def has_item(self, name):
        if name in self.__root:
            return True
        return False

    def __contains__(self, name):
        return self.has_item(name)

    def __iter__(self):
        return iter(self.__root.values())

    def has_items(self):
        if self.__root:
            return True
        return False

    def rename_item(self, name, new_name):
        item = self.get_item(name)
        if not item:
            raise RootDoNotExistError('Root folder with name:"%s" do not exist' % name)
        del self.__root[name]
        try:
            item.name = new_name
        except Exception as exp:
            log_debug(exp.message, 'RootFolders')
            self.__root[item.name] = item
            raise exp

        self.__root[item.name] = item

    def check_names(self):
        """ return the folders names that do not correspond items names
        that mean they where modified internally
        """
        p_names = []
        for name in self.list_items():
            if name != self.get_item(name).name:
                p_names.append(name)

        return p_names

    def repair_names(self):
        """ return the folders names that do not correspond items names
        that mean they where modified internally
        """
        p_names = self.check_names()
        for name in p_names:
            item = self.get_item(name)
            item.name = name

        return True