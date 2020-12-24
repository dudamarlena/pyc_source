# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.monkeyplone/atreal/monkeyplone/patch.py
# Compiled at: 2011-11-18 05:43:13
from AccessControl import getSecurityManager
from Acquisition import aq_parent, aq_inner, aq_base
from Products.CMFCore.exceptions import AccessControl_Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.PortalFolder import PortalFolderBase

def _verifyObjectPasteCMFCore(self, object, validate_src=1):
    mt = getattr(object, '__factory_meta_type__', None)
    meta_types = getattr(self, 'all_meta_types', None)
    if mt is not None:
        if meta_types is not None:
            method_name = None
            mt_permission = None
            if callable(meta_types):
                meta_types = meta_types()
            for d in meta_types:
                if d['name'] == mt:
                    method_name = d['action']
                    mt_permission = d.get('permission')
                    break

            if mt_permission is not None:
                sm = getSecurityManager()
                if sm.checkPermission(mt_permission, self):
                    if validate_src:
                        parent = aq_parent(aq_inner(object))
                        if not sm.validate(None, parent, None, object):
                            raise AccessControl_Unauthorized(object.getId())
                        if validate_src == 2:
                            raise sm.checkPermission('View', parent) or AccessControl_Unauthorized('Delete not allowed.')
            else:
                raise AccessControl_Unauthorized('You do not possess the %r permission in the context of the container into which you are pasting, thus you are not able to perform this operation.' % mt_permission)
        else:
            raise AccessControl_Unauthorized('The object %r does not support this operation.' % object.getId())
    else:
        PortalFolderBase.inheritedAttribute('_verifyObjectPaste')(self, object, validate_src)
    if hasattr(aq_base(object), 'getPortalTypeName'):
        type_name = object.getPortalTypeName()
        if type_name is not None:
            pt = getToolByName(self, 'portal_types')
            myType = pt.getTypeInfo(self)
            if myType is not None and not myType.allowType(type_name):
                raise ValueError('Disallowed subobject type: %s' % type_name)
    return