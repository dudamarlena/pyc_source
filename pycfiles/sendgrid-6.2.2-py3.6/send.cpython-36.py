# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/inbound/send.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1772 bytes
"""A module for sending test SendGrid Inbound Parse messages.
Usage: ./send.py [path to file containing test data]"""
import argparse, sys
from io import open
try:
    from config import Config
except ImportError:
    from sendgrid.helpers.inbound.config import Config

from python_http_client import Client

class Send(object):

    def __init__(self, url):
        """Create a Send object with target `url`."""
        self._url = url

    def test_payload(self, payload_filepath):
        """Send a test payload.

        Load a payload from payload_filepath, apply headers, and POST self.url.
        Return the response object.
        """
        headers = {'User-Agent':'SendGrid-Test', 
         'Content-Type':'multipart/form-data; boundary=xYzZY'}
        client = Client(host=(self.url), request_headers=headers)
        f = open(payload_filepath, 'r', encoding='utf-8')
        data = f.read()
        return client.post(request_body=data)

    @property
    def url(self):
        """URL to send to."""
        return self._url


def main():
    config = Config()
    parser = argparse.ArgumentParser(description='Test data and optional host.')
    parser.add_argument('data', type=str,
      help='path to the sample data')
    parser.add_argument('-host', type=str,
      help='name of host to send the sample data to',
      default=(config.host),
      required=False)
    args = parser.parse_args()
    send = Send(args.host)
    response = send.test_payload(sys.argv[1])
    print(response.status_code)
    print(response.headers)
    print(response.body)


if __name__ == '__main__':
    main()