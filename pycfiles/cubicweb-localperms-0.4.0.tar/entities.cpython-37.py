# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dlaxalde/src/cw/cubes/localperms/cubicweb_localperms/entities.py
# Compiled at: 2019-03-13 06:52:29
# Size of source mod 2**32: 2429 bytes
"""cubicweb-localperms entity's classes"""
from logilab.common.decorators import monkeypatch
from cubicweb import Unauthorized
from cubicweb.entities import AnyEntity, fetch_config, authobjs

@monkeypatch(authobjs.CWGroup)
def grant_permission(self, entity, pname, plabel=None):
    """grant local `pname` permission on `entity` to this group using
    :class:`CWPermission`.

    If a similar permission already exists, add the group to it, else create
    a new one.
    """
    if not self._cw.execute('SET X require_group G WHERE E eid %(e)s, G eid %(g)s, E granted_permission X, X name %(name)s, X label %(label)s', {'e':entity.eid, 
     'g':self.eid,  'name':pname, 
     'label':plabel}):
        self._cw.create_entity('CWPermission', name=pname, label=plabel, require_group=self,
          reverse_granted_permission=entity)


@monkeypatch(authobjs.CWUser)
def has_permission(self, pname, contexteid=None):
    rql = 'Any P WHERE P is CWPermission, P name %(name)s, U has_group_permission P, U eid %(u)s'
    kwargs = {'name':pname,  'u':self.eid}
    if contexteid is not None:
        rql += ', X require_permission P, X eid %(x)s'
        kwargs['x'] = contexteid
    try:
        return self._cw.execute(rql, kwargs)
    except Unauthorized:
        return False


class CWPermission(AnyEntity):
    __regid__ = 'CWPermission'
    fetch_attrs, cw_fetch_order = fetch_config(['name', 'label'])

    def dc_title(self):
        if self.label:
            return '%s (%s)' % (self._cw._(self.name), self.label)
        return self._cw._(self.name)