# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyMind/settings.py
# Compiled at: 2013-06-11 17:50:10
__doc__ = '\nCopyright 2012 Alexey Kravets  <mr.kayrick@gmail.com>\n\nThis file is part of PythonMindmeister.\n\nPythonMindmeister is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nPythonMindmeister is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with PythonMindmeister.  If not, see <http://www.gnu.org/licenses/>.\n\nThis file implements key->value interface to the settings storage. \nSettings must be stored in XML file specified in the \nconstructor of the settings class.\n\nThis product uses the MindMeister API but is not endorsed or certified\nby MindMeister.\n'
from lxml import etree
schema = '<?xml version="1.0" encoding="UTF-8"?>\n<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.example.org/schema" xmlns:tns="http://www.example.org/schema" elementFormDefault="qualified">\n  <element name="config">\n    <complexType>\n      <sequence>\n        <element minOccurs="1" maxOccurs="unbounded" name="value">\n          <complexType>\n            <simpleContent>\n              <extension base="string">\n                <attribute name="key" type="string" use="required"/>\n               </extension>\n            </simpleContent>\n          </complexType>\n        </element>\n      </sequence>\n    </complexType>\n  </element>\n</schema>\n'

class SettingsStorage:
    """
    This class implements key->value interface to the settings storage.
    Settings are loaded from the file specified in constructor.
    """

    def __init__(self, filename):
        rawXML = open(filename).read()
        etreeSchema = etree.XMLSchema(etree.XML(schema))
        parser = etree.XMLParser(schema=etreeSchema)
        root = etree.fromstring(rawXML, parser)
        self.data = {}
        for item in root:
            key = item.attrib['key']
            value = item.text
            self.data[key] = value

    def store(self):
        pass