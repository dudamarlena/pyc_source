# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/brownant/request.py
# Compiled at: 2014-10-08 05:32:06
from __future__ import absolute_import, unicode_literals

class Request(object):
    """The request object.

    :param url: the raw URL inputted from the dispatching app.
    :type url: :class:`urllib.parse.ParseResult`
    :param args: the query arguments decoded from query string of the URL.
    :type args: :class:`werkzeug.datastructures.MultiDict`
    """

    def __init__(self, url, args):
        self.url = url
        self.args = args

    def __repr__(self):
        return (b'Request(url={self.url}, args={self.args})').format(self=self)