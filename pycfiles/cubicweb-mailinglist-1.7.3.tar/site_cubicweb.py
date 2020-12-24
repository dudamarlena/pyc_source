# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cubicweb_localperms/site_cubicweb.py
# Compiled at: 2019-03-13 06:52:01
__doc__ = 'install some monkey patches to ease API'
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