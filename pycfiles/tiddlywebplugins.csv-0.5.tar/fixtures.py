# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bengillies/src/tiddlywebplugins.csv/test/fixtures.py
# Compiled at: 2012-02-02 11:19:37
"""
Setup some tiddlers to test with
"""
test_tiddlers = [
 ('foo', '{\n        "text": "Hello There!",\n        "modified": "20120202000000",\n        "created": "20120202000000",\n        "tags": ["foo", "bar", "baz"],\n        "modifier": "bob",\n        "fields": {\n            "one": "1"\n        }\n    }'),
 ('bar', '{\n        "text": "Lorem Ipsum Dolor Sit ♥",\n        "modified": "20120202000000",\n        "created": "20120202000000",\n        "tags": ["foo baz", "biz", "bix"],\n        "modifier": "alice",\n        "fields": {\n            "two": "2"\n        }\n    }'),
 ('baz', '{\n        "text": "Goodbye",\n        "modified": "20120202000000",\n        "created": "20120202000000",\n        "tags": [],\n        "modifier": "Steve",\n        "fields": {\n            "one": "1",\n            "three": "3"\n        }\n    }'),
 ('biz', '{\n        "text": "Some text, here",\n        "modified": "20120202000000",\n        "created": "20120202000000",\n        "tags": ["foo", "biz", "bix"],\n        "modifier": "Bill",\n        "fields": {\n            "one": "1"\n        }\n    }')]