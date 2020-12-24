# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/interceptor/log_interceptor.py
# Compiled at: 2018-06-03 12:36:26
from summermvc.mvc import HandlerInterceptor
from summermvc.decorator import *

@component
class LogInterceptor(HandlerInterceptor):

    @override
    def pre_handle(self, request, response, model_and_view):
        print 'pre_handle chain in LogInterceptor'

    @override
    def post_handle(self, request, response, model_and_view):
        print 'post_handle chain in LogInterceptor'

    @override
    def path_pattern(self):
        return '/.*'

    @override
    def get_order(self):
        return 1