# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_lib.py
# Compiled at: 2011-10-20 15:47:47
__author__ = 'dgraziotin'
import datapkggui.lib as lib, tempfile
TEST_PACKAGE_FIXED = 'datapkg-gui-test'

class TestLib:

    def test_list(self):
        ckan_list = lib.list('ckan://')
        assert len(ckan_list) > 2000
        package_names = []
        for package in ckan_list:
            package_names.append(package.name)

        assert TEST_PACKAGE_FIXED in package_names

    def test_search(self):
        test_package = lib.search('ckan://', TEST_PACKAGE_FIXED)
        assert len(test_package) > 0
        assert test_package[0].name == TEST_PACKAGE_FIXED

    def test_info(self):
        test_package_metadata = lib.info('ckan://' + TEST_PACKAGE_FIXED)
        assert test_package_metadata['name'] == TEST_PACKAGE_FIXED
        assert len(test_package_metadata['resources']) == 2

    def test_download(self):
        path = tempfile.mkdtemp()
        assert lib.download('ckan://' + TEST_PACKAGE_FIXED, path) == True