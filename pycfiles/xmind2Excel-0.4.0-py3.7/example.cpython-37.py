# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\example.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 1565 bytes
import xmind
from xmind.core import workbook, saver
from xmind.core.topic import TopicElement
w = xmind.load('test.xmind')
s1 = w.getPrimarySheet()
s1.setTitle('first sheet')
r1 = s1.getRootTopic()
r1.setTitle("we don't care of this sheet")
s2 = w.createSheet()
s2.setTitle('second sheet')
r2 = s2.getRootTopic()
r2.setTitle('root node')
t1 = TopicElement()
t1.setTopicHyperlink(s1.getID())
t1.setTitle('redirection to the first sheet')
t2 = TopicElement()
t2.setTitle('second node')
t2.setURLHyperlink('https://xmind.net')
t3 = TopicElement()
t3.setTitle('third node')
t3.setPlainNotes('notes for this topic')
t3.setTitle('topic with \n notes')
t4 = TopicElement()
t4.setFileHyperlink('logo.jpeg')
t4.setTitle('topic with a file')
r2.addSubTopic(t1)
r2.addSubTopic(t2)
r2.addSubTopic(t3)
r2.addSubTopic(t4)
topics = r2.getSubTopics()
for topic in topics:
    topic.addMarker('yes')

w.addSheet(s2)
rel = s2.createRelationship(t1.getID(), t2.getID(), 'test')
s2.addRelationship(rel)
xmind.save(w, 'test2.xmind')