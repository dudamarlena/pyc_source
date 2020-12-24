# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/managers.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
import logging

class InstanceManager(object):

    def __init__(self, class_list=None, instances=True):
        if class_list is None:
            class_list = []
        self.instances = instances
        self.update(class_list)
        return

    def get_class_list(self):
        return self.class_list

    def add(self, class_path):
        self.cache = None
        self.class_list.append(class_path)
        return

    def remove(self, class_path):
        self.cache = None
        self.class_list.remove(class_path)
        return

    def update(self, class_list):
        """
        Updates the class list and wipes the cache.
        """
        self.cache = None
        self.class_list = class_list
        return

    def all(self):
        """
        Returns a list of cached instances.
        """
        class_list = list(self.get_class_list())
        if not class_list:
            self.cache = []
            return []
        else:
            if self.cache is not None:
                return self.cache
            results = []
            for cls_path in class_list:
                module_name, class_name = cls_path.rsplit('.', 1)
                try:
                    module = __import__(module_name, {}, {}, class_name)
                    cls = getattr(module, class_name)
                    if self.instances:
                        results.append(cls())
                    else:
                        results.append(cls)
                except Exception:
                    logger = logging.getLogger('sentry.errors')
                    logger.exception('Unable to import %s', cls_path)
                    continue

            self.cache = results
            return results