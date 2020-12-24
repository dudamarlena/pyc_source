# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: cubicweb_localperms/site_cubicweb.py
# Compiled at: 2019-03-13 06:52:01
"""install some monkey patches to ease API"""
from logilab.common.decorators import monkeypatch
from cubicweb import schema
schema.INTERNAL_TYPES.add('CWPermission')
schema.SYSTEM_RTYPES.add('require_group')
schema.SYSTEM_RTYPES.add('require_permission')
schema.SYSTEM_RTYPES.add('has_group_permission')
schema.NO_I18NCONTEXT.add('require_permission')
try:
    from cubicweb.server import repository, session
except ImportError:
    pass
else:
    repository.NO_CACHE_RELATIONS.add(('require_permission', 'object'))

    @monkeypatch(session.InternalManager, 'has_permission')
    @staticmethod
    def has_permission(self, pname, contexteid=None):
        return True


try:
    from cubicweb import devtools
except ImportError:
    pass
else:
    devtools.SYSTEM_ENTITIES.add('CWPermission')
    devtools.SYSTEM_RELATIONS.add('require_group')
    devtools.SYSTEM_RELATIONS.add('require_permission')