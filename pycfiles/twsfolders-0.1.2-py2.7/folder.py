# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/folder.py
# Compiled at: 2014-07-10 04:23:35
from zope.interface import implementer
from zope.interface.interface import InterfaceClass
from BTrees.OOBTree import OOBTree
from BTrees.Length import Length
import item as folderitem
Item = folderitem.Item
from interface import IFolder
from _logger import log_debug

class ErrorAlreadyExist(Exception):
    """ tem already exist."""
    pass


class ErrorDoNotExist(Exception):
    """item do not exist."""
    pass


class ErrorDeleteNotAllowed(Exception):
    """Delete not allowed."""
    pass


class ErrorMoveNotAllowed(Exception):
    """Delete not allowed."""
    pass


class ErrorItemNotDeleteAble(Exception):
    """item is not delete-able."""
    pass


class ErrorAddItemNotAllowed(Exception):
    """item not allowed to be added."""
    pass


@implementer(IFolder)
class Folder(Item):
    key_type = 'string'

    def __init__(self, parent=None, name=None, title=None, description=None, **kwargs):
        super(Folder, self).__init__(parent=parent, name=name, title=title, description=description, **kwargs)
        self.__items = OOBTree()
        self.__items_len = Length()

    @property
    def is_folder(self):
        return True

    def allow_delete_item(self, name):
        return True

    def _item_attach(self, item):
        """
        internal method to attach item to this folder items collection
        @param item: Item
        @return: boolean
        """
        if isinstance(item, Item) and item.parent is None:
            self.__items[item.name] = item
            item_attached = item.inform_parent_attached(self)
            if item_attached:
                self.__items_len.change(1)
                return True
            del self.__items[item.name]
            return False
        return False

    def _item_detach(self, item):
        """
        internal method to detach item from this folder items collection
        @param item: Item
        @return: boolean
        """
        if isinstance(item, Item) and item.parent == self:
            del self.__items[item.name]
            item_detached = item.inform_parent_detached()
            if item_detached:
                self.__items_len.change(-1)
                return True
            self.__items[item.name] = item
            return False
        return False

    def allow_add_item(self, item, overwrite=False, raise_err=False):
        """
        Check whether i can add item to this folder items collection
        @param item: Item , any object instance of Item
        @param overwrite: boolean , whether i have to overwrite any existing item with item.name
        @param raise_err: boolean , whether i have to raise Exception in case of not acceptance
        @return: boolean
        """
        log_context = 'allow_add_item'
        if not isinstance(item, Item):
            message = 'expected type: Item received: %s' % type(item)
            if raise_err:
                raise TypeError(message)
            else:
                log_debug(message, log_context)
            return False
        item_name = item.name
        existing_item = self.get_item(item_name)
        if existing_item:
            if not overwrite:
                message = 'item: %s already exist' % item_name
                if raise_err:
                    raise ErrorAlreadyExist(message)
                else:
                    log_debug(message, log_context)
                return False
            if not self.allow_delete_item(item_name):
                message = 'folder "%s" do not allow item:"%s" to be deleted' % (self, item.name)
                if raise_err:
                    raise ErrorDeleteNotAllowed(message)
                else:
                    log_debug(message, log_context)
                return False
            if not existing_item.allow_delete:
                if raise_err:
                    raise ErrorItemNotDeleteAble('old item:"%s" is not delete-able' % item.name)
                else:
                    log_debug('old item:"%s" is not delete-able' % item.name, log_context)
                return False
        return True

    def add_item(self, item, overwrite=False):
        """
        Add item to this folder items collection
        @param item: Item, any object instance of Item
        @param overwrite: boolean, whether i have to overwrite any existing item
        @return: boolean
        """
        if self.allow_add_item(item, overwrite=overwrite, raise_err=True):
            item_name = item.name
            if self.has_item(item_name):
                old_item = self.get_item(item_name)
                self._item_detach(old_item)
            if self.__items is None:
                self.__items = OOBTree()
            self._item_attach(item)
            self.mark_changed()
            return True
        else:
            return

    def has_item(self, name):
        """
        Check whether this folder has item by this name
        @param name: str
        @return: boolean
        """
        if name in self.__items:
            return True
        else:
            return False

    def has_items(self):
        """
        check whether the folder has any item
        @return: boolean
        """
        if self.__items_len():
            return True
        return False

    def __contains__(self, name):
        """
        the same as has_item , in this form we can check by form
        if name in folder:
            # do some things
        or

         if name not in folder:
             # do some things

        @param name: string
        @return: boolean
        """
        return self.has_item(name)

    def __iter__(self):
        return iter(self.get_items())

    def get_item(self, name):
        """
        Return the item associated with this name in this folder collection if exist
        if not exist return None
        :param name: string
        @return: Item
        """
        item = self.__items.get(name, None)
        if item is None:
            log_debug('item %s do not exist' % name, 'get_item')
        return item

    def delete_item(self, name):
        """

        @param name: str
        @return: Item
        """
        if self.has_item(name):
            if not self.allow_delete_item(name):
                raise ErrorDeleteNotAllowed('folder "%s" do not allow item:"%s" to be deleted' % (self, name))
            item = self.get_item(name)
            if not item.allow_delete():
                raise ErrorItemNotDeleteAble('item:"%s" do not allow to be deleted' % name)
            self._item_detach(item)
            self.mark_changed()
            return item
        else:
            return

    def delete_items(self, names):
        if not isinstance(names, list):
            raise TypeError('expected list get type %s' % type(names))
        deleted_items = []
        names_not_deleted = []
        for name in names:
            if name not in deleted_items and name not in names_not_deleted:
                try:
                    item = self.delete_item(name)
                except Exception as exp:
                    log_debug(exp.message, 'delete_items')
                    item = None

                if item:
                    deleted_items.append(item)
                else:
                    names_not_deleted.append(name)

        return (
         deleted_items, names_not_deleted)

    def rename_item(self, name, new_name):
        item = self.get_item(name)
        if not item:
            raise ErrorDoNotExist('item:%s do not exist' % name)
        if self.has_item(new_name):
            raise ErrorAlreadyExist('item %s already exist' % new_name)
        self._item_detach(item)
        try:
            item.name = new_name
        except Exception as exp:
            log_debug(str(exp))
            self._item_attach(item)
            raise exp
        else:
            self._item_attach(item)
            self.mark_changed()
            return True

    def move_item(self, name, target_folder):
        if not isinstance(target_folder, Folder):
            raise AssertionError
            item = self.get_item(name)
            if not item:
                raise ErrorDoNotExist()
            if item == target_folder:
                raise Exception('can not move item:"%s" to it self' % name)
            if isinstance(item, Folder) and target_folder.is_folder_in_parents(item):
                raise Exception('target_folder %s is in the hierarchy (is one of the parents) of "%s"' % (target_folder,
                 name))
            if target_folder.has_item(name):
                raise ErrorAlreadyExist()
            if not item.allow_move(target_folder):
                raise ErrorMoveNotAllowed('item:"%s" not allowed to move to folder:"%s"' % (name, target_folder.url()))
            raise (target_folder.allow_add_item(item) or ErrorAddItemNotAllowed)('target folder:"%s" do not allow item to be added' % target_folder)
        self._item_detach(item)
        try:
            target_folder.add_item(item)
        except Exception as exp:
            self._item_attach(item)
            raise exp
        else:
            self.mark_changed()
            return True

    def list_items(self, **kwargs):
        if self.__items is None:
            return []
        else:
            items_list = list(self.__items)

            def filter_validator_interface(name, interface_validator):
                item = self.get_item(name)
                if interface_validator.providedBy(item):
                    return True
                else:
                    return False

            def filter_validator_caller(name, caller_validator):
                item = self.get_item(name)
                if caller_validator(item):
                    return True
                else:
                    return False

            validator = kwargs.get('validator', None)
            if validator:
                if isinstance(validator, InterfaceClass):
                    items_list = filter(filter_validator_interface, items_list)
                elif callable(validator):
                    items_list = filter(filter_validator_caller, items_list)
                else:
                    raise TypeError('validator must be Interface or callable')
            return items_list

    def get_items(self, **kwargs):
        items = []
        for key, item in self.__items.iteritems():
            items.append(item)

        def filter_validator_interface(v_item, interface_validator):
            if interface_validator.provided_by(v_item):
                return True
            else:
                return False

        def filter_validator_caller(v_item, caller_validator):
            if caller_validator(v_item):
                return True
            else:
                return False

        validator = kwargs.get('validator', None)
        if validator:
            if isinstance(validator, InterfaceClass):
                items = filter(filter_validator_interface, items)
            elif callable(validator):
                items = filter(filter_validator_caller, items)
            else:
                raise TypeError('validator must be Interface or callable')
        return items

    def len_items(self):
        return self.__items_len()