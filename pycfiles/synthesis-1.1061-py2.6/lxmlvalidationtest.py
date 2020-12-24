# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/lxmlvalidationtest.py
# Compiled at: 2010-08-29 15:44:28
from lxml import etree
schema_file_location = '/home/user/workspace/synthesis/installer/build/xsd/versions/HMISXML/28/HUD_HMIS.xsd'
instance_file_location = '/home/user/workspace/synthesis/TestFiles/Example_HUD_HMIS_2_8_Instance.xml'
schemafileobject = open(schema_file_location, 'r')
instancefileobject = open(instance_file_location, 'r')
etreeinstanceobject = etree.parse(instancefileobject)
etreeschemaobject = etree.parse(schemafileobject)
xmlschema = etree.XMLSchema(etreeschemaobject)
if xmlschema.validate(etreeinstanceobject):
    print 'Validates'
else:
    print "Doesn't validate"