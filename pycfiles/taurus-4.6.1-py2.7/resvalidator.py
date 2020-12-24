# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/resource/resvalidator.py
# Compiled at: 2019-08-19 15:09:29
from builtins import object
from taurus.core import TaurusElementType
from taurus.core.taurusvalidator import TaurusAttributeNameValidator, TaurusDeviceNameValidator, TaurusAuthorityNameValidator
from taurus.core.taurushelper import getSchemeFromName, Factory
__all__ = [
 'ResourceAuthorityNameValidator', 'ResourceDeviceNameValidator',
 'ResourceAttributeNameValidator']
PY_VAR = '(?<![\\.a-zA-Z0-9_])[a-zA-Z_][a-zA-Z0-9_]*'

class _ResNameValidator(object):
    """
    Abstract class for all Res validators. Res Name validators should inherit
    first from it and then from the TaurusXXXNameValidator to give its methods
    highest precedence according to the python MRO
    """
    scheme = 'res'
    authority = '(?!)'
    path = '(?P<_resname>%s)' % PY_VAR
    query = '(?!)'
    fragment = '(?!)'
    pattern = '^(?P<scheme>%(scheme)s):' + '((?P<authority>%(authority)s)(?=/))?' + '(?P<path>%(path)s)' + '(\\?(?P<query>%(query)s))?' + '(#(?P<fragment>%(fragment)s))?$'
    _elementType = None

    def _getValueValidator(self, name):
        """Return the name validator for the mapped model name scheme

        :param name: (str) resource name
        :return: A specific TaurusValidator
        """
        scheme = getSchemeFromName(name)
        f = Factory(scheme)
        if self._elementType == TaurusElementType.Attribute:
            return f.getAttributeNameValidator()
        if self._elementType == TaurusElementType.Device:
            return f.getDeviceNameValidator()
        if self._elementType == TaurusElementType.Authority:
            return f.getAuthorityNameValidator()
        msg = '_elementType must be one of (Authority, Device, Attribute)'
        raise Exception(msg)

    def _getKey(self, name):
        if self._elementType == TaurusElementType.Attribute:
            g = TaurusAttributeNameValidator.getUriGroups(self, name)
        elif self._elementType == TaurusElementType.Device:
            g = TaurusDeviceNameValidator.getUriGroups(self, name)
        elif self._elementType == TaurusElementType.Authority:
            g = TaurusAuthorityNameValidator.getUriGroups(self, name)
        else:
            msg = '_elementType must be one of (Authority, Device, Attribute)'
            raise Exception(msg)
        if g is None:
            return
        else:
            return g['_resname']
            return

    def _getValue(self, key):
        return Factory('res').getValue(key)

    def isValid(self, name, *args, **kwargs):
        """Checks validity of the key (resname) and also of the value
        (model name)"""
        key = self._getKey(name)
        if key is None:
            return False
        else:
            value = self._getValue(key)
            if value is None:
                return False
            v = self._getValueValidator(value)
            return v.isValid(value, *args, **kwargs)

    def getUriGroups(self, name, *args, **kwargs):
        """Returns the groups for the value extended with '_resname'"""
        key = self._getKey(name)
        if key is None:
            return
        else:
            value = self._getValue(key)
            if value is None:
                return
            v = self._getValueValidator(value)
            ret = v.getUriGroups(value, *args, **kwargs)
            if ret is None:
                return
            ret['_resname'] = key
            return ret

    def getNames(self, name, *args, **kwargs):
        """Returns the names of the value"""
        key = self._getKey(name)
        if key is None:
            return
        else:
            value = self._getValue(key)
            if value is None:
                return
            return self._getValueValidator(value).getNames(value, *args, **kwargs)


class ResourceAuthorityNameValidator(_ResNameValidator, TaurusAuthorityNameValidator):
    """Validator for res authority names. Apart from the named related to the
    mapped model value, the following named groups are created:

     - _resname: resource name (aka key)
    """
    _elementType = TaurusElementType.Authority


class ResourceDeviceNameValidator(_ResNameValidator, TaurusDeviceNameValidator):
    """Validator for res device names. Apart from the named related to the
    mapped model value, the following named groups are created:

     - _resname: resource name (aka key)
    """
    _elementType = TaurusElementType.Device


class ResourceAttributeNameValidator(_ResNameValidator, TaurusAttributeNameValidator):
    """Validator for res attribute names. Apart from the named related to the
    mapped model value, the following named groups are created:

     - _resname: resource name (aka key)
    """
    _elementType = TaurusElementType.Attribute