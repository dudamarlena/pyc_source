# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/exportimport.py
# Compiled at: 2011-09-02 07:59:09
from plone.app.portlets.exportimport.portlets import PropertyPortletAssignmentExportImportHandler
from persistent.dict import PersistentDict
from Solgema.PortletsManager import ATTR

class SolgemaPortletAssignmentImportExportHandler(PropertyPortletAssignmentExportImportHandler):

    def import_stopUrls(self, node):
        try:
            stopUrls = node.getAttribute('stopUrls')
        except:
            return

        if not hasattr(self.assignment, ATTR):
            setattr(self.assignment, ATTR, PersistentDict())
        getattr(self.assignment, ATTR)['stopUrls'] = stopUrls

    def export_stopUrls(self, doc, node):
        stopUrls = getattr(self.assignment, ATTR, {}).get('stopUrls')
        if stopUrls is None:
            return
        else:
            node.setAttribute('stopUrls', stopUrls)
            return

    def import_assignment(self, interface, node):
        self.import_stopUrls(node)
        PropertyPortletAssignmentExportImportHandler.import_assignment(self, interface, node)

    def export_assignment(self, interface, doc, node):
        self.export_stopUrls(doc, node)
        PropertyPortletAssignmentExportImportHandler.export_assignment(self, interface, doc, node)