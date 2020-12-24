# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_metadata.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3452 bytes
import pytest
from mediagoblin.tools.metadata import compact_and_validate
from jsonschema import ValidationError

class TestMetadataFunctionality:

    @pytest.fixture(autouse=True)
    def _setup(self, test_app):
        self.test_app = test_app

    def testCompactAndValidate(self):
        test_metadata = {'dc:title': 'My Pet Bunny', 
         'dc:description': 'A picture displaying how cute my pet bunny is.', 
         'location': '/home/goblin/Pictures/bunny.png', 
         'license': 'http://www.gnu.org/licenses/gpl.txt'}
        jsonld_metadata = compact_and_validate(test_metadata)
        assert jsonld_metadata
        assert jsonld_metadata.get('dc:title') == 'My Pet Bunny'
        assert jsonld_metadata.get('location') is None
        assert jsonld_metadata.get('@context') == 'http://www.w3.org/2013/json-ld-context/rdfa11'
        metadata_fail_1 = {'dc:title': 'My Pet Bunny', 
         'dc:description': 'A picture displaying how cute my pet bunny is.', 
         'location': '/home/goblin/Pictures/bunny.png', 
         'license': 'All Rights Reserved.'}
        jsonld_fail_1 = None
        try:
            jsonld_fail_1 = compact_and_validate(metadata_fail_1)
        except ValidationError as e:
            if not e.message == "'All Rights Reserved.' is not a 'uri'":
                raise AssertionError

        assert jsonld_fail_1 == None
        metadata_fail_2 = {'dc:title': 'My Pet Bunny', 
         'dc:description': 'A picture displaying how cute my pet bunny is.', 
         'location': '/home/goblin/Pictures/bunny.png', 
         'license': 'http://www.gnu.org/licenses/gpl.txt', 
         'dc:created': 'The other day'}
        jsonld_fail_2 = None
        try:
            jsonld_fail_2 = compact_and_validate(metadata_fail_2)
        except ValidationError as e:
            if not e.message == "'The other day' is not a 'date-time'":
                raise AssertionError

        assert jsonld_fail_2 == None