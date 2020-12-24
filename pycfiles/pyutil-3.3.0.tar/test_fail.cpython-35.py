# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_fail.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 2981 bytes
from unittest import TestCase
from pyutil import jsonutil as json
JSONDOCS = [
 '"A JSON payload should be an object or array, not a string."',
 '["Unclosed array"',
 '{unquoted_key: "keys must be quoted}',
 '["extra comma",]',
 '["double extra comma",,]',
 '[   , "<-- missing value"]',
 '["Comma after the close"],',
 '["Extra close"]]',
 '{"Extra comma": true,}',
 '{"Extra value after close": true} "misplaced quoted value"',
 '{"Illegal expression": 1 + 2}',
 '{"Illegal invocation": alert()}',
 '{"Numbers cannot have leading zeroes": 013}',
 '{"Numbers cannot be hex": 0x14}',
 '["Illegal backslash escape: \\x15"]',
 '["Illegal backslash escape: \\\'"]',
 '["Illegal backslash escape: \\017"]',
 '[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]',
 '{"Missing colon" null}',
 '{"Double colon":: null}',
 '{"Comma instead of colon", null}',
 '["Colon instead of comma": false]',
 '["Bad value", truth]',
 "['single quote']",
 '["A\x1fZ control characters in string"]']
SKIPS = {1: 'why not have a string payload?', 
 18: "spec doesn't specify any nesting limitations"}

class TestFail(TestCase):

    def test_failures(self):
        for idx, doc in enumerate(JSONDOCS):
            idx = idx + 1
            if idx in SKIPS:
                json.loads(doc)
                continue
                try:
                    json.loads(doc)
                except ValueError:
                    pass
                else:
                    self.fail('Expected failure for fail%d.json: %r' % (idx, doc))