# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/jid.py
# Compiled at: 2017-02-05 18:35:24
# Size of source mod 2**32: 5474 bytes
from threading import Lock
__internJIDs = {}
__internJIDs_lock = Lock()

class InvalidJidError(RuntimeError):
    __doc__ = 'Exception type for Invalid Jabber Identifiers.'


class Jid(object):

    def __init__(self, j):
        if isinstance(j, str):
            self._local_part, self._domain_part, self._rsrc_part = _parse(j)
        else:
            if isinstance(j, tuple):
                self._local_part, self._domain_part, self._rsrc_part = _prep(*j)
            else:
                if issubclass(j.__class__, Jid):
                    self._local_part, self._domain_part, self._rsrc_part = j._local_part, j._domain_part, j._rsrc_part
                else:
                    raise ValueError("Type must be str or tuple(str, str, str). Got '%s' instead." % str(type(j)))

    @property
    def user(self):
        return self._local_part

    localpart = user

    @property
    def host(self):
        return self._domain_part

    domainpart = host

    @property
    def resource(self):
        return self._rsrc_part

    resourcepart = resource

    @property
    def full(self):
        if self._local_part:
            if self._rsrc_part:
                return '%s@%s/%s' % (self._local_part,
                 self._domain_part,
                 self._rsrc_part)
            else:
                return '%s@%s' % (self._local_part, self._domain_part)
        else:
            if self.resource:
                return '%s/%s' % (self._domain_part, self._rsrc_part)
            else:
                return self._domain_part

    @property
    def bare(self):
        if self._local_part:
            return '%s@%s' % (self._local_part, self._domain_part)
        else:
            return self._domain_part

    def __eq__(self, other):
        if isinstance(other, Jid):
            return self.user == other.user and self.host == other.host and self.resource == other.resource
        raise NotImplementedError("Jid and '%s' not compariable" % str(type(other)))

    @property
    def bare_jid(self):
        """
        Extract the bare JID.

        A bare JID does not have a resource part, so this returns a
        Jid object representing either user@host or just host.

        If the JID object doesn't have a resource set, it will return itself
        (i.e. self). Otherwise, the bare JID object will be created, interned
        using ``internJID``.
        """
        if self.resource:
            return internJid(self.bare)
        else:
            return self

    def __ne__(self, other):
        try:
            result = self.__eq__(other)
        except NotImplementedError:
            return True
        else:
            return not result

    def __hash__(self):
        return hash((self.user, self.host, self.resource))

    def __unicode__(self):
        return self.full

    def __repr__(self):
        return 'Jid(%r)' % self.full


def _parse(j):
    user = None
    host = None
    resource = None
    user_sep = j.find('@')
    res_sep = j.find('/')
    if user_sep == -1:
        if res_sep == -1:
            host = j
        else:
            host = j[0:res_sep]
            resource = j[res_sep + 1:] or None
    else:
        if res_sep == -1:
            user = j[0:user_sep] or None
            host = j[user_sep + 1:]
        else:
            if user_sep < res_sep:
                user = j[0:user_sep] or None
                host = j[user_sep + 1:user_sep + (res_sep - user_sep)]
                resource = j[res_sep + 1:] or None
            else:
                host = j[0:res_sep]
                resource = j[res_sep + 1:] or None
    return _prep(user, host, resource)


def _prep(user, host, resource):
    from ._stringprep import nodeprep, nameprep, resourceprep
    for arg in (user, host, resource):
        if arg and not isinstance(arg, str):
            raise ValueError('Jid comonents must be unicode strings')

    if user:
        user = nodeprep.prepare(user)
    else:
        user = None
    if not host:
        raise InvalidJidError('Domain part required.')
    else:
        host = nameprep.prepare(host)
    if resource:
        resource = resourceprep.prepare(resource)
    else:
        resource = None
    return (user, host, resource)


def internJid(jidstring):
    """
    Return interned JID.
    """
    __internJIDs_lock.acquire()
    try:
        if jidstring in __internJIDs:
            return __internJIDs[jidstring]
        else:
            j = Jid(jidstring)
            jidstring = j.full
            if jidstring in __internJIDs:
                return __internJIDs[jidstring]
            __internJIDs[jidstring] = j
            return j
    finally:
        __internJIDs_lock.release()