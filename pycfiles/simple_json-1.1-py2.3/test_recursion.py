# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.3.0-Power_Macintosh/egg/simple_json/tests/test_recursion.py
# Compiled at: 2005-12-30 07:26:07
import simple_json

def test_listrecursion():
    x = []
    x.append(x)
    try:
        simple_json.dumps(x)
    except ValueError:
        pass
    else:
        assert False, "didn't raise ValueError on list recursion"

    x = []
    y = [
     x]
    x.append(y)
    try:
        simple_json.dumps(x)
    except ValueError:
        pass
    else:
        assert False, "didn't raise ValueError on alternating list recursion"

    y = []
    x = [
     y, y]
    simple_json.dumps(x)


def test_dictrecursion():
    x = {}
    x['test'] = x
    try:
        simple_json.dumps(x)
    except ValueError:
        pass
    else:
        assert False, "didn't raise ValueError on dict recursion"

    x = {}
    y = {'a': x, 'b': x}
    simple_json.dumps(x)


class TestObject:
    __module__ = __name__


class RecursiveJSONEncoder(simple_json.JSONEncoder):
    __module__ = __name__
    recurse = False

    def default(self, o):
        if o is TestObject:
            if self.recurse:
                return [
                 TestObject]
            else:
                return 'TestObject'
        simple_json.JSONEncoder.default(o)


def test_defaultrecursion():
    enc = RecursiveJSONEncoder()
    assert enc.encode(TestObject) == '"TestObject"'
    enc.recurse = True
    try:
        enc.encode(TestObject)
    except ValueError:
        pass
    else:
        assert False, "didn't raise ValueError on default recursion"