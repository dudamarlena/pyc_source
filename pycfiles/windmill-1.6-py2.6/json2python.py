# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/bin/json2python.py
# Compiled at: 2011-01-13 01:48:00
from windmill.dep import json
import sys, os
from windmill.authoring import transforms

def transform_json_to_python(json_strings):
    """Transform serialized JSON objects to python code using the windmill transformer architecture"""
    tests = []
    for line in json_strings:
        tests.append(json.loads(line))

    return transforms.build_test_file(tests)


if __name__ == '__main__':
    if len(sys.argv) is 1:
        files = [ fn for fn in os.listdir('.') if fn.endswith('.json') ]
    else:
        files = [ fn for fn in sys.argv if fn.endswith('.json') ]
    for filename in files:
        f = open(filename.replace('.json', '.py'), 'w')
        f.write(transform_json_to_python(open(filename, 'r').read().splitlines()))
        f.flush()
        f.close()
        print 'created file %s' % filename.replace('.json', '.py')