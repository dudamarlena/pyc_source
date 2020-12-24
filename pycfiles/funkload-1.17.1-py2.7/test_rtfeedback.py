# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/tests/test_rtfeedback.py
# Compiled at: 2015-05-06 05:03:08
import unittest, time
from funkload import rtfeedback
import zmq

class TestFeedback(unittest.TestCase):

    def test_feedback(self):
        context = zmq.Context.instance()
        pub = rtfeedback.FeedbackPublisher(context=context)
        pub.start()
        msgs = []

        def _msg(msg):
            msgs.append(msg)

        sub = rtfeedback.FeedbackSubscriber(handler=_msg, context=context)
        sub.start()
        sender = rtfeedback.FeedbackSender(context=context)
        for i in range(10):
            sender.test_done({'result': 'success'})

        time.sleep(0.1)
        self.assertEqual(len(msgs), 10)