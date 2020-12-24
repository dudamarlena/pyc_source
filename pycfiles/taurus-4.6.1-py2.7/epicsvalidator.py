# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/epics/epicsvalidator.py
# Compiled at: 2019-08-19 15:09:29
"""
Epics module. See __init__.py for more detailed documentation
"""
__all__ = [
 'EpicsAuthorityNameValidator', 'EpicsDeviceNameValidator',
 'EpicsAttributeNameValidator']
import re
from taurus.core.taurusvalidator import TaurusAttributeNameValidator, TaurusDeviceNameValidator, TaurusAuthorityNameValidator
PV_CHARS = '[a-zA-Z0-9_\\-:;\\<\\>' + '[\\.\\[\\]]'

class EpicsAuthorityNameValidator(TaurusAuthorityNameValidator):
    """Validator for Epics authority names. For now, the only supported
    authority is "//":
    """
    scheme = '(ca|epics)'
    authority = '//'
    path = '(?!)'
    query = '(?!)'
    fragment = '(?!)'

    def getNames(self, fullname, factory=None):
        if self.isValid(fullname):
            return ('ca://', '//', '')
        else:
            return


class EpicsDeviceNameValidator(TaurusDeviceNameValidator):
    """Validator for Epics device names. Apart from the standard named
    groups (scheme, authority, path, query and fragment), the following named
    groups are created:

     - devname: device name (only empty string allowed for now)

    Note: brackets on the group name indicate that this group will only contain
    a string if the URI contains it.
    """
    scheme = '(ca|epics)'
    authority = EpicsAuthorityNameValidator.authority
    path = '/(?P<devname>)'
    query = '(?!)'
    fragment = '(?!)'

    def getNames(self, fullname, factory=None):
        if self.isValid(fullname):
            return ('ca:', '', '')
        else:
            return


class EpicsAttributeNameValidator(TaurusAttributeNameValidator):
    """Validator for Epics attribute names. Apart from the standard named
    groups (scheme, authority, path, query and fragment), the following named
    groups are created:

     - attrname: attribute name (an epics PV name).

    Note: brackets on the group name indicate that this group will only contain
    a value if the URI contains it.
    """
    scheme = '(ca|epics)'
    authority = EpicsAuthorityNameValidator.authority
    path = '(?P<attrname>%s+?(\\.(?P<_field>[A-Z]+))?)' % PV_CHARS
    query = '(?!)'
    fragment = '[^# ]*'

    def getNames(self, fullname, factory=None, fragment=False):
        """reimplemented from :class:`TaurusDeviceNameValidator`"""
        groups = self.getUriGroups(fullname)
        if groups is None:
            return
        else:
            complete = 'ca:%s' % groups['attrname']
            normal = groups['attrname']
            short = normal
            if fragment:
                key = groups.get('fragment', None)
                return (
                 complete, normal, short, key)
            return (
             complete, normal, short)