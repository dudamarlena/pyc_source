# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/tangovalidator.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the base taurus name validator classes"""
__all__ = [
 'TangoAuthorityNameValidator', 'TangoDeviceNameValidator',
 'TangoAttributeNameValidator']
__docformat__ = 'restructuredtext'
import socket
from taurus.core.taurusvalidator import TaurusAttributeNameValidator, TaurusDeviceNameValidator, TaurusAuthorityNameValidator

class TangoAuthorityNameValidator(TaurusAuthorityNameValidator):
    """Validator for Tango authority names. Apart from the standard named
    groups (scheme, authority, path, query and fragment), the following named
    groups are created:

     - host: tango host name, without port.
     - port: port number
    """
    scheme = 'tango'
    authority = '//(?P<host>([\\w\\-_]+\\.)*[\\w\\-_]+):(?P<port>\\d{1,5})'
    path = '(?!)'
    query = '(?!)'
    fragment = '(?!)'

    def getUriGroups(self, name, strict=None):
        """Reimplementation of getUriGroups to fix the host and authority
        name using fully qualified domain name for the host.
        """
        ret = TaurusAuthorityNameValidator.getUriGroups(self, name, strict)
        if ret is not None:
            fqdn = socket.getfqdn(ret['host'])
            ret['host'] = fqdn
            ret['authority'] = ('//{host}:{port}').format(**ret)
        return ret


class TangoDeviceNameValidator(TaurusDeviceNameValidator):
    """Validator for Tango device names. Apart from the standard named
    groups (scheme, authority, path, query and fragment), the following named
    groups are created:

     - devname: device name (either alias or slashed name)
     - [_devalias]: device alias
     - [_devslashname]: device name in slashed (a/b/c) form
     - [host] as in :class:`TangoAuthorityNameValidator`
     - [port] as in :class:`TangoAuthorityNameValidator`

    Note: brackets on the group name indicate that this group will only contain
    a string if the URI contains it.
    """
    scheme = 'tango'
    authority = TangoAuthorityNameValidator.authority
    path = '/?(?P<devname>((?P<_devalias>[^/?#:]+)|' + '(?P<_devslashname>[^/?#:]+/[^/?#:]+/[^/?#:]+)))'
    query = '(?!)'
    fragment = '(?!)'

    def getUriGroups(self, name, strict=None):
        """Reimplementation of getUriGroups to fix the host and authority
        name using fully qualified domain name for the host.
        """
        ret = TaurusDeviceNameValidator.getUriGroups(self, name, strict)
        if ret is not None and ret.get('host', None) is not None:
            fqdn = socket.getfqdn(ret['host'])
            ret['host'] = fqdn
            ret['authority'] = ('//{host}:{port}').format(**ret)
        return ret

    def getNames(self, fullname, factory=None, queryAuth=True):
        """reimplemented from :class:`TaurusDeviceNameValidator`. It accepts an
        extra keyword arg `queryAuth` which, if set to False, will prevent the
        validator from trying to query a TaurusAuthority to obtain missing info
        such as the devslashname <--> devalias correspondence.
        """
        groups = self.getUriGroups(fullname)
        if groups is None:
            return
        default_authority = None
        if factory is None:
            from taurus import Factory
            factory = Factory(scheme=self.scheme)
        default_authority = factory.get_default_tango_host()
        if default_authority is None:
            import PyTango
            host, port = PyTango.ApiUtil.get_env_var('TANGO_HOST').split(':')
            host = socket.getfqdn(host)
            default_authority = ('//{0}:{1}').format(host, port)
        authority = groups.get('authority')
        if authority is None:
            groups['authority'] = authority = default_authority
        db = None
        if queryAuth:
            try:
                db = factory.getAuthority('tango:%s' % authority)
            except:
                pass

        _devalias = groups.get('_devalias')
        _devslashname = groups.get('_devslashname')
        if _devslashname is None and db is not None:
            _devslashname = db.getElementFullName(_devalias)
            groups['_devslashname'] = _devslashname
        if _devslashname is None:
            return (
             None, None, _devalias)
        else:
            complete = 'tango:%(authority)s/%(_devslashname)s' % groups
            if authority.lower() == default_authority.lower():
                normal = '%(_devslashname)s' % groups
            else:
                normal = '%(authority)s/%(_devslashname)s' % groups
            if _devalias is not None:
                short = _devalias
            elif db is not None:
                short = db.getElementAlias(_devslashname) or _devslashname
            else:
                short = _devslashname
            return (complete, normal, short)

    @property
    def nonStrictNamePattern(self):
        """In non-strict mode, allow double-slash even if there is no Authority.
        (e.g., "tango://a/b/c" passes this non-strict form)
        """
        pattern = '^((?P<scheme>%(scheme)s)://)?' + '((?P<authority>%(authority)s)(?=/))?' + '(?P<path>%(path)s)' + '(\\?(?P<query>%(query)s))?' + '(#%(fragment)s)?$'
        authority = '(?P<host>([\\w\\-_]+\\.)*[\\w\\-_]+):(?P<port>\\d{1,5})'
        path = '/?(?P<devname>((?P<_devalias>([^/?#:]+))|' + '(?P<_devslashname>[^/?#:]+/[^/?#:]+/[^/?#:]+)))'
        return pattern % dict(scheme=self.scheme, authority=authority, path=path, query='(?!)', fragment='(?!)')


