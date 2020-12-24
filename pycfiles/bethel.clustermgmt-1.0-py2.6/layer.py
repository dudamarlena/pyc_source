# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/clustermgmt/tests/layer.py
# Compiled at: 2012-04-27 16:55:43
from Products.Silva.testing import SilvaLayer
import transaction

class HealthLayer(SilvaLayer):

    def _install_application(self, app):
        """ install the silva event extension """
        super(HealthLayer, self)._install_application(app)
        app.root.service_extensions.install('bethel.clustermgmt')
        self.hr = self.addObject(app.root, 'HealthReporter', 'hr', product='bethel.clustermgmt')

    def addObject(self, container, type_name, id, product='Silva', **kw):
        getattr(container.manage_addProduct[product], 'manage_add%s' % type_name)(id, **kw)
        transaction.savepoint()
        return getattr(container, id)