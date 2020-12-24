# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\example2.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 576 bytes
import xmind
from xmind.core import workbook, saver
from xmind.core.topic import TopicElement
w = xmind.load('test.xmind')
w = xmind.load('mac.xmind')
s1 = w.getPrimarySheet()
r1 = s1.getRootTopic()
topics_l01 = r1.getSubTopics()
for topic_case_group in topics_l01:
    topic_case_priority_name = topic_case_group.getMarkers()[0].getMarkerId()
    print(topic_case_priority_name)