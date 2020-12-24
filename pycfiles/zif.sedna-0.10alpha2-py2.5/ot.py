# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/sedna/example/ot.py
# Compiled at: 2008-03-30 11:18:23
from zif.sedna import protocol
import sys
username = 'SYSTEM'
password = 'MANAGER'
database = 'test'
port = 5050
host = 'localhost'
from lxml.etree import fromstring
import logging
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
conn = protocol.SednaProtocol(host, database, username, password, trace=True)
docs = conn.documents
qry2 = "doc('ot')//v[contains(., 'begat')]/text()"
qry1 = 'for $item in doc("ot")//v' + ' where contains($item,"begat") return $item'
if 'ot' not in docs:
    conn.loadFile('/home/jwashin/Desktop/ot/ot.xml', 'ot')
begat_verses = conn.query(qry2)
print begat_verses.time
conn.traceOff()
count = 0
for k in begat_verses:
    count += 1
    print count, k.strip()

conn.commit()
conn.close()