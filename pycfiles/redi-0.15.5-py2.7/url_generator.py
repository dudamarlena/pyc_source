# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/url_generator.py
# Compiled at: 2018-08-13 08:58:37
import logging
from HTMLParser import HTMLParser
import urllib, urllib2
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class InitPlugin:
    """Call the Form URL Plugin for REDCap with POST parameters
    and get the response.
    Parse the response and extract the URL form it.

    """

    def __init__(self, url, values):
        self.url = url
        self.values = values
        log_str = 'Initializing Plugin parser with URL: ' + self.url
        logger.info(log_str)
        self.get_response(self.url, self.values)

    def get_response(self, url, values):
        post_data = urllib.urlencode(values)
        prepared_request = urllib2.Request(url, post_data)
        response = urllib2.urlopen(prepared_request)
        html_string = response.read()
        parser = PluginParser()
        parser.feed(html_string)
        return parser.output


class PluginParser(HTMLParser):
    """Parser module for the HTML response received

    """

    def feed(self, data):
        self.output = []
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.output.append(value)