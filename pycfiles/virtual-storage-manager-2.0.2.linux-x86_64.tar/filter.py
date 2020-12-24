# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/scheduler/filter.py
# Compiled at: 2016-06-13 14:11:03
"""
Filter support
"""
import inspect
from stevedore import extension

class BaseFilter(object):
    """Base class for all filter classes."""

    def _filter_one(self, obj, filter_properties):
        """Return True if it passes the filter, False otherwise.
        Override this in a subclass.
        """
        return True

    def filter_all(self, filter_obj_list, filter_properties):
        """Yield objects that pass the filter.

        Can be overriden in a subclass, if you need to base filtering
        decisions on all objects.  Otherwise, one can just override
        _filter_one() to filter a single object.
        """
        for obj in filter_obj_list:
            if self._filter_one(obj, filter_properties):
                yield obj


class BaseFilterHandler(object):
    """ Base class to handle loading filter classes.

    This class should be subclassed where one needs to use filters.
    """

    def __init__(self, filter_class_type, filter_namespace):
        self.namespace = filter_namespace
        self.filter_class_type = filter_class_type
        self.filter_manager = extension.ExtensionManager(filter_namespace)

    def _is_correct_class(self, obj):
        """Return whether an object is a class of the correct type and
        is not prefixed with an underscore.
        """
        return inspect.isclass(obj) and not obj.__name__.startswith('_') and issubclass(obj, self.filter_class_type)

    def get_all_classes(self):
        return [ x.plugin for x in self.filter_manager if self._is_correct_class(x.plugin)
               ]

    def get_filtered_objects(self, filter_classes, objs, filter_properties):
        for filter_cls in filter_classes:
            objs = filter_cls().filter_all(objs, filter_properties)

        return list(objs)