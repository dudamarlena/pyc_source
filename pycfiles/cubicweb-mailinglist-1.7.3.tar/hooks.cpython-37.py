# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dlaxalde/src/cw/cubes/localperms/cubicweb_localperms/hooks.py
# Compiled at: 2019-03-13 06:51:56
# Size of source mod 2**32: 5661 bytes
__doc__ = 'cubicweb-localperms specific hooks and operations'
from cubicweb.server import hook
S_RELS = set()
O_RELS = set(())
SKIP_S_RELS = set()
SKIP_O_RELS = set()

class AddGrantedToSynchronizationHook(hook.Hook):
    __regid__ = 'localperms.granted_permission_added'
    __select__ = hook.Hook.__select__ & hook.match_rtype('granted_permission')
    events = ('after_add_relation', )
    rql = 'SET P require_permission G WHERE P eid %(p)s, G eid %(g)s,NOT P require_permission G'

    def __call__(self):
        self._cw.execute(self.rql, {'p':self.eidfrom,  'g':self.eidto})


class DelGrantedToSynchronizationHook(AddGrantedToSynchronizationHook):
    __regid__ = 'localperms.granted_permission_deleted'
    events = ('after_delete_relation', )
    rql = 'DELETE P require_permission G WHERE P eid %(p)s, G eid %(g)s'


class AddEntitySecurityPropagationHook(hook.PropagateRelationHook):
    """AddEntitySecurityPropagationHook"""
    __regid__ = 'localperms.add_entity'
    __select__ = hook.PropagateRelationHook.__select__ & hook.match_rtype_sets(S_RELS, O_RELS)
    main_rtype = 'require_permission'
    subject_relations = S_RELS
    object_relations = O_RELS


class AddPermissionSecurityPropagationHook(hook.PropagateRelationAddHook):
    __regid__ = 'localperms.add_permission'
    __select__ = hook.PropagateRelationAddHook.__select__ & hook.match_rtype('require_permission')
    subject_relations = S_RELS
    object_relations = O_RELS
    skip_subject_relations = SKIP_S_RELS
    skip_object_relations = SKIP_O_RELS


class DelPermissionSecurityPropagationHook(hook.PropagateRelationDelHook):
    __regid__ = 'localperms.del_permission'
    __select__ = hook.PropagateRelationDelHook.__select__ & hook.match_rtype('require_permission')
    subject_relations = S_RELS
    object_relations = O_RELS
    skip_subject_relations = SKIP_S_RELS
    skip_object_relations = SKIP_O_RELS


class AddGroupPermissionSecurityPropagationHook(hook.Hook):
    """AddGroupPermissionSecurityPropagationHook"""
    __regid__ = 'localperms.add_group_permission'
    __select__ = hook.Hook.__select__ & hook.match_rtype('require_group')
    events = ('after_add_relation', )
    rql = 'SET U has_group_permission P WHERE U in_group G, P eid %(p)s, G eid %(g)s,NOT U has_group_permission P'

    def __call__(self):
        if self._cw.entity_metas(self.eidfrom)['type'] != 'CWPermission':
            return
        self._cw.execute(self.rql, {'p':self.eidfrom,  'g':self.eidto})


class DelGroupPermissionSecurityPropagationHook(AddGroupPermissionSecurityPropagationHook):
    """DelGroupPermissionSecurityPropagationHook"""
    __regid__ = 'localperms.del_group_permission'
    events = ('after_delete_relation', )
    rql = 'DELETE U has_group_permission P WHERE U in_group G, P eid %(p)s, G eid %(g)s,NOT EXISTS(U in_group G2, P require_group G2)'


class AddInGroupSecurityPropagationHook(hook.Hook):
    """AddInGroupSecurityPropagationHook"""
    __regid__ = 'localperms.add_in_group_permission'
    __select__ = hook.Hook.__select__ & hook.match_rtype('in_group')
    events = ('after_add_relation', )
    rql = 'SET U has_group_permission P WHERE U eid %(u)s, P require_group G, G eid %(g)s, NOT U has_group_permission P'

    def __call__(self):
        self._cw.execute(self.rql, {'u':self.eidfrom,  'g':self.eidto})


class DelInGroupSecurityPropagationHook(AddInGroupSecurityPropagationHook):
    """DelInGroupSecurityPropagationHook"""
    __regid__ = 'localperms.del_in_group_permission'
    events = ('after_delete_relation', )
    rql = 'DELETE U has_group_permission P WHERE U eid %(u)s, P require_group G, G eid %(g)s, NOT EXISTS(U in_group G2, P require_group G2)'


def registration_callback(vreg):
    global O_RELS
    global S_RELS
    vreg.register_all(globals().values(), __name__)
    import os
    if os.environ.get('LOCALPERMS_INSTRUMENTALIZE'):
        from cubicweb.devtools.instrument import CubeTracerSet
        S_RELS = CubeTracerSet(vreg, S_RELS)
        O_RELS = CubeTracerSet(vreg, O_RELS)