# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/python_grabber/test.py
# Compiled at: 2010-01-22 19:34:24
from gmail import GmailGrabber
from msn import MsnGrabber
from yahoo import YahooGrabber

def test_gmail():
    res = GmailGrabber(username='username', password='password').grab()
    assert len(res) > 0


def test_hotmail():
    res = MsnGrabber(username='username@hotmail.com', password='password').grab()
    assert len(res) > 0


def test_yahoo():
    res = YahooGrabber(username='username@yahoo.fr', password='password').grab()
    assert len(res) > 0