# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/test_files.py
# Compiled at: 2011-01-27 14:39:21
__doc__ = '\ntest_files.py\n\nCreated by Craig Sawyer on 2010-01-14.\nCopyright (c) 2009, 2010 Craig Sawyer (csawyer@yumaed.org). All rights reserved. see LICENSE.\n'
import os, nose, files

def test_append():
    s = 'ssh-dss fj20ufjsklfoowjAAACBAMWQmI0CjhHwZPdBNjLwb/xTxyn7bnOo/9AzLp4LcJILuYQy+sgFmNe1ivUBJdSqA58AcoeL8hhsfg2RE/Wb/kXOIHRXWawr8wzhYdGZYzgtLP7oIwPmQQP76vh+mcbEdyBGHVwFa++TJbNVH2nreYfrF4hniQ14y0FIooM9WSvjAAAAFQDWJ0n2bIjkiSJKgXSicrWYvjC9jQAAAIACdv8/C0geNKgQypmMzhQGZ8BH2B6A65KTA8543wBUZx6OWDaL//6KfsxulULdHjAOTuMBsHan8+qyEB6ixd3sr6gVj/w60CzIMshmwkPOEmAghGrxR6wSg6JAJnTIgo8xyWNi4hvOeKvAAY8x0QAd0mqBvAag4TH1mmOPddAOmQAAAIAeHnFzKpzMzuN/MAwKLOuroJZkU8WAdjmkRYupQjUmgermxb5x8fmh9Z7gzyeA6814MlnZWXUB0kAEMyWTNAXVPO8iGcun/Z2LRy//7x2bnlmVoSfdiPi1h4bSYy4WlGhhhlxst+I3HPshk7mB1CgALHYYrqj36rFM5yyObGxUUA== pootardia@testhost'
    files.append('/tmp/files_test', [s])
    res = open('/tmp/files_test').read()
    print res
    print s
    assert res == s + os.linesep


if __name__ == '__main__':
    nose.run()