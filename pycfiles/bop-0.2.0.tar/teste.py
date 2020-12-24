# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boo_box/teste.py
# Compiled at: 2008-05-02 09:14:26
import boo_box, simplejson
boo = boo_box.Box('submarinoid', '248960').getJSON('livros javascript').replace('jsonBooboxApi(', '')
json = simplejson.loads(boo[:-1])
for item in json['item']:
    print item