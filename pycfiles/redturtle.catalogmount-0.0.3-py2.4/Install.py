# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redturtle/catalogmount/Extensions/Install.py
# Compiled at: 2009-03-03 10:57:26
from Products.ZODBMountPoint.MountedObject import manage_getMountStatus, MountedObject, setMountPoint, CustomTrailblazer
from StringIO import StringIO
import tempfile
from App.config import getConfiguration
import transaction

def install(self, out=None):
    if out is None:
        out = StringIO()
    to_mount = manage_getMountStatus(self)
    items = [ item for item in to_mount if 'catalog' in item['path'] if '** Something is in the way **' in item['status'] ]
    out.write('Mounting...')
    for item in items:
        path = item['path']
        id = path.split('/')[(-1)]
        old_obj = self.unrestrictedTraverse(path)
        old_parent = old_obj.aq_parent.aq_base
        db_name = item['name']
        db = getConfiguration().dbtab.getDatabase(path)
        new_trans = db.open()
        root = new_trans.root()
        if not root.has_key('Application'):
            from OFS.Application import Application
            root['Application'] = Application()
            transaction.savepoint(optimistic=True)
        root = root['Application']
        f = tempfile.TemporaryFile()
        old_obj._p_jar.exportFile(old_obj._p_oid, f)
        f.seek(0)
        new_obj = root._p_jar.importFile(f)
        f.close()
        blazer = CustomTrailblazer(root)
        obj = blazer.traverseOrConstruct(path)
        obj.aq_parent._setOb(id, new_obj)
        mo = MountedObject(path)
        mo._create_mount_points = True
        old_parent._p_jar.add(mo)
        old_parent._setOb(id, mo)
        setMountPoint(old_parent, id, mo)
        out.write('Path: %s, mounted to db:%s' % (path, db_name))

    return out.getvalue()