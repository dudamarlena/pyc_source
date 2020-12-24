# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/evax/bitten/tools/check.py
# Compiled at: 2010-07-27 02:20:52
__docformat__ = 'restructuredtext en'
from bitten.build import FileSet
from bitten.util import xmlio
import os
from xml.dom import minidom
from xml.parsers.expat import ExpatError

def get_xml_value(elem, sub_elem):
    """ xml helper function """
    return elem.getElementsByTagName(sub_elem)[0].firstChild.data


def check(ctxt, reports=None):
    """ Analyse the xml output from check and integrate it in the report.

    :param ctxt: the build context
    :type ctxt: `Context`
    :param reports: a glob pattern matching the check xml repports
    """
    assert reports, 'Missing required attribute "reports"'
    results = xmlio.Fragment()
    for filename in FileSet(ctxt.basedir, reports, None):
        try:
            xmldoc = minidom.parse(os.path.join(ctxt.basedir, filename))
        except ExpatError:
            continue

        for suite in xmldoc.getElementsByTagName('suite'):
            for test in suite.getElementsByTagName('test'):
                desc = get_xml_value(test, 'description')
                tid = get_xml_value(test, 'id')
                result = test.attributes['result'].value
                results.append(xmlio.Element('test', fixture=desc, name=tid, status=result))

    ctxt.report('test', results)
    return