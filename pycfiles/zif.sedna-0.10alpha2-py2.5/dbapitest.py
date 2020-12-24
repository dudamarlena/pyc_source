# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/sedna/dbapitest.py
# Compiled at: 2008-03-30 11:18:23
from dbapi import connect
from lxml.etree import parse
s = connect('dbi://SYSTEM:MANAGER@localhost:5050/test')
g = s.cursor()
g.execute('for $item in doc("ot")//v' + ' where contains($item,"begat") return $item')
items = []
for z in g.fetchall():
    items.append(parse(z))

g = z[0]
for (name, value) in g.docinfo.__dict__.items():
    print name, value