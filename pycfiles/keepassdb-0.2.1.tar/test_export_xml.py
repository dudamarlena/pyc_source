# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/tests/test_export_xml.py
# Compiled at: 2013-01-01 20:26:58
"""
Unit tests for group-related operations.
"""
from __future__ import print_function
import os.path
from xml.etree import ElementTree as ET
from keepassdb import Database, model, exc
from keepassdb.export.xml import XmlExporter
from keepassdb.tests import TestBase, RESOURCES_DIR

class XmlExporterTest(TestBase):

    def test_export(self):
        """ Really basic XML-export smoke test. """
        db = Database(os.path.join(RESOURCES_DIR, 'example.kdb'), password='test')
        exporter = XmlExporter()
        output = exporter.export(db)
        tree = ET.fromstring(output)
        entries = tree.findall('.//entry')
        s1 = set([ e.find('./title').text.strip() for e in entries ])
        s2 = set([ e.title for e in db.entries if e.title != 'Meta-Info' ])
        self.assertEquals(s2, s1)