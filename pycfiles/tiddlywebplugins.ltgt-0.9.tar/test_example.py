# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jon/Documents/TiddlyWiki/Trunk/contributors/JonRobson/TiddlyWeb/plugins/LessThanGreaterThanFilter/test/test_example.py
# Compiled at: 2010-03-22 09:49:13
from tiddlywebplugins import ltgt
from tiddlyweb.model.tiddler import Tiddler

def test_comparedate():
    d1 = '20081201'
    d2 = '20091205'
    res1 = ltgt.comparedate(d1, d2)
    assert res1 is -1
    res2 = ltgt.comparedate(d1, d1)
    assert res2 is 0
    res3 = ltgt.comparedate('20101201123201', '20101201123200')
    assert res3 is 1


def test_lt_gt():
    tiddlers = []
    dummy = '20050322134706'
    dates = ['20091203', '20081203', '20080403', '20090903', '20090331', '20071103', dummy, dummy, dummy, dummy, dummy, dummy]
    for i in [1, 2, 4, 6, 10, 12, 55, 90, 100, 201, 323, 2223]:
        tid = Tiddler('foo%s' % i)
        tid.fields['foo'] = '%s' % i
        try:
            tid.modified = dates.pop()
        except IndexError:
            pass

        tiddlers.append(tid)

    restiddlers = ltgt.lt('foo:10', tiddlers)
    result = []
    for tid in restiddlers:
        result.append(tid)

    assert 4 is len(result)
    restiddlers = ltgt.lt('foo:1', tiddlers)
    result = []
    for tid in restiddlers:
        result.append(tid)

    assert 0 is len(result)
    restiddlers = ltgt.gt('foo:300', tiddlers)
    result = []
    for tid in restiddlers:
        result.append(tid)

    assert 2 is len(result)
    restiddlers = ltgt.gt('modified:20081101', tiddlers)
    result = []
    for tid in restiddlers:
        print tid.modified
        result.append(tid)

    assert 4 is len(result)
    restiddlers = ltgt.lt('modified:20050323', tiddlers)
    result = []
    for tid in restiddlers:
        print tid.modified
        result.append(tid)

    assert 6 is len(result)