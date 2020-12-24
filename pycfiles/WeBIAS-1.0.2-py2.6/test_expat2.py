# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/objectify/test/test_expat2.py
# Compiled at: 2015-04-13 16:10:45
"""Read using Expat parser and print and objectified XML file"""
import sys
from gnosis.xml.objectify import XML_Objectify, pyobj_printer, EXPAT

class MyExpatBased_XML_Objectify(XML_Objectify):
    expat_args = []
    expat_kwargs = {'nspace_sep': None}

    def __init__(self, xml_src):
        XML_Objectify.__init__(self, xml_src=xml_src, parser=EXPAT)


if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        try:
            xml_obj = XML_Objectify(xml_src=filename, parser=EXPAT)
            py_obj = xml_obj.make_instance()
        except SyntaxError:
            print 'Caught SyntaxError exception! Possibly an XML file with namespaces that\nis causing this, so try again but ignore XML namespaces...',
            xml_obj = MyExpatBased_XML_Objectify(filename)
            try:
                py_obj = xml_obj.make_instance()
                print 'it worked!'
            except:
                print 'it did NOT work!'
                raise

        print pyobj_printer(py_obj).encode('UTF-8')

else:
    print 'Please specify one or more XML files to Objectify.'