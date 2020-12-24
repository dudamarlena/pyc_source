# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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