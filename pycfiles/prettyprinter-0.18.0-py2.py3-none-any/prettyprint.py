# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/prettyprint/prettyprint.py
# Compiled at: 2012-02-23 13:23:09
try:
    import json
except ImportError:
    import simplejson as json

__all__ = [
 'pp', 'pp_str']

class MyEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


def pp(obj):
    print pp_str(obj)


def pp_str(obj):
    orig = json.dumps(obj, indent=4, sort_keys=True, skipkeys=True, cls=MyEncoder)
    return eval("u'''%s'''" % orig).encode('utf-8')


if __name__ == '__main__':
    target = [
     'want pretty printing', '望麗出力']
    print target
    pp(target)
    target_dict = {'order': {'en': 'print prettily', 'ja': '綺麗に出力せよ'}}
    print target_dict
    pp(target_dict)
    set1 = set(['John', 'Jane', 'Jack', 'Janice'])
    pp(set1)
    orig = set(['item1', 'item2'])
    res = pp_str(orig)
    print res
    print json.loads(res)