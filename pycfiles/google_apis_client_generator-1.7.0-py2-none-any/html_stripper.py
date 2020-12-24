# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/html_stripper.py
# Compiled at: 2019-01-24 16:56:47
"""HTMLStripper based on HTMLParser."""
__author__ = 'wclarkso@google.com (Will Clarkson)'
import HTMLParser

class HTMLStripper(HTMLParser.HTMLParser):
    """Simple class to strip tags from HTML."""

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def GetFedData(self):
        return ('').join(self.fed)

    def ClearFedData(self):
        self.fed = []