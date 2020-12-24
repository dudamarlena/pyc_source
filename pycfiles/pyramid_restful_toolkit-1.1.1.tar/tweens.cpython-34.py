# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /sources/github/pyramid_restful_toolkit/pyramid_restful_toolkit/tweens.py
# Compiled at: 2014-08-22 04:59:55
# Size of source mod 2**32: 951 bytes
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