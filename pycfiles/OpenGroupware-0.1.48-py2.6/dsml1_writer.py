# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/ldap/dsml1_writer.py
# Compiled at: 2012-10-12 07:02:39
import string, base64
from xml.sax.saxutils import escape
DSML_EXCLUDED_ATTRIBUTES = [
 'objectClass', 'objectcass']

class DSML1Writer(object):

    def __init__(self):
        self._wfile = None
        return

    def _write_objectclasses(self, entry):
        objectclasses = entry.get('objectClass', entry.get('objectclass', []))
        if len(objectclasses) > 0:
            self._wfile.write('<dsml:objectclass>')
            for oc in objectclasses:
                self._wfile.write(('<dsml:oc-value>{0}</dsml:oc-value>').format(oc))

            self._wfile.write('</dsml:objectclass>')

    def _write_attribute(self, attribute, values):
        self._wfile.write(('<dsml:attr name="{0}">').format(attribute))
        for value in values:
            try:
                text = unicode(value, 'utf-8')
            except UnicodeError:
                text = base64.encodestring(value)
                self._wfile.write(('<dsml:value encoding="base64">{0}</dsml:value>').format(text))
            else:
                self._wfile.write(('<dsml:value>{0}</dsml:value>').format(escape(text)))

        self._wfile.write('</dsml:attr>')

    def _write_attributes(self, entry):
        attributes = entry.keys()[:]
        attributes.sort()
        for attribute in attributes:
            if attribute not in DSML_EXCLUDED_ATTRIBUTES:
                self._write_attribute(attribute, entry[attribute])

    def _write_entry(self, entry):
        self._wfile.write(('<dsml:entry dn="{0}">').format(escape(entry[0])))
        self._write_objectclasses(entry[1])
        self._write_attributes(entry[1])
        self._wfile.write('</dsml:entry>')

    def write(self, data, stream):
        self._wfile = stream
        self._wfile.write('<?xml version="1.0" encoding="utf-8"?>')
        self._wfile.write('<dsml:dsml xmlns:dsml="http://www.dsml.org/DSML">')
        self._wfile.write('<dsml:directory-entries>')
        if isinstance(data, list):
            for entry in data:
                self._write_entry(entry)

        else:
            self._write_entry(data)
        self._wfile.write('</dsml:directory-entries>')
        self._wfile.write('</dsml:dsml>')