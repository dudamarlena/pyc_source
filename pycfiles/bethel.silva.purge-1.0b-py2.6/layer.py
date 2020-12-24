# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/silva/purge/tests/layer.py
# Compiled at: 2012-05-23 10:50:42
from Products.Silva.testing import SilvaLayer
import transaction

class PurgeLayer(SilvaLayer):
    default_products = SilvaLayer.default_products + ['SilvaDocument']
    default_packages = SilvaLayer.default_packages + ['zope.annotation']

    def _install_application(self, app):
        """ install the silva event extension """
        super(PurgeLayer, self)._install_application(app)
        app.root.service_extensions.install('bethel.silva.purge')
        self.grok('bethel.silva.purge.tests.grok')

    def addObject(self, container, type_name, id, product='Silva', **kw):
        getattr(container.manage_addProduct[product], 'manage_add%s' % type_name)(id, **kw)
        transaction.savepoint()
        return getattr(container, id)