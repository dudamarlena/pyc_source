# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/tests/test_license_tool.py
# Compiled at: 2011-07-11 14:56:02
import os, pkg_resources
from cc.licenserdf.tools import license
from cc.licenserdf.tests.util import PrinterCollector, unordered_ensure_printer_printed
RDF_DIR = pkg_resources.resource_filename('cc.licenserdf', 'licenses')
TEST_RDF_DIR = pkg_resources.resource_filename('cc.licenserdf.tests', 'licenses')

def test_license_rdf_filename():
    expected_url = os.path.join(RDF_DIR, 'creativecommons.org_licenses_by_2.0_.rdf')
    assert license.license_rdf_filename('http://creativecommons.org/licenses/by/2.0/') == expected_url
    expected_url = os.path.join(RDF_DIR, 'creativecommons.org_licenses_by_2.0_cl_.rdf')
    assert license.license_rdf_filename('http://creativecommons.org/licenses/by/2.0/cl/') == expected_url
    expected_url = os.path.join(RDF_DIR, 'creativecommons.org_licenses_BSD_.rdf')
    assert license.license_rdf_filename('http://creativecommons.org/licenses/BSD/') == expected_url
    expected_url = os.path.join(RDF_DIR, 'creativecommons.org_publicdomain_zero_1.0_.rdf')
    assert license.license_rdf_filename('http://creativecommons.org/publicdomain/zero/1.0/') == expected_url
    expected_url = os.path.join(TEST_RDF_DIR, 'creativecommons.org_publicdomain_zero_1.0_.rdf')
    assert license.license_rdf_filename('http://creativecommons.org/publicdomain/zero/1.0/', TEST_RDF_DIR) == expected_url


def test_legalcode_list():
    printer = PrinterCollector()
    license.legalcode_list('http://creativecommons.org/licenses/by-sa/3.0/', TEST_RDF_DIR, _printer=printer)
    unordered_ensure_printer_printed(printer, [
     'http://creativecommons.org/licenses/by-sa/3.0/legalcode'])