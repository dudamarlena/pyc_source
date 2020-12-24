# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/evalfactory.py
# Compiled at: 2019-08-19 15:09:29
"""
evaluation module. See __init__.py for more detailed documentation
"""
from __future__ import absolute_import
import weakref
from taurus.core.taurusbasetypes import TaurusElementType
from .evalattribute import EvaluationAttribute
from .evalauthority import EvaluationAuthority
from .evaldevice import EvaluationDevice
from taurus.core.taurusexception import TaurusException, DoubleRegistration
from taurus.core.util.log import Logger
from taurus.core.util.singleton import Singleton
from taurus.core.taurusfactory import TaurusFactory
__all__ = [
 'EvaluationFactory']

class EvaluationFactory(Singleton, TaurusFactory, Logger):
    """
    A Singleton class that provides Evaluation related objects.
    """
    elementTypesMap = {TaurusElementType.Authority: EvaluationAuthority, TaurusElementType.Device: EvaluationDevice, 
       TaurusElementType.Attribute: EvaluationAttribute}
    schemes = ('eval', 'evaluation')
    DEFAULT_DEVICE = '@DefaultEvaluator'
    DEFAULT_AUTHORITY = '//localhost'
    DEFAULT_DATABASE = '_DefaultEvalDB'

    def __init__(self):
        """ Initialization. Nothing to be done here for now."""
        pass

    def init(self, *args, **kwargs):
        """Singleton instance initialization."""
        name = self.__class__.__name__
        self.call__init__(Logger, name)
        self.call__init__(TaurusFactory)
        self.eval_attrs = weakref.WeakValueDictionary()
        self.eval_devs = weakref.WeakValueDictionary()
        self.eval_configs = weakref.WeakValueDictionary()
        self.scheme = 'eval'

    def findObjectClass(self, absolute_name):
        """Operation models are always OperationAttributes
        """
        if EvaluationDevice.isValid(absolute_name):
            return EvaluationDevice
        else:
            if EvaluationAttribute.isValid(absolute_name):
                return EvaluationAttribute
            else:
                self.debug('Not able to find Object class for %s' % absolute_name)
                self.traceback()
                return

            return

    def getAuthority(self, name=None):
        """Obtain the EvaluationDatabase object.

        :param db_name: (str) this is ignored because only one database is supported

        :return: (EvaluationDatabase)
        """
        if name is None:
            name = 'eval://localhost'
        v = self.getAuthorityNameValidator()
        if not v.isValid(name):
            raise TaurusException('Invalid Evaluation authority name %s' % name)
        if not hasattr(self, '_auth'):
            self._auth = EvaluationAuthority(self.DEFAULT_AUTHORITY)
        return self._auth

    def getDevice(self, dev_name):
        """Obtain the object corresponding to the given device name. If the
        corresponding device already exists, the existing instance is returned.
        Otherwise a new instance is stored and returned.

        :param dev_name: (str) the device name string. See
                         :mod:`taurus.core.evaluation` for valid device names

        :return: (EvaluationDevice)

        @throws TaurusException if the given name is invalid.
        """
        d = self.eval_devs.get(dev_name, None)
        if d is None:
            validator = self.getDeviceNameValidator()
            names = validator.getNames(dev_name)
            if names is None:
                raise TaurusException('Invalid evaluator device name %s' % dev_name)
            fullname, normalname, devname = names
            d = self.eval_devs.get(fullname, None)
            if d is None:
                groups = validator.getUriGroups(dev_name)
                DevClass = EvaluationDevice
                _safedict = {}
                if groups['_evaldotname'] is not None:
                    modulename = groups.get('_evalmodname')
                    classname = groups.get('_evalclassname')
                    classargs = groups.get('_evalclassparenths')
                    try:
                        import importlib
                        m = importlib.import_module(modulename)
                    except:
                        self.warning('Problem importing "%s"' % modulename)
                        raise

                    if classname == '*':
                        for key in dir(m):
                            _safedict[key] = getattr(m, key)

                    else:
                        klass = getattr(m, classname)
                        if classargs:
                            from taurus.core.util.parse_args import parse_args
                            a, kw = parse_args(classargs, strip_pars=True)
                            instancename = groups.get('_evalinstname') or 'self'
                            instance = klass(*a, **kw)
                            _safedict[instancename] = instance
                        else:
                            DevClass = klass
                auth_name = groups.get('authority') or self.DEFAULT_AUTHORITY
                authority = self.getAuthority(auth_name)
                d = DevClass(fullname, parent=authority, storeCallback=self._storeDev)
                d.addSafe(_safedict, permanent=True)
        return d

    def getAttribute(self, attr_name, **kwargs):
        """Obtain the object corresponding to the given attribute name. If the
        corresponding attribute already exists, the existing instance is
        returned. Otherwise a new instance is stored and returned. The evaluator
        device associated to this attribute will also be created if necessary.

        :param attr_name: (str) the attribute name string. See
                          :mod:`taurus.core.evaluation` for valid attribute
                          names

        Any aditional keyword arguments will be passed directly to the
        constructor of `:class:EvaluationAttribute`

        :return: (EvaluationAttribute)

        @throws TaurusException if the given name is invalid.
        """
        a = self.eval_attrs.get(attr_name, None)
        if a is None:
            validator = self.getAttributeNameValidator()
            names = validator.getNames(attr_name)
            if names is None or names[0] is None:
                raise TaurusException('Invalid evaluation attribute name %s' % attr_name)
            fullname = names[0]
            a = self.eval_attrs.get(fullname, None)
            if a is None:
                dev = self.getDevice(validator.getDeviceName(attr_name))
                kwargs['storeCallback'] = self._storeAttr
                if 'pollingPeriod' not in kwargs:
                    kwargs['pollingPeriod'] = self.getDefaultPollingPeriod()
                a = EvaluationAttribute(fullname, parent=dev, **kwargs)
        return a

    def _storeDev(self, dev):
        name = dev.getFullName()
        exists = self.eval_devs.get(name)
        if exists is not None:
            if exists == dev:
                self.debug('%s has already been registered before' % name)
                raise DoubleRegistration
            else:
                self.debug('%s has already been registered before with a different object!' % name)
                raise DoubleRegistration
        self.eval_devs[name] = dev
        return

    def _storeAttr(self, attr):
        name = attr.getFullName()
        exists = self.eval_attrs.get(name)
        if exists is not None:
            if exists == attr:
                self.debug('%s has already been registered before' % name)
                raise DoubleRegistration
            else:
                self.debug('%s has already been registered before with a different object!' % name)
                raise DoubleRegistration
        self.eval_attrs[name] = attr
        return

    def _storeConfig(self, fullname, config):
        name = fullname
        exists = self.eval_configs.get(name)
        if exists is not None:
            if exists == config:
                self.debug('%s has already been registered before' % name)
                raise DoubleRegistration
            else:
                self.debug('%s has already been registered before with a different object!' % name)
                raise DoubleRegistration
        self.eval_configs[name] = config
        return

    def getAuthorityNameValidator(self):
        """Return EvaluationAuthorityNameValidator"""
        from . import evalvalidator
        return evalvalidator.EvaluationAuthorityNameValidator()

    def getDeviceNameValidator(self):
        """Return EvaluationDeviceNameValidator"""
        from . import evalvalidator
        return evalvalidator.EvaluationDeviceNameValidator()

    def getAttributeNameValidator(self):
        """Return EvaluationAttributeNameValidator"""
        from . import evalvalidator
        return evalvalidator.EvaluationAttributeNameValidator()