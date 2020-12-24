# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/prefixes.py
# Compiled at: 2014-07-07 10:35:55
from zope.interface.interface import InterfaceClass
from interface import IItem
import _compat
from _logger import log_debug
URL_SEPARATOR = '/'
_registry = {}

def is_interface(validator):
    return isinstance(validator, InterfaceClass)


class _Prefix(object):

    def __init__(self, name, validator, getter):
        self.name = name
        self.validator = validator
        self.getter = getter

    @staticmethod
    def get_parent_by_validator(item, validator, **kwargs):
        log_debug('get parent from item: %s by validator:  %s ' % (item, validator), 'get_parent_by_validator')
        if not IItem.providedBy(item):
            raise Exception('item do provide IItem')
        parent_item = item
        while parent_item:
            log_debug(' ... look parent_item: %s ' % parent_item, 'get_parent_by_validator')
            if validate_item(parent_item, validator, **kwargs):
                log_debug(' ... parent_item validated by interface: %s' % parent_item, 'get_parent_by_validator')
                break
            parent_item = parent_item.parent

        log_debug('return: %s' % parent_item, 'get_parent_by_validator')
        return parent_item

    def get_parent(self, item, **kwargs):
        if self.getter:
            return self.getter(item, **kwargs)
        if self.validator:
            return self.get_parent_by_validator(item, self.validator, **kwargs)

    def validate(self, item, **kwargs):
        if self.validator:
            if is_interface(self.validator):
                return self.validator.providedBy(item)
            else:
                return self.validator(item, **kwargs)

        return False


def register(prefix_name, validator=None, getter=None):
    global _registry
    if not isinstance(prefix_name, _compat.string_types):
        raise TypeError('prefix name must be a string')
    if validator is not None and not is_interface(validator) and not callable(validator):
        raise TypeError('validator must be interface or callable')
    if not validator and not callable(getter):
        raise TypeError('getter must be callable, if no validator ')
    _registry[prefix_name] = _Prefix(prefix_name, validator, getter)
    return


def get_parent(prefix, item, **kwargs):
    pr = _registry.get(prefix, None)
    if pr:
        return pr.get_parent(item, **kwargs)
    else:
        return


def validate_item(item, validator, **kwargs):
    if is_interface(validator) and validator.providedBy(item) or not is_interface(validator) and callable(validator) and validator(item, **kwargs):
        return True
    return False


def validate_item_by_prefix(prefix, item, **kwargs):
    pr = _registry.get(prefix, None)
    if pr:
        return pr.validate(item, **kwargs)
    else:
        return False


def has_prefix(prefix):
    if prefix in _registry:
        return True
    return False


def root_folder_validator(item, **kwargs):
    if item.parent is None:
        return True
    else:
        return False


def parent_folder_getter(item, **kwargs):
    """
    :param item: C{Item} , storage item or folder
    :return: C{Folder} the parent of item
    """
    return item.parent


def private_folder_getter(item, **kwargs):
    return item.private_folder


def sibling_parent_getter(item, **kwargs):
    """ return the the first item that contain next_item_name"""
    next_item_name = kwargs.get('next_item_name', None)
    if next_item_name is None:
        return
    else:
        parent_item = item.parent
        while parent_item:
            if next_item_name in parent_item:
                return parent_item
            parent_item = parent_item.parent

        return


def _init():
    register(URL_SEPARATOR, validator=root_folder_validator)
    register('..', getter=parent_folder_getter)
    register('~', getter=sibling_parent_getter)
    register('@', getter=private_folder_getter)


_init()