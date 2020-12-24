# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/readers/xml_reader.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
import xml.etree.ElementTree as et

class XMLReader(object):

    def __init__(self, instance):
        self.instance = instance

    def read(self):
        """Convert XML to Dict"""
        tree = et.parse(self.instance.source)
        elements = tree.findall(self.instance.root)
        for elem in elements:
            items = list(elem)
            content = [ i.text for i in items ]
            yield content