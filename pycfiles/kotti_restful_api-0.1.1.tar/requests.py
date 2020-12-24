# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_restful_api/kotti_restful_api/requests.py
# Compiled at: 2016-12-20 13:25:57


class ContentTypePredicate(object):

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'content type = %s' % self.val

    phash = text

    def __call__(self, context, request):
        return request.content_type == self.val


class CrossRequestPredicate(object):

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'cross_request = %s' % self.val

    phash = text

    def __call__(self, context, request):
        try:
            return request.cross_request == self.val
        except:
            return False