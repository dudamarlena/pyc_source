# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/resource/resfactory.py
# Compiled at: 2019-08-19 15:09:29
"""
resfactory.py:
"""
from __future__ import absolute_import
from future.utils import string_types
import os, imp, collections
from taurus.core.taurushelper import Manager
from taurus.core.util.singleton import Singleton
from taurus.core.util.log import Logger
from taurus.core.taurusfactory import TaurusFactory
from taurus.core.taurusexception import TaurusException

class ResourcesFactory(Singleton, TaurusFactory, Logger):
    """A Singleton class designed to provide Simulation related objects."""
    schemes = ('res', 'resource')
    DftResourceName = 'taurus_resources.py'
    DftResourcePriority = 10

    def __init__(self):
        """ Initialization. Nothing to be done here for now."""
        pass

    def init(self, *args, **kwargs):
        """Singleton instance initialization.
           **For internal usage only**"""
        name = self.__class__.__name__
        self.call__init__(Logger, name)
        self.call__init__(TaurusFactory)
        self.clear()

    def clear(self):
        self._resource_map = {}
        self._resource_priority = {}
        self._resource_priority_keys = []
        self._resource_count = 0

    def reloadResource(self, obj=None, priority=1, name=None):
        """(Re)Loads the given resource.

           :param obj: (dict or file or None) the resource object. Default is
                       None meaning in will (re)load the default resource:
                       taurus_resources.py from the application directory
           :param priority: (int) the resource priority. Default is 1 meaning
                            maximum priority
           :param name: (str) an optional name to give to the resource

           :return: (dict) a dictionary version of the given resource object
        """
        if priority < 1:
            raise ValueError('priority must be >=1')
        if isinstance(obj, collections.Mapping):
            name = name or 'DICT%02d' % priority
        elif type(obj) in (str,) or obj is None:
            name, mod = self.__reloadResource(obj)
            obj = {}
            for k, v in mod.__dict__.items():
                if not k.startswith('_') and isinstance(v, string_types):
                    obj[k] = v

        else:
            raise TypeError
        if self._resource_map.get(name) is None:
            self._resource_count += 1
        self._resource_map[name] = obj
        if self._resource_count == 1:
            self._first_resource = obj
        pl = self._resource_priority.get(priority)
        if pl is None:
            self._resource_priority[priority] = pl = []
        pl.append(name)
        self._resource_priority_keys = list(self._resource_priority.keys())
        self._resource_priority_keys.sort()
        return obj

    loadResource = reloadResource
    loadResource.__doc__ = reloadResource.__doc__

    def __reloadResource(self, name=None):
        path = os.path.curdir
        if name is None:
            file_name = ResourcesFactory.DftResourceName
        else:
            path, file_name = os.path.split(name)
            if not path:
                path = os.path.curdir
            path = os.path.abspath(path)
            full_name = os.path.join(path, file_name)
            if not os.path.isfile(full_name):
                raise ImportError
            module_name, ext = os.path.splitext(file_name)
            m, file_ = (None, None)
            try:
                file_, pathname, desc = imp.find_module(module_name, [path])
                self.info('(re)loading resource %s', pathname)
                m = imp.load_module(module_name, file_, pathname, desc)
                if file_:
                    file_.close()
            except Exception as e:
                if file_:
                    file_.close()
                raise e

        if m is None:
            self.warning('failed to (re)load resource %s' % module_name)
            raise ImportError
        return (full_name, m)

    def getValue(self, key):
        """Returns the value for a given key

           :param key: (str) a key

           :return: (str) the value for the given key
        """
        if self._resource_count == 0:
            try:
                self.reloadResource(priority=self.DftResourcePriority)
            except:
                return

        if self._resource_count == 1:
            return self._first_resource.get(key, None)
        else:
            for p in self._resource_priority_keys:
                for resource_name in self._resource_priority[p]:
                    resource = self._resource_map[resource_name]
                    try:
                        return resource[key]
                    except:
                        pass

            return

    def findObjectClass(self, absolute_name):
        """
        Obtain the class object corresponding to the given name.

        :param absolute_name: (str) the object absolute name string

        :return: (taurus.core.taurusmodel.TaurusModel or None) the class
                 for the model object mapped by absolute_name, or None if
                 absolute_name is invalid.
        """
        validators = (
         self.getAttributeNameValidator(),
         self.getDeviceNameValidator(),
         self.getAuthorityNameValidator())
        for v in validators:
            try:
                value = self.getValue(v.getUriGroups(absolute_name)['_resname'])
                return Manager().findObjectClass(value)
            except:
                pass

        return

    def getAuthority(self, name=None):
        """
        Obtain the authority model object referenced by name.

        :param name: (str) name

        :return: (taurus.core.taurusauthority.TaurusAuthority) authority object
        :raise: (taurus.core.taurusexception.TaurusException) if name is invalid
        """
        groups = self.getAuthorityNameValidator().getUriGroups(name)
        if groups is None:
            raise TaurusException('Invalid name "%s"' % name)
        res_name = groups['_resname']
        value = self.getValue(res_name)
        return Manager().getAuthority(value)

    def getDevice(self, name):
        """
        Obtain the device model object referenced by name.

        :param name: (str) name

        :return: (taurus.core.taurusdevice.TaurusDevice) device object
        :raise: (taurus.core.taurusexception.TaurusException) if name is invalid
        """
        groups = self.getDeviceNameValidator().getUriGroups(name)
        if groups is None:
            raise TaurusException('Invalid name "%s"' % name)
        res_name = groups['_resname']
        value = self.getValue(res_name)
        return Manager().getDevice(value)

    def getAttribute(self, name):
        """
        Obtain the attribute model object referenced by name.

        :param name: (str) name

        :return: (taurus.core.taurusattribute.TaurusAttribute) attribute object
        :raise: (taurus.core.taurusexception.TaurusException) if name is invalid
        """
        groups = self.getAttributeNameValidator().getUriGroups(name)
        if groups is None:
            raise TaurusException('Invalid name "%s"' % name)
        res_name = groups['_resname']
        value = self.getValue(res_name)
        return Manager().getAttribute(value)

    def getAuthorityNameValidator(self):
        """Return ResourceAuthorityNameValidator"""
        from . import resvalidator
        return resvalidator.ResourceAuthorityNameValidator()

    def getDeviceNameValidator(self):
        """Return ResourceDeviceNameValidator"""
        from . import resvalidator
        return resvalidator.ResourceDeviceNameValidator()

    def getAttributeNameValidator(self):
        """Return ResourceAttributeNameValidator"""
        from . import resvalidator
        return resvalidator.ResourceAttributeNameValidator()