# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.3.0-Power_Macintosh/egg/simple_json/tests/test_pass3.py
# Compiled at: 2005-12-29 17:00:38
JSON = '\\\n{\n    "JSON Test Pattern pass3": {\n        "The outermost value": "must be an object or array.",\n        "In this test": "It is an object."\n    }\n}'

def test_parse():
    import simple_json
    res = simple_json.loads(JSON)
    out = simple_json.dumps(res)
    assert res == simple_json.loads(out)