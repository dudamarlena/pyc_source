# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/testpackage/pbr_testpackage/wsgi.py
# Compiled at: 2017-12-04 07:19:32
from __future__ import print_function
import argparse, functools, sys

def application(env, start_response, data):
    sys.stderr.flush()
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [data.encode('utf-8')]


def main():
    parser = argparse.ArgumentParser(description='Return a string.')
    parser.add_argument('--content', '-c', help='String returned', default='Hello World')
    args = parser.parse_args()
    return functools.partial(application, data=args.content)


class WSGI(object):

    @classmethod
    def app(self):
        return functools.partial(application, data='Hello World')