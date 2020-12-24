# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/pyrpl_utils.py
# Compiled at: 2017-08-29 09:44:06
import time
from timeit import default_timer
import logging
logger = logging.getLogger(__file__)
from collections import OrderedDict, Counter

def isnotebook():
    """ returns True if Jupyter notebook is runnung """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        if shell == 'TerminalInteractiveShell':
            return False
        return False
    except NameError:
        return False


def time():
    """ returns the time. used instead of time.time for rapid portability"""
    return default_timer()


def get_unique_name_list_from_class_list(cls_list):
    """
    returns a list of names using cls.name if unique or cls.name1, cls.name2... otherwise.
    Order of the name list matches order of cls_list, such that iterating over zip(cls_list, name_list) is OK
    """
    all_names = [ cls.__name__.lower() for cls in cls_list ]
    final_names = []
    for name in all_names:
        occurences = all_names.count(name)
        if occurences == 1:
            final_names.append(name)
        else:
            for i in range(occurences):
                if name + str(i) not in final_names:
                    final_names.append(name + str(i))
                    break

    return final_names


def get_class_name_from_module_name(module_name):
    """ returns the class name corresponding to a module_name """
    return module_name[0].upper() + module_name[1:].rstrip('1234567890')


def get_base_module_class(module):
    """ returns the base class of module that has the same name as module """
    base_module_class_name = get_class_name_from_module_name(module.name)
    for base_module_class in type(module).__mro__:
        if base_module_class.__name__ == base_module_class_name:
            return base_module_class


def all_subclasses(cls):
    """ returns a list of all subclasses of cls """
    return cls.__subclasses__() + [ g for s in cls.__subclasses__() for g in all_subclasses(s)
                                  ]


def recursive_getattr(root, path):
    """ returns root.path (i.e. root.attr1.attr2) """
    attribute = root
    for name in path.split('.'):
        if name != '':
            attribute = getattr(attribute, name)

    return attribute


def recursive_setattr(root, path, value):
    """ returns root.path = value (i.e. root.attr1.attr2 = value) """
    attribute = root
    names = path.split('.')
    for name in names[:-1]:
        attribute = getattr(attribute, name)

    setattr(attribute, names[(-1)], value)


def setloglevel(level='info', loggername='pyrpl'):
    """ sets the log level to the one specified in config file"""
    try:
        loglevels = {'notset': logging.NOTSET, 'debug': logging.DEBUG, 
           'info': logging.INFO, 
           'warning': logging.WARNING, 
           'error': logging.ERROR, 
           'critical': logging.CRITICAL}
        level = loglevels[level]
    except:
        pass
    else:
        logging.getLogger(name=loggername).setLevel(level)


class DuplicateFilter(logging.Filter):
    """
    Prevent multiple repeated logging message from polluting the console
    """

    def filter(self, record):
        current_log = (
         record.module, record.levelno, record.msg)
        if current_log != getattr(self, 'last_log', None):
            self.last_log = current_log
            return True
        else:
            return False


def sorted_dict(dict_to_sort=None, sort_by_values=True, **kwargs):
    if dict_to_sort is None:
        dict_to_sort = kwargs
    if not sort_by_values:
        return OrderedDict(sorted(dict_to_sort.items()))
    else:
        return OrderedDict(sorted(dict_to_sort.items(), key=lambda x: x[1]))
        return


def update_with_typeconversion(dictionary, update):
    for k, v in update.items():
        if k in dictionary:
            v = type(dictionary[k])(v)
        dictionary[k] = v

    return dictionary


def unique_list(nonunique_list):
    """ Returns a list where each element of nonunique_list occurs exactly once.
    The last occurence of an element defines its position in the returned list.
    """
    unique_list = []
    for attr in reversed(nonunique_list):
        if attr not in unique_list:
            unique_list.insert(0, attr)

    return unique_list


class Bijection(dict):
    """ This class defines a bijection object based on dict

    It can be used exactly like dict, but additionally has a property
    'inverse' which contains the inverted {value: key} dict. """

    def __init__(self, *args, **kwargs):
        super(Bijection, self).__init__(*args, **kwargs)
        self.inverse = {v:k for k, v in self.items()}

    def __setitem__(self, key, value):
        super(Bijection, self).__setitem__(key, value)
        self.inverse[value] = key

    def __delitem__(self, key):
        self.inverse.__delitem__(self.__getitem__(key))
        super(Bijection, self).__delitem__(key)

    def pop(self, key):
        self.inverse.pop(self.__getitem__(key))
        super(Bijection, self).pop(key)

    def update(self, *args, **kwargs):
        super(Bijection, self).update(*args, **kwargs)
        self.inverse = {v:k for k, v in self.items()}