class TangoAttributeNameValidator(TaurusAttributeNameValidator):
    """Validator for Tango attribute names. Apart from the standard named
    groups (scheme, authority, path, query and fragment), the following named
    groups are created:

     - attrname: attribute name including device name
     - _shortattrname: attribute name excluding device name
     - devname: as in :class:`TangoDeviceNameValidator`
     - [_devalias]: as in :class:`TangoDeviceNameValidator`
     - [_devslashname]: as in :class:`TangoDeviceNameValidator`
     - [host] as in :class:`TangoAuthorityNameValidator`
     - [port] as in :class:`TangoAuthorityNameValidator`
     - [cfgkey] same as fragment (for bck-compat use only)

    Note: brackets on the group name indicate that this group will only contain
    a string if the URI contains it.
    """
    scheme = 'tango'
    authority = TangoAuthorityNameValidator.authority
    path = '(?P<attrname>%s/(?P<_shortattrname>[^/?:#]+))' % TangoDeviceNameValidator.path
    query = '(?!)'
    fragment = '(?P<cfgkey>[^# ]*)'

    def getUriGroups(self, name, strict=None):
        """Reimplementation of getUriGroups to fix the host and authority
        name using fully qualified domain name for the host.
        """
        ret = TaurusAttributeNameValidator.getUriGroups(self, name, strict)
        if ret is not None and ret.get('host', None) is not None:
            fqdn = socket.getfqdn(ret['host'])
            ret['host'] = fqdn
            ret['authority'] = ('//{host}:{port}').format(**ret)
        return ret

    def getNames(self, fullname, factory=None, queryAuth=True, fragment=False):
        """Returns the complete and short names"""
        groups = self.getUriGroups(fullname)
        if groups is None:
            return
        else:
            complete, normal, short = None, None, groups.get('_shortattrname')
            devname = fullname.rsplit('#', 1)[0].rsplit('/', 1)[0]
            v = TangoDeviceNameValidator()
            devcomplete, devnormal, _ = v.getNames(devname, factory=factory, queryAuth=queryAuth)
            if devcomplete is not None:
                complete = '%s/%s' % (devcomplete, short)
            if devnormal is not None:
                normal = '%s/%s' % (devnormal, short)
            if fragment:
                key = groups.get('fragment', None)
                return (
                 complete, normal, short, key)
            return (complete, normal, short)

    @property
    def nonStrictNamePattern(self):
        """In non-strict mode, allow double-slash even if there is no Authority.
        Also allow old-style "?configuration[=cfgkey]" instead of fragment.
        If cfgkey is present, it is also stored in the "fragment" named group.
        For example, "tango://a/b/c/d?configuration=label" passes this
        non-strict form, and the named group "fragment" will contain "label"
        """
        pattern = '^((?P<scheme>%(scheme)s)://)?' + '((?P<authority>%(authority)s)(?=/))?' + '(?P<path>%(path)s)' + '(\\?(?P<query>%(query)s))?' + '(#%(fragment)s)?$'
        authority = '(?P<host>([\\w\\-_]+\\.)*[\\w\\-_]+):(?P<port>\\d{1,5})'
        query = 'configuration(=(?P<fragment>(?P<cfgkey>[^# ]+)))?'
        return pattern % dict(scheme=self.scheme, authority=authority, path=self.path, query=query, fragment='(?!)')