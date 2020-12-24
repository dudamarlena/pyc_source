# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /sources/github/pyramid_restful_toolkit/pyramid_restful_toolkit/tweens.py
# Compiled at: 2014-08-22 04:59:55
__author__ = 'tarzan'

def jsonize_uncaught_exception_tween_factory(handler, registry):
    """
    This tween prevent all uncaught exception and return JSON response with error code 500
    """

    def jsonize_uncaught_exception_tween(request):
        """
        :type request: pyramid.request.Request
        :rtype : pyramid.response.Response
        """
        try:
            return handler(request)
        except BaseException as e:
            import json
            from pyramid import response
            body = json.dumps({'error': e.__class__.__name__, 
               'code': 500, 
               'status': '500 Internal Server Error', 
               'message': e.message})
            return response.Response(body=body, status='500 Internal Server Error', content_type='application/json')

    return jsonize_uncaught_exception_tween